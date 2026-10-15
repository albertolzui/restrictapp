# Errors and language preferences

This is the v2 FastAPI/JavaScript contract. Keep it in sync with implementation,
README.md and DOCUMENTATION.md in every affected commit.

## Backend contract

`shared/error-messages.json` owns reviewed English/German error messages and stable
codes. `shared/errors.py` wraps the complete ASGI application, including routing
and unexpected exceptions. Preserve the actual HTTP status: an error is never a
successful 200 response. The JSON envelope is `{detail, error: {code, status,
request_id, retryable}}`. Set Content-Language, Cache-Control: no-store and
X-Request-ID; preserve security headers, Allow and Retry-After where applicable.
Never return exception strings, SQL, credentials, submitted passwords or raw
gateway HTML. Log request IDs and exception types without sensitive values.
Database connection failures return 503. Unexpected failures return 500.

Language priority is valid X-Restrictapp-Language, preference cookie, supported
Accept-Language, then English. Browser requests send their selected language.
Account preference is restored by the frontend after authentication. Add reviewed
messages in both languages and exercise EN/DE failure paths when adding endpoints.

## Browser recovery

Use the central api() helper: it handles JSON errors, HTML gateway responses,
offline failures and a 20-second timeout with safe localized messages. Preserve
entered values, release loading controls, and never automatically replay account,
trip, deletion or other mutations. Offer explicit retry of reads where useful.
Retain existing saved-trip rows when refresh fails. Privacy pages retain their
printed operator/contact details if dynamic contact loading fails.

A Render ingress outage, stopped service or DNS failure happens outside this
application. It cannot replace a provider-owned error document. The loaded
frontend can handle a failed request; recovery of the infrastructure itself
requires hosting controls. Do not promise uninterrupted service or universal
custom 502 pages. V3 has its own Nginx recovery implementation and guide.

## Preferred language

`users.preferred_language` is en/de, defaults to en and is separate from traveler
profile data. GET/PUT /api/preferences requires authentication; PUT uses existing
same-origin write protection and owner-scoped SQL. Login/session/export include
the preference. Existing SQLite/PostgreSQL databases receive an additive column;
the migration helper preserves it or defaults older source records to English.

Selectors remember the device choice and save it to signed-in accounts. Sign-in
restores the account preference unless the user explicitly selected a language
on the current page. Serialize saves and invalidate queued writes on logout.
Failed saves explain that the choice remains on this device. A nonidentifying
en/de cookie lasts one year, uses SameSite=Lax and Secure on HTTPS, and is disclosed
in the privacy notice. Account deletion removes the account preference; browser
site-data controls clear device storage.

## Contributor checks

Run `python scripts/build_locales.py` after catalogue changes; commit the generated
locale-data.js and error-messages.js. Run Python regression tests and
`node tests/test_i18n.cjs`; retain install/service-worker checks when touching their
contracts. Cover unknown exceptions, unavailable databases, malformed/upstream
errors, language restoration and authenticated preference validation. Use only
disposable accounts/databases. Update both root documentation files every commit.
