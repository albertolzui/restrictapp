import json
import os
import tempfile
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path
from unittest.mock import patch
from api.travel_data import route_data

class TravelDataTests(unittest.TestCase):
    def test_feed_freshness_and_safe_sources(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'feed.json'
            record = {'origin':'Germany','destination':'Japan', 'summary':'Test fixture, not travel advice.',
                'checked_at':datetime.now(timezone.utc).isoformat(),
                'requirements':[{'title':'Test requirement','detail':'Fixture only.'}],
                'sources':[{'title':'Test source','url':'https://example.com/fixture'}]}
            with patch.dict(os.environ, {'RESTRICTAPP_TRAVEL_FEED':str(path)}):
                path.write_text(json.dumps([record]), encoding='utf-8')
                self.assertEqual(route_data('Germany','Japan')['status'], 'sourced')
                self.assertEqual(route_data('Germany','Italy')['status'], 'unverified')
                record['checked_at'] = (datetime.now(timezone.utc)-timedelta(days=2)).isoformat()
                path.write_text(json.dumps([record]), encoding='utf-8')
                self.assertEqual(route_data('Germany','Japan')['status'], 'stale')
                record['sources'][0]['url'] = 'javascript:alert(1)'
                path.write_text(json.dumps([record]), encoding='utf-8')
                self.assertEqual(route_data('Germany','Japan')['status'], 'unverified')
                path.write_text('invalid json', encoding='utf-8')
                self.assertEqual(route_data('Germany','Japan')['status'], 'unverified')

    def test_missing_feed(self):
        with patch.dict(os.environ, {'RESTRICTAPP_TRAVEL_FEED':''}):
            self.assertEqual(route_data('Germany','Japan')['sources'], [])
