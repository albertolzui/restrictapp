"""Build a pinned, attributed reference snapshot; does not execute upstream code."""
import argparse
import ast
from collections import Counter
from datetime import datetime, timezone
import json
import gzip
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def build(source):
    site = json.loads((source / 'site.json').read_text(encoding='utf-8'))['dataset']
    if site['license']['spdx'] != 'CC-BY-4.0':
        raise ValueError('Unexpected dataset licence; review before importing')
    tree = ast.parse((ROOT / 'api/crawler_for_api_all_possible_trips.py').read_text(encoding='utf-8'))
    codes = next(ast.literal_eval(n.value) for n in ast.walk(tree) if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'origins_dict' for t in n.targets))
    countries = json.loads((ROOT / 'api/countries.json').read_text(encoding='utf-8'))
    codes = {country:codes[country] for country in countries if country in codes}
    destinations = {}
    counts = Counter()
    for file in sorted((source / 'destinations').glob('*.json')):
        doc = json.loads(file.read_text(encoding='utf-8'))
        policy = doc['visaPolicy']
        rows = {}
        for passport, row in policy['byPassport'].items():
            raw = row.get('source') or policy.get('defaultSource') or {}
            citation = {key:raw.get(key) for key in ['url','name','type','lastVerified','lastChanged','unverifiable','conflict','portalOnly'] if raw.get(key) is not None}
            rows[passport] = {'category':row['requirement'], 'source':citation,
                'evidence_level':'passport-row' if row.get('evidence') or row.get('quote') else 'destination-policy',
                'notes':row.get('notes'), 'valid_until':row.get('validUntil')}
            counts[row['requirement']] += 1
            for flag in ['unverifiable','conflict','portalOnly']:
                if raw.get(flag): counts[flag] += 1
        primary = [{key:s.get(key) for key in ['url','name','type','lastVerified']}
            for s in doc.get('meta',{}).get('primarySources',[])[:3]]
        destinations[doc['iso2']] = {'name':doc['names']['common'], 'slug':doc['id'], 'rows':rows, 'primary_sources':primary,
            'conditional_waivers_listed':bool(policy.get('conditionalWaivers'))}
    sha = subprocess.check_output(['git','-c',f'safe.directory={source.as_posix()}','-C',str(source),'rev-parse','HEAD'], text=True).strip()
    result = {'provider':'TravelRequirements.info', 'publisher':'AXG Sp. z o.o.', 'version':site['version'], 'commit':sha,
        'imported_at':datetime.now(timezone.utc).isoformat(), 'license':'CC-BY-4.0',
        'license_url':'https://creativecommons.org/licenses/by/4.0/', 'dataset_url':'https://travelrequirements.info/en/data/',
        'attribution':'TravelRequirements.info — Entry Requirements Dataset, AXG Sp. z o.o. (CC BY 4.0). Adapted by Restrictapp: selected fields and conservative display filters; not independently verified.',
        'country_codes':codes,'destinations':destinations,'audit_counts':dict(counts)}
    target = ROOT / 'api/reference_data'
    target.mkdir(exist_ok=True)
    temporary = target / 'entry_snapshot.tmp'
    temporary.write_bytes(gzip.compress(json.dumps(result,ensure_ascii=False,separators=(',',':')).encode('utf-8'),mtime=0))
    temporary.replace(target / 'entry_snapshot.json.gz')
    (target / 'LICENSE-TravelRequirements.txt').write_text((source/'LICENSE').read_text(encoding='utf-8'),encoding='utf-8')
    (target / 'NOTICE-TravelRequirements.md').write_text((source/'NOTICE.md').read_text(encoding='utf-8'),encoding='utf-8')
    print(json.dumps({'commit':sha,'destinations':len(destinations),'counts':dict(counts)},indent=2))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    build(parser.parse_args().source.resolve())
