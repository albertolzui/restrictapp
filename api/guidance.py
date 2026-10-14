"""Official advisory content via the GOV.UK JSON API. No traveler data is sent."""
import json
import time
from datetime import datetime, timezone
from html.parser import HTMLParser
from threading import Lock
from urllib.request import Request, urlopen

SLUGS = {'United-States':'usa', 'United-Arab-Emirates':'united-arab-emirates',
    'The-Bahamas':'bahamas', 'Czech-Republic':'czechia', 'Ivory-Coast':'cote-d-ivoire',
    'East-Timor':'timor-leste', 'Republic-of-the-Congo':'congo', 'Brunei-Darussalam':'brunei',
    'Cape-Verde':'cape-verde', 'Palestinian-Territories':'the-occupied-palestinian-territories'}
_cache = {}
_lock = Lock()

class PlainText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in {'script', 'style'}:
            self.skip += 1
        if tag in {'p', 'li', 'h2', 'h3', 'br'}:
            self.parts.append('\n')
    def handle_endtag(self, tag):
        if tag in {'script', 'style'} and self.skip:
            self.skip -= 1
        if tag in {'p', 'li', 'h2', 'h3'}:
            self.parts.append('\n')
    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)
    def text(self):
        return '\n'.join(line.strip() for line in ''.join(self.parts).splitlines() if line.strip())

def fetch_document(slug):
    request = Request(f'https://www.gov.uk/api/content/foreign-travel-advice/{slug}',
        headers={'Accept':'application/json', 'User-Agent':'Restrictapp/2.0 travel-planning'})
    with urlopen(request, timeout=6) as response:
        raw = response.read(2_000_001)
    if len(raw) > 2_000_000:
        raise ValueError('Response exceeds limit')
    return json.loads(raw)

def official_guidance(destination):
    if destination == 'United-Kingdom':
        return {'status':'links_only', 'provider':'GOV.UK', 'scope':'UK entry guidance; eligibility depends on nationality and status.',
            'url':'https://www.gov.uk/uk-border-control', 'updated_at':None, 'retrieved_at':None, 'sections':[]}
    slug = SLUGS.get(destination, destination.lower())
    # Destination is validated against the country catalog by the API layer.
    fallback = {'status':'unavailable', 'provider':'FCDO / GOV.UK',
        'scope':'UK government travel advice. Entry guidance is generally for British citizen passport holders; it does not establish eligibility for other passports.',
        'url':'https://www.gov.uk/foreign-travel-advice', 'updated_at':None, 'retrieved_at':None, 'sections':[]}
    with _lock:
        cached = _cache.get(slug)
        if cached and time.monotonic()-cached[0] < (3600 if cached[1]['status']=='available' else 60):
            return cached[1]
        try:
            document = fetch_document(slug)
            if document.get('document_type') != 'travel_advice' or document.get('base_path') != f'/foreign-travel-advice/{slug}':
                raise ValueError('Unexpected advice document')
            sections = []
            for part in document.get('details', {}).get('parts', []):
                if part.get('slug') in {'warnings-and-insurance', 'entry-requirements', 'safety-and-security', 'health'}:
                    parser = PlainText()
                    parser.feed(part['body'])
                    sections.append({'title':part['title'], 'slug':part['slug'], 'text':parser.text(),
                        'url':f'https://www.gov.uk/foreign-travel-advice/{slug}/{part["slug"]}'})
            if not sections:
                raise ValueError('Missing advice sections')
            result = {**fallback, 'status':'available', 'url':f'https://www.gov.uk/foreign-travel-advice/{slug}',
                'sections':sections, 'updated_at':document.get('public_updated_at'),
                'retrieved_at':datetime.now(timezone.utc).isoformat()}
        except (OSError, ValueError, TypeError, KeyError):
            result = fallback
        _cache[slug] = (time.monotonic(), result)
        return result
