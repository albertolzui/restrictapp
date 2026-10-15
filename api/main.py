"""Restrictapp 2 local application. Legacy MongoDB code is not imported."""
import json
import hashlib
import hmac
import os
from pathlib import Path
import secrets
import time
from datetime import date
from typing import Literal
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from api.travel_data import route_data
from api.planning import checklist, planning_notes, authority_links
from api.guidance import official_guidance
from api.entry_reference import lookup
from api import storage
from api.security import auth_throttle
from starlette.middleware.trustedhost import TrustedHostMiddleware

ROOT = Path(__file__).resolve().parent
DB_PATH = Path(os.getenv('RESTRICTAPP_DB', str(ROOT / 'data/restrictapp.sqlite3')))
COUNTRIES = json.loads((ROOT / 'countries.json').read_text(encoding='utf-8'))
@asynccontextmanager
async def lifespan(app):
    storage.validate_configuration()
    with database() as db:
        db.execute('SELECT 1')
    yield

app = FastAPI(title='Restrictapp', version='2.0.0', lifespan=lifespan)
app.mount('/static', StaticFiles(directory=ROOT / 'static'), name='static')
allowed_hosts = os.getenv('RESTRICTAPP_ALLOWED_HOSTS') or os.getenv('RENDER_EXTERNAL_HOSTNAME')
if allowed_hosts:
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=[host.strip() for host in allowed_hosts.split(',') if host.strip()])

def database():
    return storage.database(DB_PATH)

@app.middleware('http')
async def response_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['X-Frame-Options'] = 'DENY'
    if request.url.path.startswith('/api/'):
        response.headers['Cache-Control'] = 'no-store'
    if storage.production():
        response.headers['Strict-Transport-Security'] = 'max-age=31536000'
    return response

def password_hash(password, salt=None):
    salt = salt or secrets.token_hex(16)
    return salt + ':' + hashlib.scrypt(password.encode(), salt=salt.encode(), n=16384, r=8, p=1).hex()

def current_user(request):
    token = request.cookies.get('restrictapp_session', '')
    with database() as db:
        user = db.execute('SELECT users.id,users.email FROM sessions JOIN users ON users.id=sessions.user_id WHERE token=? AND expires>?', (hashlib.sha256(token.encode()).hexdigest(), time.time())).fetchone()
    if not user:
        raise HTTPException(401, 'Sign in to manage your trips.')
    return dict(user)

def protect_write(request):
    if request.headers.get('x-restrictapp') != '1':
        raise HTTPException(403, 'Invalid request.')
    origin = request.headers.get('origin')
    if origin and origin.rstrip('/') != str(request.base_url).rstrip('/'):
        raise HTTPException(403, 'Invalid origin.')

class Credentials(BaseModel):
    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=10, max_length=128)

class Traveler(BaseModel):
    nationality: str = ''
    residence: str = ''
    passport_expiry: date | None = None

class Trip(Traveler):
    origin: str
    destination: str
    departure_date: date | None = None
    return_date: date | None = None
    purpose: Literal['tourism', 'business', 'work', 'study'] = 'tourism'
    transit: str = ''

class TaskProgress(BaseModel):
    done: bool

def validate_context(data):
    for field in ('nationality', 'residence', 'transit'):
        value = getattr(data, field, '')
        if value and value not in COUNTRIES:
            raise HTTPException(422, 'Choose countries from the list.')
    if isinstance(data, Trip):
        validate_trip(data.origin, data.destination)
        if data.return_date and not data.departure_date:
            raise HTTPException(422, 'Add a departure date before a return date.')
        if data.departure_date and data.return_date and data.return_date < data.departure_date:
            raise HTTPException(422, 'Return date must be on or after departure.')
        if data.transit and data.transit in {data.origin, data.destination}:
            raise HTTPException(422, 'Choose a transit country different from your origin and destination.')

def validate_trip(origin, destination):
    if origin not in COUNTRIES or destination not in COUNTRIES:
        raise HTTPException(422, 'Choose countries from the list.')
    if origin == destination:
        raise HTTPException(422, 'Choose a different destination.')

@app.get('/')
def home():
    return FileResponse(ROOT / 'static/app/index.html')

@app.get('/manifest.webmanifest')
def web_manifest(request: Request):
    filename = 'manifest.de.webmanifest' if request.query_params.get('lang') == 'de' else 'manifest.webmanifest'
    return FileResponse(ROOT / ('static/app/' + filename), media_type='application/manifest+json', headers={'Cache-Control': 'no-cache'})

@app.get('/sw.js')
def service_worker():
    return FileResponse(ROOT / 'static/app/sw.js', media_type='application/javascript', headers={'Cache-Control': 'no-cache'})

@app.get('/privacy')
@app.get('/cookies')
def privacy_page():
    return FileResponse(ROOT / 'static/app/privacy.html')

@app.get('/api/privacy')
def privacy_details():
    return {'operator': os.getenv('RESTRICTAPP_OPERATOR_NAME', 'Restrictapp Admin'),
            'contact': os.getenv('RESTRICTAPP_PRIVACY_EMAIL', 'olanipekun_albert@live.com')}

@app.get('/api/account/export')
def export_account(request: Request):
    user = current_user(request)
    with database() as db:
        profile = db.execute('SELECT data FROM profiles WHERE user_id=?', (user['id'],)).fetchone()
        saved = [dict(row) for row in db.execute('SELECT id,origin,destination,created,context FROM trips WHERE user_id=?', (user['id'],))]
        for trip in saved:
            trip['context'] = json.loads(trip['context'])
            trip['checklist_progress'] = [dict(row) for row in db.execute('SELECT task_id,done FROM checklist_progress WHERE trip_id=?', (trip['id'],))]
    return JSONResponse({'account': user, 'profile': json.loads(profile['data']) if profile else None, 'trips': saved},
        headers={'Content-Disposition': 'attachment; filename="restrictapp-account.json"'})

@app.delete('/api/account')
def delete_account(data: Credentials, request: Request, response: Response):
    protect_write(request)
    user = current_user(request)
    auth_throttle(database, request, user['email'])
    with database() as db:
        row = db.execute('SELECT password FROM users WHERE id=?', (user['id'],)).fetchone()
        if data.email.strip().lower() != user['email'] or not hmac.compare_digest(password_hash(data.password, row['password'].split(':')[0]), row['password']):
            raise HTTPException(401, 'Email or password is incorrect.')
        db.execute('DELETE FROM users WHERE id=?', (user['id'],))
    response.delete_cookie('restrictapp_session', secure=os.getenv('RESTRICTAPP_SECURE_COOKIES') == '1', httponly=True, samesite='lax')
    return {'ok': True}

@app.get('/api/health')
def health():
    try:
        with database() as db:
            db.execute('SELECT 1').fetchone()
    except Exception:
        raise HTTPException(503,'Database is unavailable.')
    return {'status': 'ok', 'database':'postgresql' if os.getenv('DATABASE_URL') else 'sqlite', 'travel_data': 'configured' if os.getenv('RESTRICTAPP_TRAVEL_FEED') else 'reference_snapshot'}

@app.get('/api/countries')
def countries():
    return COUNTRIES

@app.get('/api/search')
def search(origin: str, destination: str):
    validate_trip(origin, destination)
    return route_data(origin, destination)

@app.post('/api/plan')
def plan(data: Trip):
    validate_context(data)
    context = data.model_dump(mode='json')
    result = route_data(data.origin, data.destination)
    return {**result, 'traveler':context, 'notes':planning_notes(context), 'checklist':checklist(context), 'authority_links':authority_links(context), 'entry_reference':lookup(context),
        'scope':'This preparation plan does not determine entry eligibility. Any travel-feed information is route-level and has not been checked against your passport, residence, dates, or transit.'}

@app.get('/api/guidance/{destination}')
def guidance(destination: str):
    if destination not in COUNTRIES:
        raise HTTPException(422, 'Choose a country from the list.')
    return official_guidance(destination)

@app.get('/api/profile')
def profile(request: Request):
    user = current_user(request)
    with database() as db:
        row = db.execute('SELECT data FROM profiles WHERE user_id=?', (user['id'],)).fetchone()
    return json.loads(row['data']) if row else Traveler().model_dump(mode='json')

@app.put('/api/profile')
def save_profile(data: Traveler, request: Request):
    protect_write(request)
    user = current_user(request)
    validate_context(data)
    if not data.nationality or not data.residence:
        raise HTTPException(422, 'Choose your passport country and country of residence.')
    with database() as db:
        db.execute('INSERT INTO profiles(user_id,data) VALUES (?,?) ON CONFLICT(user_id) DO UPDATE SET data=excluded.data',
            (user['id'], data.model_dump_json()))
    return data.model_dump(mode='json')

@app.post('/api/auth/{action}')
def authenticate(action: str, data: Credentials, request: Request, response: Response):
    protect_write(request)
    if action not in {'signup', 'login'}:
        raise HTTPException(404, 'Unknown action.')
    email = data.email.strip().lower()
    if '@' not in email or '.' not in email.rsplit('@', 1)[-1] or ' ' in email:
        raise HTTPException(422, 'Enter a valid email address.')
    auth_throttle(database, request, email)
    with database() as db:
        if action == 'signup':
            try:
                db.execute('INSERT INTO users(email,password) VALUES (?,?)', (email, password_hash(data.password)))
            except storage.INTEGRITY_ERRORS:
                raise HTTPException(409, 'This email is already registered.')
        user = db.execute('SELECT * FROM users WHERE email=?', (email,)).fetchone()
        if not user or not hmac.compare_digest(password_hash(data.password, user['password'].split(':')[0]), user['password']):
            raise HTTPException(401, 'Email or password is incorrect.')
        token = secrets.token_urlsafe(32)
        db.execute('DELETE FROM sessions WHERE expires<=?', (time.time(),))
        db.execute('INSERT INTO sessions VALUES (?,?,?)', (hashlib.sha256(token.encode()).hexdigest(), user['id'], time.time()+604800))
    response.set_cookie('restrictapp_session', token, httponly=True, samesite='lax', secure=os.getenv('RESTRICTAPP_SECURE_COOKIES') == '1', max_age=604800)
    return {'email': email}

@app.get('/api/me')
def me(request: Request):
    return current_user(request)

@app.post('/api/logout')
def logout(request: Request, response: Response):
    protect_write(request)
    with database() as db:
        db.execute('DELETE FROM sessions WHERE token=?', (hashlib.sha256(request.cookies.get('restrictapp_session', '').encode()).hexdigest(),))
    response.delete_cookie('restrictapp_session', secure=os.getenv('RESTRICTAPP_SECURE_COOKIES') == '1', httponly=True, samesite='lax')
    return {'ok': True}

@app.get('/api/trips')
def trips(request: Request):
    user = current_user(request)
    with database() as db:
        rows = [dict(row) for row in db.execute('SELECT id,origin,destination,created,context FROM trips WHERE user_id=? ORDER BY id DESC', (user['id'],))]
        for row in rows:
            row['context'] = json.loads(row['context'])
            done = {task['task_id'] for task in db.execute('SELECT task_id FROM checklist_progress WHERE trip_id=? AND done=1', (row['id'],))}
            row['checklist'] = [{**task, 'done':task['id'] in done} for task in checklist(row['context'])]
        return rows

@app.post('/api/trips', status_code=201)
def save_trip(data: Trip, request: Request):
    protect_write(request)
    user = current_user(request)
    validate_context(data)
    with database() as db:
        existing = db.execute('SELECT id,context FROM trips WHERE user_id=? AND origin=? AND destination=?', (user['id'], data.origin, data.destination)).fetchone()
        context = data.model_dump_json()
        if existing:
            if json.loads(existing['context']) != data.model_dump(mode='json'):
                db.execute('DELETE FROM checklist_progress WHERE trip_id=?', (existing['id'],))
            db.execute('UPDATE trips SET context=? WHERE id=?', (context, existing['id']))
            trip_id = existing['id']
        else:
            trip_id = db.execute('INSERT INTO trips(user_id,origin,destination,context) VALUES (?,?,?,?) RETURNING id', (user['id'], data.origin, data.destination, context)).fetchone()['id']
    return {'ok': True, 'id':trip_id}

@app.put('/api/trips/{trip_id}/checklist/{task_id}')
def update_task(trip_id: int, task_id: str, data: TaskProgress, request: Request):
    protect_write(request)
    user = current_user(request)
    with database() as db:
        trip = db.execute('SELECT context FROM trips WHERE id=? AND user_id=?', (trip_id, user['id'])).fetchone()
        if not trip:
            raise HTTPException(404, 'Trip not found.')
        if task_id not in {task['id'] for task in checklist(json.loads(trip['context']))}:
            raise HTTPException(422, 'Unknown checklist task.')
        db.execute('INSERT INTO checklist_progress(trip_id,task_id,done) VALUES (?,?,?) ON CONFLICT(trip_id,task_id) DO UPDATE SET done=excluded.done', (trip_id, task_id, int(data.done)))
    return {'ok':True}

@app.delete('/api/trips/{trip_id}')
def delete_trip(trip_id: int, request: Request):
    protect_write(request)
    user = current_user(request)
    with database() as db:
        if db.execute('DELETE FROM trips WHERE id=? AND user_id=?', (trip_id, user['id'])).rowcount == 0:
            raise HTTPException(404, 'Trip not found.')
    return {'ok': True}
