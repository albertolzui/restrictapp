from copy import deepcopy
from datetime import date
import unittest
from api.entry_reference import lookup

class EntryReferenceTests(unittest.TestCase):
    def setUp(self):
        self.context = {'nationality':'Nigeria','destination':'Japan','residence':'Germany','purpose':'tourism'}
        self.data = {'provider':'TravelRequirements.info','publisher':'Fixture','version':'test','commit':'fixture','imported_at':'2026-10-14T12:00:00Z','license':'CC-BY-4.0','license_url':'https://creativecommons.org/licenses/by/4.0/','attribution':'Test fixture only','dataset_url':'https://travelrequirements.info/en/data/',
            'country_codes':{'Nigeria':'NG','Japan':'JP'},'destinations':{'JP':{'primary_sources':[], 'rows':{'NG':{'category':'embassy-visa','evidence_level':'passport-row','source':{'url':'https://www.mofa.go.jp/j_info/visit/visa/index.html','name':'Test source','type':'government','lastVerified':'2026-10-13'}}}}}}

    def read(self, data=None, context=None):
        return lookup(context or self.context, data or self.data, today=date(2026,10,14))

    def test_sourced_result_is_dataset_reported_not_verified(self):
        result = self.read()
        self.assertEqual(result['status'],'dataset_reported')
        self.assertEqual(result['publisher_checked_at'],'2026-10-13')
        self.assertEqual(result['check_age_days'],1)
        self.assertIn('Residence permits', result['limitations'][0])
        self.assertEqual(result['source']['url'],self.data['destinations']['JP']['rows']['NG']['source']['url'])

    def test_flagged_and_stale_rows_withhold_category_keep_links(self):
        for flag in ['unverifiable','conflict','portalOnly']:
            data = deepcopy(self.data); data['destinations']['JP']['rows']['NG']['source'][flag] = True
            result = self.read(data)
            self.assertEqual(result['status'],'links_only')
            self.assertIsNone(result['category'])
            self.assertTrue(result['links'])
        for checked in ['2026-10-01','2026-10-15','not-a-date']:
            data = deepcopy(self.data); data['destinations']['JP']['rows']['NG']['source']['lastVerified'] = checked
            self.assertIsNone(self.read(data)['category'])

    def test_unknown_unsafe_purpose_and_expired_rules(self):
        for category in ['unconfirmed','new-schema-value']:
            data = deepcopy(self.data); data['destinations']['JP']['rows']['NG']['category'] = category
            self.assertEqual(self.read(data)['status'],'links_only')
        data = deepcopy(self.data); data['destinations']['JP']['rows']['NG']['source']['url'] = 'javascript:alert(1)'
        result = self.read(data)
        self.assertIsNone(result['category']); self.assertFalse(result['links'])
        for purpose in ['business','study','work']:
            self.assertIsNone(self.read(context={**self.context,'purpose':purpose})['category'])
        data = deepcopy(self.data); data['destinations']['JP']['rows']['NG']['valid_until'] = '2026-10-16'
        self.assertIsNone(self.read(data,context={**self.context,'departure_date':'2026-10-17'})['category'])

    def test_missing_mapping_and_policy_scope(self):
        self.assertEqual(self.read(context={**self.context,'nationality':'Unknown'})['status'],'links_only')
        data = deepcopy(self.data); data['destinations']['JP']['rows']['NG']['evidence_level'] = 'destination-policy'
        self.assertTrue(any('destination-level' in item for item in self.read(data)['limitations']))

    def test_real_snapshot_is_loadable_and_attributed(self):
        result = lookup(self.context)
        self.assertIn(result['status'], {'links_only','dataset_reported'})
        self.assertEqual(result['license'],'CC-BY-4.0')
        self.assertEqual(len(result['commit']),40)
