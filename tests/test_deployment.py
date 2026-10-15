from contextlib import closing
import os
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from api import main,storage
from scripts.migrate_sqlite import read_source

class DeploymentTests(unittest.TestCase):
    def test_production_rejects_ephemeral_sqlite_and_insecure_configuration(self):
        config = {'RESTRICTAPP_ENV':'production','DATABASE_URL':'','RESTRICTAPP_SECURE_COOKIES':'1','RESTRICTAPP_RATE_SECRET':'x'*32}
        with patch.dict(os.environ,config):
            with self.assertRaises(RuntimeError): storage.validate_configuration()
        config['DATABASE_URL']='postgresql://example:placeholder@example.invalid/db?sslmode=require'
        with patch.dict(os.environ,config): storage.validate_configuration()
        config['DATABASE_URL']='postgresql://example:placeholder@example.invalid/db?sslmode=disable'
        with patch.dict(os.environ,config):
            with self.assertRaises(RuntimeError): storage.validate_configuration()

    def test_rate_limit_survives_connection_changes(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(main,'DB_PATH',Path(folder)/'test.sqlite3'), patch.dict(os.environ,{'DATABASE_URL':'','RESTRICTAPP_ENV':'development'}):
            with TestClient(main.app) as client:
                for _ in range(10):
                    self.assertEqual(client.post('/api/auth/login',json={'email':'test@example.com','password':'wrong-password'},headers={'X-Restrictapp':'1'}).status_code,401)
                response = client.post('/api/auth/login',json={'email':'test@example.com','password':'wrong-password'},headers={'X-Restrictapp':'1'})
                self.assertEqual(response.status_code,429)
                self.assertIn('Retry-After',response.headers)
                with main.database() as db:
                    db.execute('UPDATE auth_attempts SET expires=0')
                self.assertEqual(client.post('/api/auth/login',json={'email':'test@example.com','password':'wrong-password'},headers={'X-Restrictapp':'1'}).status_code,401)

    def test_secure_cookie_logout_headers_and_proxy_origin(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(main,'DB_PATH',Path(folder)/'test.sqlite3'), patch.dict(os.environ,{'DATABASE_URL':'','RESTRICTAPP_SECURE_COOKIES':'1','RESTRICTAPP_ENV':'development'}):
            with TestClient(main.app,base_url='https://restrictapp.example') as client:
                response = client.post('/api/auth/signup',json={'email':'test@example.com','password':'test-password-123'},headers={'X-Restrictapp':'1','Origin':'https://restrictapp.example'})
                self.assertEqual(response.status_code,202)
                response = client.post('/api/auth/login',json={'email':'test@example.com','password':'test-password-123'},headers={'X-Restrictapp':'1','Origin':'https://restrictapp.example'})
                self.assertEqual(response.status_code,200)
                self.assertIn('Secure',response.headers['set-cookie'])
                self.assertEqual(client.get('/api/me').status_code,200)
                self.assertEqual(response.headers['cache-control'],'no-store')
                self.assertEqual(response.headers['x-content-type-options'],'nosniff')
                self.assertEqual(client.post('/api/logout',headers={'X-Restrictapp':'1'}).status_code,200)
                self.assertEqual(client.get('/api/me').status_code,401)

    def test_read_only_migration_inventory_and_plaintext_rejection(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'source.sqlite3'
            with storage.database(path) as db:
                db.execute('INSERT INTO users(email,password) VALUES (?,?)',('test@example.com',main.password_hash('test-password-123')))
            result=read_source(path)
            self.assertEqual(len(result['users']),1)
            self.assertNotIn('sessions',result)
            with storage.database(path) as db:
                db.execute("UPDATE users SET password='plaintext'")
            with self.assertRaises(ValueError): read_source(path)
