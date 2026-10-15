"""Optional integration suite, restricted to a disposable restrictapp_test database."""
import os
import unittest
import json
from unittest.mock import patch
from urllib.parse import urlsplit
from fastapi.testclient import TestClient
import psycopg
from api import main,storage
from scripts.migrate_sqlite import copy_to_postgres

URL=os.getenv('RESTRICTAPP_TEST_DATABASE_URL','')

@unittest.skipUnless(URL,'Set RESTRICTAPP_TEST_DATABASE_URL to run the PostgreSQL integration test')
class PostgresTests(unittest.TestCase):
    def setUp(self):
        if urlsplit(URL).path != '/restrictapp_test' or urlsplit(URL).hostname not in {'127.0.0.1','localhost'}:
            self.fail('Integration tests require a disposable local restrictapp_test database.')

    def test_sqlite_migration_preserves_ids_progress_and_identity_sequences(self):
        rows={'users':[{'id':42,'email':'migrated@example.com','password':main.password_hash('test-password-123')}],
            'trips':[{'id':88,'user_id':42,'origin':'Germany','destination':'Japan','created':'2026-10-14 12:00:00','context':json.dumps({'nationality':'Nigeria','residence':'Germany'})}],
            'profiles':[{'user_id':42,'data':json.dumps({'nationality':'Nigeria','residence':'Germany','passport_expiry':None})}],
            'checklist_progress':[{'trip_id':88,'task_id':'passport','done':1}]}
        with patch.dict(os.environ,{'DATABASE_URL':URL,'RESTRICTAPP_ENV':'development','RESTRICTAPP_SECURE_COOKIES':'0'}):
            with main.database() as db:
                db.execute('TRUNCATE users,auth_attempts RESTART IDENTITY CASCADE')
            copy_to_postgres(rows,main.database)
            with self.assertRaises(ValueError): copy_to_postgres(rows,main.database)
            with TestClient(main.app) as client:
                headers={'X-Restrictapp':'1'}
                self.assertEqual(client.post('/api/auth/login',json={'email':'migrated@example.com','password':'test-password-123'},headers=headers).status_code,200)
                self.assertEqual(client.get('/api/me').json()['id'],42)
                trip=client.get('/api/trips').json()[0]
                self.assertEqual(trip['id'],88)
                self.assertTrue(trip['checklist'][0]['done'])
                self.assertEqual(client.post('/api/auth/signup',json={'email':'next@example.com','password':'test-password-123'},headers=headers).status_code,202)
                self.assertEqual(client.post('/api/auth/login',json={'email':'next@example.com','password':'test-password-123'},headers=headers).status_code,200)
                self.assertEqual(client.get('/api/me').json()['id'],43)
                self.assertEqual(client.post('/api/trips',json={'origin':'Germany','destination':'Italy'},headers=headers).json()['id'],89)
            with main.database() as db:
                db.execute('TRUNCATE users,auth_attempts RESTART IDENTITY CASCADE')

    def test_full_postgres_account_trip_profile_and_progress_flow(self):
        if urlsplit(URL).path != '/restrictapp_test' or urlsplit(URL).hostname not in {'127.0.0.1','localhost'}:
            self.fail('Integration tests require a disposable local restrictapp_test database.')
        with patch.dict(os.environ,{'DATABASE_URL':URL,'RESTRICTAPP_ENV':'development','RESTRICTAPP_SECURE_COOKIES':'0'}):
            with main.database() as db:
                db.execute('TRUNCATE users,auth_attempts RESTART IDENTITY CASCADE')
            with TestClient(main.app) as client:
                headers={'X-Restrictapp':'1'}
                account={'email':'pg-test@example.com','password':'test-password-123'}
                self.assertEqual(client.post('/api/auth/signup',json=account,headers=headers).status_code,202)
                self.assertEqual(client.post('/api/auth/login',json=account,headers=headers).status_code,200)
                self.assertEqual(client.post('/api/auth/signup',json=account,headers=headers).status_code,202)
                profile={'nationality':'Nigeria','residence':'Germany','passport_expiry':None}
                self.assertEqual(client.put('/api/profile',json=profile,headers=headers).status_code,200)
                self.assertEqual(client.get('/api/profile').json(),profile)
                trip={**profile,'origin':'Germany','destination':'Japan'}
                trip_id=client.post('/api/trips',json=trip,headers=headers).json()['id']
                self.assertEqual(client.post('/api/trips',json=trip,headers=headers).json()['id'],trip_id)
                self.assertEqual(client.put(f'/api/trips/{trip_id}/checklist/passport',json={'done':True},headers=headers).status_code,200)
                self.assertTrue(client.get('/api/trips').json()[0]['checklist'][0]['done'])
                self.assertEqual(client.get('/api/health').json()['database'],'postgresql')
                self.assertEqual(client.delete(f'/api/trips/{trip_id}',headers=headers).status_code,200)
                self.assertEqual(client.post('/api/logout',headers=headers).status_code,200)
                self.assertEqual(client.post('/api/auth/login',json=account,headers=headers).status_code,200)
                self.assertEqual(client.get('/api/me').json()['email'],account['email'])
            with main.database() as db:
                db.execute('TRUNCATE users,auth_attempts RESTART IDENTITY CASCADE')
