# Restrictapp 2.0

Read the [complete application documentation](DOCUMENTATION.md) for entities,
relationships, API contracts, workflows and frontend navigation. Contributor/AI
instructions are in [AGENTS.md](AGENTS.md). Every commit must update both DOCUMENTATION.md and README.md;
install the local guard with `git config core.hooksPath .githooks`.

A refreshed travel planning workspace built with FastAPI and a responsive HTML/CSS/JavaScript frontend.

English/German preferences now persist to signed-in accounts and restore at login.
API, network and gateway failures use safe localized messages while preserving
entered values. Contributors must follow [the error handling guide](ERROR_HANDLING.md).

For Render + Neon, follow [the deployment guide](DEPLOYMENT.md). Production uses PostgreSQL through `DATABASE_URL`; local development continues to use SQLite. The root `render.yaml` configures one free Render service and accepts a separately created Neon database.

## Run locally

From the repository root, using Python 3.12 or newer:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe -m uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
```

Open http://127.0.0.1:8000. No MongoDB account or credentials file is needed.

## What works

- Country search with the original country catalog, route validation, and origin/destination swapping.
- Traveler profiles separate nationality and residence from departure country. Optional passport expiry, dates, purpose, and one transit stop shape a preparation plan.
- Per-trip checklists persist completed checks; changing traveler or itinerary details resets progress. Completion is self-reported and does not confirm eligibility.
- Downloadable preparation plans and curated destination/transit visa-authority links for Japan, Italy, and the UK.
- Live FCDO advisories from the official GOV.UK Content API, labeled with British-passport scope, publication dates, retrieval dates, and Open Government Licence attribution.
- Destination shortcuts and a responsive travel workspace.
- Email/password signup and sign-in, scrypt password hashes, expiring opaque sessions, HttpOnly cookies, and cross-site write protection.
- Persistent saved trips with account ownership enforced on the server and duplicate prevention.
- Sourced travel requirements with check dates and stale-data labeling when a feed is configured.
- Explicit unavailable-data states when a route has no sourced information.
- Passport-based tourism reference categories from an attributed TravelRequirements.info snapshot, with publisher check dates, evidence scope, and links-only fallbacks for flagged or stale records. See [source evaluation](SOURCE_EVALUATION.md).

SQLite data lives in `api/data/restrictapp.sqlite3`, ignored by Git. Set `RESTRICTAPP_DB` to change the location. Back up the database for durable deployments.

## Travel data

**No personalized travel requirements provider is connected.** Official destination guidance is fetched from the public GOV.UK Content API when requested. It provides entry, safety, health, and advisory sections; it is not a visa eligibility engine for every nationality. Destination cards are inspiration, not claims of entry eligibility. The old COVID scraper is retained as reference and is not executed by the new application.

The guidance adapter sends only the destination slug to GOV.UK, never passport, residence, dates, or account details. Successful responses are cached in memory for one hour, failures for one minute. Requests have a six-second timeout and a response size limit. Unsupported countries, unavailable networks, and unexpected document formats fall back to the official advice directory without invented content. Country slug mappings may need extensions for less common territories. Source update time is distinct from retrieval time. The local app process needs outbound HTTPS access for live guidance.

Saved profiles require an account. Guest traveler details and checklist checks are held in page memory and disappear on refresh. Saved trips store a snapshot of traveler details so subsequent profile changes do not silently change an existing trip. Legacy saved routes without profiles still appear and can be upgraded by adding traveler details. The SQLite schema upgrades existing local version-2 databases in place.

Set `RESTRICTAPP_TRAVEL_FEED` to an absolute path to a UTF-8 JSON array maintained by a trusted data pipeline. Each record has this shape (the following is a schema example, not real travel advice):

```json
[
  {
    "origin": "Germany",
    "destination": "Japan",
    "checked_at": "2026-01-01T12:00:00Z",
    "summary": "Replace with reviewed, sourced information and its traveler scope.",
    "requirements": [
      {"title": "Requirement category", "detail": "Reviewed requirement text, including passport and residency scope."}
    ],
    "sources": [
      {"title": "Official authority", "url": "https://example.com/replace-with-official-source"}
    ]
  }
]
```

Use catalog identifiers, e.g. `United-Kingdom`. Checks must include a timezone; future timestamps, unsafe source URLs, malformed records, and missing sources are rejected. Records older than 24 hours are labeled stale. The adapter only validates the record format; the data owner must verify source authority, content, and freshness. Traveler details personalize the preparation plan, but the feed adapter does not resolve legal eligibility by nationality, residence, transit, or dates.

## Personalized provider evaluation

IATA Timatic and Sherpa both offer maintained requirements integrations. Evaluate coverage for nationality plus residence and multi-segment itineraries, source freshness, exception handling, API/widget terms, permitted caching/display, cost, and a sandbox before selecting a provider. No commercial contract, API account, or purchase has been initiated. The guest planning API is `POST /api/plan`; guidance is fetched separately so a provider outage does not prevent creating a checklist.

Future work: provider-backed eligibility, change alerts for saved trips, multi-traveler and multi-stop support, and broader curated visa-authority coverage. No scheduled monitoring or outbound notifications are enabled.

## Tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
node --check api/static/app/app.js
```

The tests use temporary databases and fixtures, never production travel advice or user accounts.

## Deployment and legacy code

The active entry point is `api.main:app` from the repository root. `api/legacy_main.py`, old templates, routers, and scrapers remain for reference; the new app does not import their missing credential dependencies. `api/requirements.txt` describes the legacy app; use the root requirements for version 2.

Existing MongoDB users and saved trips are not migrated automatically. Migration needs a separate reviewed process and password reset flow; plaintext passwords must not be carried into the new database.

Deployment preparation includes PostgreSQL storage, database health checks, HTTPS cookie configuration, security headers, Host validation, and persistent login/signup rate limiting. Email verification, account recovery, and a personalized requirements provider remain future work. The API exposes no legacy account or trip mutations through GET requests. Migration of the current SQLite data is available; legacy MongoDB users still need a separate password-reset migration.

The frontend uses local/system fonts without external font requests. All illustrations are CSS and require no third-party image downloads.

## English and German

Use the English/Deutsch selector to change the interface without losing the current route or checklist. German country names are accepted while saved identifiers remain unchanged. The privacy, install and offline pages and downloadable plans are localized too. External source text stays in its published language and is labelled as such. See [localization maintenance and tests](LOCALIZATION.md).
