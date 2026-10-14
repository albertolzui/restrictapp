"""Read an explicitly configured travel feed; never turn missing data into clearance."""
import json
import os
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.parse import urlsplit


def route_data(origin, destination):
    unavailable = {'origin': origin, 'destination': destination, 'status': 'unverified',
        'checked_at': None, 'requirements': [], 'sources': [],
        'message': 'Verified entry requirements are not available for this route yet. Check the destination’s official immigration authority before booking.'}
    path = os.getenv('RESTRICTAPP_TRAVEL_FEED')
    if not path:
        return unavailable
    try:
        records = json.loads(Path(path).read_text(encoding='utf-8'))
        record = next((r for r in records if r['origin'] == origin and r['destination'] == destination), None)
        if not record:
            return unavailable
        checked = datetime.fromisoformat(record['checked_at'].replace('Z', '+00:00'))
        if checked.tzinfo is None or checked > datetime.now(timezone.utc):
            return unavailable
        sources = record['sources']
        requirements = record['requirements']
        if not sources or not requirements or not isinstance(record['summary'], str):
            return unavailable
        for source in sources:
            url = urlsplit(source['url'])
            if url.scheme != 'https' or not url.hostname or url.username or not isinstance(source['title'], str):
                return unavailable
        if any(not isinstance(item['title'], str) or not isinstance(item['detail'], str) for item in requirements):
            return unavailable
        stale = datetime.now(timezone.utc) - checked > timedelta(hours=24)
        return {**unavailable, 'status': 'stale' if stale else 'sourced', 'checked_at': checked.isoformat(),
            'requirements': requirements, 'sources': sources, 'message': record['summary']}
    except (OSError, ValueError, KeyError, TypeError):
        return unavailable
