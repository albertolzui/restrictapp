import tempfile
import unittest
import sqlite3
from contextlib import closing
from pathlib import Path
from fastapi.testclient import TestClient
from api import main


class AppTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.original = main.DB_PATH
        main.DB_PATH = Path(self.temp.name) / 'test.sqlite3'
        self.client = TestClient(main.app)
        self.headers = {'X-Restrictapp': '1'}

    def tearDown(self):
        self.client.close()
        main.DB_PATH = self.original
        self.temp.cleanup()

    def signup(self, client, email='test@example.com'):
        credentials = {'email': email, 'password': 'test-password-123'}
        self.assertEqual(client.post('/api/auth/signup', json=credentials, headers=self.headers).status_code,202)
        return client.post('/api/auth/login', json=credentials, headers=self.headers)

    def test_account_export_and_deletion(self):
        self.assertEqual(self.client.get('/api/account/export').status_code, 401)
        self.signup(self.client)
        other = TestClient(main.app)
        self.signup(other, 'other@example.com')
        self.client.put('/api/profile', json={'nationality':'Nigeria','residence':'Germany'}, headers=self.headers)
        trip = self.client.post('/api/trips', json={'origin':'Germany','destination':'Japan','nationality':'Nigeria','residence':'Germany'}, headers=self.headers).json()
        self.client.put(f"/api/trips/{trip['id']}/checklist/passport", json={'done':True}, headers=self.headers)
        export = self.client.get('/api/account/export')
        self.assertEqual(export.status_code, 200)
        self.assertEqual(export.headers['cache-control'], 'no-store')
        self.assertEqual(export.json()['profile']['nationality'], 'Nigeria')
        self.assertEqual(len(export.json()['trips']), 1)
        self.assertEqual(export.json()['trips'][0]['checklist_progress'][0]['done'], 1)
        self.assertNotIn('password', export.text)
        self.assertNotIn('token', export.text)
        self.assertNotIn('other@example.com', export.text)
        credentials = {'email':'test@example.com','password':'test-password-123'}
        self.assertEqual(self.client.request('DELETE','/api/account',json=credentials).status_code, 403)
        self.assertEqual(self.client.request('DELETE','/api/account',json={**credentials,'password':'wrong-password'},headers=self.headers).status_code, 401)
        self.assertEqual(self.client.get('/api/me').status_code, 200)
        self.assertEqual(self.client.request('DELETE','/api/account',json=credentials,headers=self.headers).status_code, 200)
        self.assertEqual(self.client.get('/api/me').status_code, 401)
        with main.database() as db:
            for table in ('profiles','trips','checklist_progress'):
                self.assertEqual(db.execute(f'SELECT COUNT(*) AS count FROM {table}').fetchone()['count'], 0)
            self.assertEqual(db.execute('SELECT COUNT(*) AS count FROM users').fetchone()['count'], 1)
            self.assertEqual(db.execute('SELECT COUNT(*) AS count FROM sessions').fetchone()['count'], 1)
        self.assertEqual(other.get('/api/me').status_code, 200)
        other.close()

    def test_privacy_pages_and_no_external_fonts(self):
        for path in ('/privacy','/cookies'):
            self.assertEqual(self.client.get(path).status_code, 200)
        self.assertIn('Restrictapp Admin', self.client.get('/privacy').text)
        self.assertNotIn('fonts.googleapis', self.client.get('/static/app/style.css').text)

    def test_search_validation_and_honest_data_state(self):
        self.assertEqual(self.client.get('/').status_code, 200)
        self.assertIn('Germany', self.client.get('/api/countries').json())
        result = self.client.get('/api/search', params={'origin':'Germany','destination':'Japan'})
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json()['status'], 'unverified')
        self.assertIsNone(result.json()['checked_at'])
        for destination in ['Germany', 'Atlantis']:
            self.assertEqual(self.client.get('/api/search', params={'origin':'Germany','destination':destination}).status_code, 422)

    def test_accounts_hashing_sessions_and_logout(self):
        response = self.signup(self.client)
        self.assertEqual(response.status_code, 200)
        self.assertIn('HttpOnly', response.headers['set-cookie'])
        with main.database() as db:
            stored = db.execute('SELECT password FROM users').fetchone()['password']
            self.assertNotEqual(stored, 'test-password-123')
            self.assertTrue(main.password_hash('test-password-123', stored.split(':')[0]) == stored)
        self.assertEqual(self.client.post('/api/auth/signup',json={'email':'test@example.com','password':'test-password-123'},headers=self.headers).status_code,202)
        self.assertEqual(self.client.get('/api/me').status_code, 200)
        self.assertEqual(self.client.post('/api/logout', headers=self.headers).status_code, 200)
        self.assertEqual(self.client.get('/api/me').status_code, 401)
        self.assertEqual(self.client.post('/api/auth/login', json={'email':'test@example.com','password':'incorrect-password'}, headers=self.headers).status_code, 401)
        self.assertEqual(self.client.post('/api/auth/login', json={'email':'test@example.com','password':'test-password-123'}, headers=self.headers).status_code, 200)

    def test_trip_ownership_and_deduplication(self):
        self.assertEqual(self.client.get('/api/trips').status_code, 401)
        self.signup(self.client)
        trip = {'origin':'Germany','destination':'Japan'}
        for _ in range(2):
            self.assertEqual(self.client.post('/api/trips', json=trip, headers=self.headers).status_code, 201)
        trips = self.client.get('/api/trips').json()
        self.assertEqual(len(trips), 1)
        with TestClient(main.app) as other:
            self.signup(other, 'other@example.com')
            self.assertEqual(other.get('/api/trips').json(), [])
            self.assertEqual(other.delete('/api/trips/'+str(trips[0]['id']), headers=self.headers).status_code, 404)
        self.assertEqual(self.client.delete('/api/trips/'+str(trips[0]['id']), headers=self.headers).status_code, 200)
        self.assertEqual(self.client.get('/api/trips').json(), [])

    def test_cross_site_writes_blocked_and_sessions_expire(self):
        self.assertEqual(self.client.post('/api/auth/signup', json={'email':'test@example.com','password':'test-password-123'}).status_code, 403)
        self.assertEqual(self.client.post('/api/auth/signup', json={'email':'test@example.com','password':'test-password-123'}, headers={**self.headers, 'Origin':'https://other.example'}).status_code, 403)
        self.signup(self.client)
        with main.database() as db:
            db.execute('UPDATE sessions SET expires=0')
        self.assertEqual(self.client.get('/api/me').status_code, 401)

    def test_profile_and_plan_context(self):
        self.assertEqual(self.client.get('/api/profile').status_code, 401)
        self.signup(self.client)
        profile = {'nationality':'Nigeria', 'residence':'Germany', 'passport_expiry':'2027-01-01'}
        self.assertEqual(self.client.put('/api/profile', json=profile, headers=self.headers).status_code, 200)
        self.assertEqual(self.client.get('/api/profile').json(), profile)
        plan = {**profile, 'origin':'Germany','destination':'Japan','departure_date':'2027-02-01','return_date':'2027-02-15','purpose':'study','transit':'United-Kingdom'}
        result = self.client.post('/api/plan', json=plan)
        self.assertEqual(result.status_code, 200)
        self.assertIn('transit', [task['id'] for task in result.json()['checklist']])
        self.assertTrue(any('expires before' in note for note in result.json()['notes']))
        self.assertTrue(any('Work and study' in note for note in result.json()['notes']))
        self.assertIn('route-level', result.json()['scope'])
        self.assertEqual(self.client.post('/api/plan', json={**plan,'return_date':'2027-01-01'}).status_code, 422)
        self.assertEqual(self.client.post('/api/plan', json={**plan,'nationality':'Atlantis'}).status_code, 422)
        with TestClient(main.app) as other:
            self.signup(other, 'other@example.com')
            self.assertEqual(other.get('/api/profile').json()['nationality'], '')

    def test_checklist_owner_progress_and_context_reset(self):
        self.signup(self.client)
        trip = {'origin':'Germany','destination':'Japan','nationality':'Nigeria','residence':'Germany'}
        trip_id = self.client.post('/api/trips', json=trip, headers=self.headers).json()['id']
        url = f'/api/trips/{trip_id}/checklist/passport'
        self.assertEqual(self.client.put(url, json={'done':True}, headers=self.headers).status_code, 200)
        self.assertTrue(self.client.get('/api/trips').json()[0]['checklist'][0]['done'])
        self.client.post('/api/trips', json=trip, headers=self.headers)
        self.assertTrue(self.client.get('/api/trips').json()[0]['checklist'][0]['done'])
        self.client.post('/api/trips', json={**trip,'nationality':'France'}, headers=self.headers)
        self.assertFalse(self.client.get('/api/trips').json()[0]['checklist'][0]['done'])
        self.assertEqual(self.client.put(f'/api/trips/{trip_id}/checklist/made-up', json={'done':True}, headers=self.headers).status_code, 422)
        with TestClient(main.app) as other:
            self.signup(other, 'other@example.com')
            self.assertEqual(other.put(url,json={'done':True},headers=self.headers).status_code,404)
        self.client.delete(f'/api/trips/{trip_id}',headers=self.headers)
        with main.database() as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM checklist_progress').fetchone()[0],0)

    def test_existing_database_migration_preserves_trip(self):
        with closing(sqlite3.connect(main.DB_PATH)) as db, db:
            db.executescript("CREATE TABLE users(id INTEGER PRIMARY KEY,email TEXT UNIQUE NOT NULL,password TEXT NOT NULL); CREATE TABLE trips(id INTEGER PRIMARY KEY,user_id INTEGER,origin TEXT,destination TEXT,created TEXT DEFAULT CURRENT_TIMESTAMP,UNIQUE(user_id,origin,destination)); INSERT INTO users VALUES(1,'old@example.com','hash'); INSERT INTO trips(user_id,origin,destination) VALUES(1,'Germany','Japan');")
        with main.database() as db:
            row = db.execute('SELECT origin,context FROM trips').fetchone()
            self.assertEqual(row['origin'],'Germany')
            self.assertEqual(row['context'],'{}')


if __name__ == '__main__':
    unittest.main()
