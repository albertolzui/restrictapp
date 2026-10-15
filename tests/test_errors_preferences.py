from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from api import main,storage

class ErrorPreferenceTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.override=patch.object(main,'DB_PATH',Path(self.temp.name)/'test.sqlite3');self.override.start()
        self.client=TestClient(main.app);self.headers={'X-Restrictapp':'1','X-Restrictapp-Language':'de'}
        self.credentials={'email':'language@example.com','password':'test-password-123'}
    def tearDown(self):
        self.client.close();self.override.stop();self.temp.cleanup()
    def test_saved_language_survives_a_fresh_login_and_rejects_invalid_choices(self):
        self.client.post('/api/auth/signup',json=self.credentials,headers=self.headers)
        self.client.post('/api/auth/login',json=self.credentials,headers=self.headers)
        self.assertEqual(self.client.get('/api/preferences').json()['language'],'de')
        self.assertEqual(self.client.put('/api/preferences',json={'language':'fr'},headers=self.headers).status_code,422)
        self.assertEqual(self.client.put('/api/preferences',json={'language':'en'},headers=self.headers).status_code,200)
        with TestClient(main.app) as fresh:
            response=fresh.post('/api/auth/login',json=self.credentials,headers=self.headers)
            self.assertEqual(response.json()['preferred_language'],'en')
        self.assertEqual(self.client.get('/api/account/export').json()['account']['preferred_language'],'en')
    def test_localized_safe_errors_and_database_outage(self):
        response=self.client.post('/api/auth/login',json=self.credentials,headers=self.headers)
        self.assertEqual(response.status_code,401)
        self.assertEqual(response.json()['error']['code'],'invalid_credentials')
        self.assertIn('falsch',response.json()['detail'])
        self.assertEqual(self.client.get('/api/missing',headers=self.headers).headers['Content-Language'],'de')
        self.client.post('/api/auth/signup',json=self.credentials,headers=self.headers)
        self.client.post('/api/auth/login',json=self.credentials,headers=self.headers)
        with patch.object(main,'database',side_effect=storage.DatabaseUnavailable('PRIVATE_DATABASE_SECRET')):
            response=self.client.get('/api/me',headers=self.headers)
        self.assertEqual(response.status_code,503)
        self.assertNotIn('PRIVATE',response.text)
        self.assertEqual(response.headers['Cache-Control'],'no-store')
