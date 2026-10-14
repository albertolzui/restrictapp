import unittest
from unittest.mock import patch
from api import guidance

class GuidanceTests(unittest.TestCase):
    def setUp(self):
        guidance._cache.clear()

    @patch('api.guidance.fetch_document')
    def test_official_content_scope_safety_and_cache(self, fetch):
        fetch.return_value = {'document_type':'travel_advice', 'base_path':'/foreign-travel-advice/japan', 'public_updated_at':'2026-10-01T12:00:00Z',
            'details':{'parts':[{'slug':'entry-requirements','title':'Entry requirements','body':'<h2>Passport</h2><p>Test advice</p><script>dangerous()</script>'}]}}
        result = guidance.official_guidance('Japan')
        self.assertEqual(result['status'],'available')
        self.assertIn('British',result['scope'])
        self.assertNotIn('dangerous',result['sections'][0]['text'])
        self.assertEqual(result['updated_at'],'2026-10-01T12:00:00Z')
        guidance.official_guidance('Japan')
        self.assertEqual(fetch.call_count,1)

    @patch('api.guidance.fetch_document', side_effect=OSError('network unavailable'))
    def test_outage_fallback_does_not_invent_guidance(self, fetch):
        result = guidance.official_guidance('Japan')
        self.assertEqual(result['status'],'unavailable')
        self.assertIsNone(result['retrieved_at'])
        self.assertEqual(result['sections'],[])

    @patch('api.guidance.fetch_document')
    def test_wrong_document_rejected(self, fetch):
        fetch.return_value = {'document_type':'travel_advice','base_path':'/wrong-country'}
        self.assertEqual(guidance.official_guidance('Japan')['status'],'unavailable')
        self.assertEqual(guidance.official_guidance('United-Kingdom')['status'],'links_only')
