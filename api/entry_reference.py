"""Conservative use of an independent compilation, with links-only fallbacks."""
from datetime import date, datetime, timezone
import json
import gzip
from pathlib import Path
from urllib.parse import urlsplit
from functools import lru_cache

SNAPSHOT = Path(__file__).resolve().parent / 'reference_data/entry_snapshot.json.gz'
CATEGORIES = {'visa-free':'Visa-free category', 'embassy-visa':'Visa application before travel',
    'visa-required':'Visa required category', 'evisa':'Electronic visa category', 'eta':'Travel authorisation category',
    'visa-on-arrival':'Visa on arrival category', 'freedom-of-movement':'Freedom of movement category',
    'banned':'Entry restriction reported', 'travel-permit':'Travel permit category'}

@lru_cache(maxsize=1)
def load_snapshot(modified):
    with gzip.open(SNAPSHOT, 'rt', encoding='utf-8') as stream:
        return json.load(stream)

def safe_link(url):
    if not isinstance(url,str): return False
    parsed = urlsplit(url)
    return parsed.scheme == 'https' and bool(parsed.hostname) and not parsed.username and not parsed.password

def source_link(source):
    if not isinstance(source,dict) or not safe_link(source.get('url')): return None
    try:
        checked = date.fromisoformat(source.get('lastVerified'))
        reported_date = checked.isoformat() if checked <= datetime.now(timezone.utc).date() else None
    except (TypeError,ValueError):
        reported_date = None
    return {'title':source.get('name') or urlsplit(source['url']).hostname, 'url':source['url'],
        'type':source.get('type','unknown'), 'publisher_checked_at':reported_date}

def lookup(context, snapshot=None, today=None):
    today = today or datetime.now(timezone.utc).date()
    result = {'status':'links_only','category':None,'category_label':None,'source':None,'links':[],
        'publisher_checked_at':None,'check_age_days':None,'evidence_level':None,
        'limitations':['Short-stay tourism reference only. Residence permits, existing visas, passport type, travel dates, and transit eligibility are not resolved.',
            'A publisher verification date is not an independent Restrictapp check or a guarantee that the rule still applies.'],
        'reason':'No usable passport-specific reference is available. Check the official authority.',
        'provider':'TravelRequirements.info','dataset_url':'https://travelrequirements.info/en/data/'}
    try:
        data = snapshot if snapshot is not None else load_snapshot(SNAPSHOT.stat().st_mtime_ns)
        result.update({key:data[key] for key in ['provider','publisher','version','commit','imported_at','license','license_url','attribution','dataset_url']})
        destination = data['destinations'].get(data['country_codes'].get(context.get('destination')))
        if not destination: return result
        result['links'] = [link for source in destination.get('primary_sources',[]) if (link:=source_link(source))]
        row = destination['rows'].get(data['country_codes'].get(context.get('nationality')))
        if not row: return result
        source = row.get('source',{})
        result['source'] = source_link(source)
        result['evidence_level'] = row.get('evidence_level')
        if result['source'] and result['source']['url'] not in {s['url'] for s in result['links']}:
            result['links'].insert(0,result['source'])
        try:
            checked = date.fromisoformat(source['lastVerified'])
        except (KeyError, TypeError, ValueError):
            result['reason'] = 'The source has no valid publisher verification date. Follow the authority links.'
            return result
        age = (today-checked).days
        if age < 0:
            result['reason'] = 'The source verification date is in the future; the category is withheld.'
            return result
        result['publisher_checked_at'] = checked.isoformat()
        result['check_age_days'] = age
        if context.get('purpose','tourism') != 'tourism':
            result['reason'] = 'This dataset adapter covers short-stay tourism, not your selected travel purpose.'
        elif any(source.get(flag) for flag in ['unverifiable','conflict','portalOnly']):
            flags = [name for key,name in [('unverifiable','source could not be re-read'),('conflict','conflicting source information'),('portalOnly','portal-only evidence')] if source.get(key)]
            result['reason'] = 'Category withheld: publisher flags '+', '.join(flags)+'.'
        elif age > 7:
            result['reason'] = 'Publisher check is older than seven days. Reconfirm with the authority; category withheld.'
        elif not result['source'] or source.get('type') not in {'government','igo'}:
            result['reason'] = 'No usable government or intergovernmental citation is recorded.'
        elif row.get('category') not in CATEGORIES:
            result['reason'] = 'The publisher has not confirmed a usable visa category for this passport.'
        elif row.get('valid_until') and date.fromisoformat(row['valid_until']) < (date.fromisoformat(context['departure_date']) if context.get('departure_date') else today):
            result['reason'] = 'The cited rule expires before departure, or has expired. Category withheld.'
        else:
            result.update(status='dataset_reported',category=row['category'],category_label=CATEGORIES[row['category']],
                reason='Baseline category reported by an independent dataset. Confirm its conditions and exceptions with the cited authority.')
            if row.get('notes'): result['limitations'].append(str(row['notes']))
        if result['evidence_level'] == 'destination-policy':
            result['limitations'].append('The publisher cites destination-level policy rather than supporting text for this specific passport row.')
        if destination.get('conditional_waivers_listed'):
            result['limitations'].append('The destination lists conditional waivers. They have not been evaluated for this traveler.')
        return result
    except (OSError, ValueError, KeyError, TypeError):
        result.update(status='links_only',category=None,category_label=None,reason='Reference data could not be validated. Use official guidance.')
        return result
