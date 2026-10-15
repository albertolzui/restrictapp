import struct
import unittest
from fastapi.testclient import TestClient
from api.main import app


class PwaTests(unittest.TestCase):
    def test_install_metadata_and_icons(self):
        with TestClient(app) as client:
            response = client.get('/manifest.webmanifest')
            self.assertEqual(response.status_code, 200)
            self.assertIn('application/manifest+json', response.headers['content-type'])
            manifest = response.json()
            self.assertEqual(manifest['display'], 'standalone')
            self.assertEqual(manifest['scope'], '/')
            self.assertEqual(manifest['id'], '/')
            german = client.get('/manifest.webmanifest?lang=de').json()
            self.assertEqual(german['lang'], 'de')
            self.assertEqual(german['id'], manifest['id'])
            self.assertEqual(german['start_url'], manifest['start_url'])
            for icon in manifest['icons']:
                response = client.get(icon['src'])
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.content[:8], b'\x89PNG\r\n\x1a\n')
                dimensions = struct.unpack('>II', response.content[16:24])
                self.assertEqual(icon['sizes'], f'{dimensions[0]}x{dimensions[1]}')
            apple = client.get('/static/images/app-icon-180.png').content
            self.assertEqual(struct.unpack('>II', apple[16:24]), (180,180))
            worker = client.get('/sw.js')
            self.assertEqual(worker.status_code, 200)
            self.assertIn('javascript', worker.headers['content-type'])
            self.assertEqual(worker.headers['cache-control'], 'no-cache')
            self.assertEqual(client.get('/static/app/offline.html').status_code, 200)
            self.assertIn('apple-touch-icon', client.get('/').text)


if __name__ == '__main__':
    unittest.main()
