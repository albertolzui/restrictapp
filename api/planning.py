"""Preparation actions are user tasks, never an automated entry clearance."""
from datetime import date

TASKS = [
    ('passport', 'Check your passport', 'Confirm the expiry date, blank pages, and destination-specific validity rules.'),
    ('visa', 'Confirm visa or travel authorisation', 'Check the official rules for your passport, residence, purpose, and length of stay. Apply if required.'),
    ('health', 'Review health and entry formalities', 'Check official health guidance and any arrival declarations for your dates.'),
    ('insurance', 'Review insurance and travel advisories', 'Read destination advisories and confirm that your insurance covers your itinerary and activities.'),
    ('documents', 'Prepare your departure documents', 'Keep your required approvals, booking details, and airline document checklist accessible.'),
    ('return', 'Check your return journey', 'Confirm your documents and permission to re-enter your country of residence.')
]

AUTHORITY_LINKS = {
    'Japan': [{'title':'Japan Ministry of Foreign Affairs — visa guidance', 'url':'https://www.mofa.go.jp/j_info/visit/visa/index.html'}],
    'Italy': [{'title':'Italian Ministry of Foreign Affairs — Visa for Italy', 'url':'https://vistoperitalia.esteri.it/'}],
    'United-Kingdom': [{'title':'UK government — check if you need a visa', 'url':'https://www.gov.uk/check-uk-visa'}]
}

def authority_links(context):
    links = [{**link, 'country':context['destination'], 'role':'Destination'} for link in AUTHORITY_LINKS.get(context['destination'], [])]
    if context.get('transit'):
        links += [{**link, 'country':context['transit'], 'role':'Transit'} for link in AUTHORITY_LINKS.get(context['transit'], [])]
    return links

def checklist(context):
    items = [{'id': key, 'title': title, 'detail': detail} for key, title, detail in TASKS]
    if context.get('transit'):
        items.insert(2, {'id':'transit', 'title':'Check your connection', 'detail':f"Review transit requirements in {context['transit'].replace('-', ' ')}, including whether you pass border control or change airports."})
    return items

def planning_notes(context):
    notes = []
    nationality = context.get('nationality')
    if nationality:
        notes.append(f"Your {nationality.replace('-', ' ')} passport is separate from your departure country. Official requirements must match your traveler details.")
    else:
        notes.append('Add your passport country to make your preparation plan more useful.')
    expiry = context.get('passport_expiry')
    end = context.get('return_date') or context.get('departure_date')
    if expiry and end and date.fromisoformat(expiry) < date.fromisoformat(end):
        notes.append('Your passport expires before this journey ends. Review renewal before booking; completing the checklist does not resolve this issue.')
    elif expiry:
        notes.append('A passport expiry date alone does not confirm compliance. Some destinations require additional validity beyond your stay.')
    if context.get('purpose') in {'work', 'study'}:
        notes.append('Work and study can require different permission from a tourist visit. Confirm the correct route with the destination authority.')
    return notes
