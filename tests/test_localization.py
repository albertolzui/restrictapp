import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from api.planning import TASKS
from api.entry_reference import CATEGORIES

ROOT=Path(__file__).resolve().parents[1]/'api/static/app'

class LocalizationTests(unittest.TestCase):
    def setUp(self):
        self.messages=json.loads((ROOT/'de.json').read_text(encoding='utf-8'))
        self.messages.update(json.loads((ROOT/'privacy-de.json').read_text(encoding='utf-8')))

    def test_static_app_text_has_reviewed_translation(self):
        allowed={'Restrictapp','Restrictapp Admin','Chrome','Safari','Microsoft Edge','Android','iPhone & iPad','English','Deutsch','olanipekun_albert@live.com','restrictapp_session'}
        texts=[]
        class Text(HTMLParser):
            def __init__(self): super().__init__(); self.skip=0
            def handle_starttag(self,tag,attrs):
                if tag in {'script','style','code'}: self.skip+=1
                texts.extend(value.strip() for key,value in attrs if key in {'placeholder','aria-label','alt'} and value)
            def handle_endtag(self,tag):
                if tag in {'script','style','code'}: self.skip-=1
            def handle_data(self,data):
                if not self.skip and re.search('[A-Za-z]',data) and not re.search(r'\d+°',data):texts.append(data.strip())
        for page in ('index.html','privacy.html','offline.html'):
            Text().feed((ROOT/page).read_text(encoding='utf-8'))
        missing=set(texts)-allowed-self.messages.keys()
        self.assertEqual(missing,set())

    def test_checklists_categories_country_ids_and_bundle(self):
        for _,title,detail in TASKS:
            self.assertIn(title,self.messages); self.assertIn(detail,self.messages)
        for label in CATEGORIES.values():self.assertIn(label,self.messages)
        codes=json.loads((ROOT/'country-codes.json').read_text())
        countries=json.loads((ROOT.parents[1]/'countries.json').read_text())
        self.assertEqual(set(codes),set(countries))
        self.assertTrue(all(re.fullmatch('[A-Z]{2}',code) for code in codes.values()))
        bundle=(ROOT/'locale-data.js').read_text(encoding='utf-8')
        bundled=json.loads(bundle.split('window.RestrictappLocales = ',1)[1].split(';\nwindow.RestrictappCountryCodes',1)[0])
        self.assertEqual(bundled['de'],self.messages)
        for english,german in self.messages.items():
            self.assertEqual(set(re.findall(r'\{\d+\}',english)),set(re.findall(r'\{\d+\}',german)))
