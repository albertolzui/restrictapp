import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from fastapi.testclient import TestClient
from api import main

class SecurityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.override = patch.object(main,'DB_PATH',Path(self.temp.name)/'security.sqlite3')
        self.override.start()
        self.client = TestClient(main.app)
    def tearDown(self):
        self.client.close()
        self.override.stop()
        self.temp.cleanup()
    def test_oversized_and_chunked_requests_rejected(self):
        self.assertEqual(self.client.post('/api/plan',content=b'x'*32769).status_code,413)
        self.assertEqual(self.client.post('/api/plan',content=iter([b'x'*20000,b'x'*20000])).status_code,413)
    def test_validation_never_echoes_credentials(self):
        response=self.client.post('/api/auth/login',json={'email':'test@example.com','password':'secret'})
        self.assertEqual(response.status_code,422)
        self.assertNotIn('secret',response.text)
        self.assertNotIn('input',response.text)
    def test_browser_policies_and_fetch_metadata(self):
        response=self.client.get('/')
        self.assertIn("script-src 'self'",response.headers['content-security-policy'])
        self.assertIn("object-src 'none'",response.headers['content-security-policy'])
        self.assertEqual(response.headers['cross-origin-opener-policy'],'same-origin')
        response=self.client.post('/api/auth/signup',json={'email':'a@example.com','password':'test-password-123'},headers={'X-Restrictapp':'1','Sec-Fetch-Site':'cross-site'})
        self.assertEqual(response.status_code,403)
    def test_missing_user_still_hashes_password(self):
        with patch.object(main,'password_hash',wraps=main.password_hash) as hasher:
            response=self.client.post('/api/auth/login',json={'email':'nobody@example.com','password':'test-password-123'},headers={'X-Restrictapp':'1'})
            self.assertEqual(response.status_code,401)
            hasher.assert_called_once()
    def test_signup_response_does_not_reveal_account_existence(self):
        credentials={'email':'new@example.com','password':'test-password-123'}
        first=self.client.post('/api/auth/signup',json=credentials,headers={'X-Restrictapp':'1'})
        again=self.client.post('/api/auth/signup',json=credentials,headers={'X-Restrictapp':'1'})
        self.assertEqual(first.status_code,202)
        self.assertEqual(first.json(),again.json())
        self.assertNotIn('set-cookie',first.headers)
        self.assertNotIn('set-cookie',again.headers)
        self.assertEqual(self.client.get('/api/me').status_code,401)
