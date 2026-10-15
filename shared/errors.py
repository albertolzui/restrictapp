"""Safe localized errors across ASGI and Django. Exception text is never public."""
from http.cookies import SimpleCookie
import json
import logging
from pathlib import Path
import re
from uuid import uuid4
from starlette.responses import JSONResponse

MESSAGES=json.loads(Path(__file__).with_name('error-messages.json').read_text(encoding='utf-8'))
DEFAULTS={400:'invalid_request',401:'sign_in_required',403:'forbidden',404:'not_found',405:'method_not_allowed',408:'request_timeout',409:'conflict',413:'request_too_large',414:'invalid_request',415:'unsupported_media',422:'validation_failed',429:'rate_limited',500:'internal_error',502:'bad_gateway',503:'service_unavailable',504:'gateway_timeout'}
ALIASES={'Use a password of 12–128 characters that is not common, entirely numeric, or similar to your email.':'weak_password','Choose a different destination.':'same_destination','Choose countries from the list.':'invalid_countries','Invalid host.':'invalid_host','Email or password is incorrect.':'invalid_credentials','Sign in to manage your trips.':'sign_in_required','Trip not found.':'trip_not_found','Your security token has expired. Refresh and try again.':'csrf_failed','You can save up to 100 trips. Remove a trip before adding another.':'trip_limit'}

def request_id(value=''):
    return value if re.fullmatch(r'[a-f0-9]{32}',value or '') else uuid4().hex

def language(headers,preferred=None):
    explicit=headers.get('x-restrictapp-language','').lower()
    if explicit in {'en','de'}: return explicit
    if preferred in {'en','de'}: return preferred
    cookie=SimpleCookie()
    try: cookie.load(headers.get('cookie',''))
    except Exception: cookie=SimpleCookie()
    if 'restrictapp_language' in cookie and cookie['restrictapp_language'].value in {'en','de'}: return cookie['restrictapp_language'].value
    candidates=[]
    for index,item in enumerate(headers.get('accept-language','').split(',')):
        parts=item.strip().lower().split(';')
        base=parts[0].split('-')[0]
        try: quality=float(parts[1].strip().removeprefix('q=')) if len(parts)>1 else 1
        except ValueError: continue
        if base in {'en','de'} and 0<quality<=1: candidates.append((quality,-index,base))
    return max(candidates)[2] if candidates else 'en'

def payload(status,lang='en',identifier='',body=b''):
    code=DEFAULTS.get(status,'internal_error' if status>=500 else 'invalid_request')
    try:
        original=json.loads(body)
        supplied=original.get('error',{}).get('code')
        if supplied in MESSAGES and MESSAGES[supplied]['status']==status: code=supplied
        elif original.get('detail') in ALIASES: code=ALIASES[original['detail']]
    except (ValueError,TypeError,AttributeError): pass
    return {'detail':MESSAGES[code][lang],'error':{'code':code,'status':status,'request_id':identifier,'retryable':status in {408,429,500,502,503,504}}}

def log_failure(identifier,exc):
    logging.getLogger('restrictapp.errors').error('Request failed request_id=%s exception_type=%s',identifier,type(exc).__name__)

def unavailable(exc):
    return any(cls.__name__ in {'OperationalError','InterfaceError'} for cls in type(exc).__mro__)

class SafeDjangoLog(logging.Filter):
    def filter(self,record):
        record.msg='Django request failure status=%s request_id=%s'
        record.args=(getattr(record,'status_code','unknown'),getattr(getattr(record,'request',None),'error_request_id','unknown'))
        record.exc_info=None
        record.exc_text=None
        return True

class ErrorBoundary:
    def __init__(self,app): self.app=app
    async def __call__(self,scope,receive,send):
        if scope['type']!='http': return await self.app(scope,receive,send)
        incoming=dict(scope['headers'])
        identifier=request_id(incoming.get(b'x-request-id',b'').decode('latin1'))
        scope=dict(scope,headers=[(k,v) for k,v in scope['headers'] if k.lower()!=b'x-request-id']+[(b'x-request-id',identifier.encode())])
        lang=language({k.decode('latin1').lower():v.decode('latin1') for k,v in scope['headers']})
        start=None
        body=bytearray()
        started=False
        emitted=False
        async def safe_send(event):
            nonlocal start,started,emitted
            if event['type']=='http.response.start':
                start=event
                if event['status']>=400: return
                event['headers']=[(k,v) for k,v in event.get('headers',[]) if k.lower()!=b'x-request-id']+[(b'x-request-id',identifier.encode())]
                started=True
            elif event['type']=='http.response.body' and start and start['status']>=400:
                if len(body)<16384: body.extend(event.get('body',b'')[:16384-len(body)])
                if event.get('more_body',False): return
                original=dict(start.get('headers',[]))
                selected=original.get(b'content-language',lang.encode()).decode('latin1')
                selected=selected if selected in {'en','de'} else lang
                headers={k.decode('latin1'):v.decode('latin1') for k,v in start.get('headers',[]) if k.lower() in {b'allow',b'retry-after',b'strict-transport-security',b'x-frame-options',b'referrer-policy',b'permissions-policy',b'content-security-policy'}}
                headers.update({'Cache-Control':'no-store','Content-Language':selected,'X-Request-ID':identifier,'X-Content-Type-Options':'nosniff','Vary':'Accept-Language, X-Restrictapp-Language, Cookie'})
                emitted=True
                response=JSONResponse(payload(start['status'],selected,identifier,body),status_code=start['status'],headers=headers)
                response.raw_headers.extend((k,v) for k,v in start.get('headers',[]) if k.lower()==b'set-cookie')
                return await response(scope,receive,send)
            await send(event)
        try: await self.app(scope,receive,safe_send)
        except Exception as exc:
            log_failure(identifier,exc)
            if emitted: return
            if started: raise RuntimeError('Response interrupted; request_id='+identifier) from None
            status=503 if unavailable(exc) else 500
            await JSONResponse(payload(status,lang,identifier),status_code=status,headers={'Cache-Control':'no-store','Content-Language':lang,'X-Request-ID':identifier,'X-Content-Type-Options':'nosniff','Retry-After':'5'})(scope,receive,send)
