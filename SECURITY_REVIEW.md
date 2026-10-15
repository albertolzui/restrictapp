# Security review — 15 October 2026

Target: active FastAPI 2 application, browser code, database access and deployment
configuration. Legacy MongoDB crawlers are not imported by the running app.
This is a targeted review, not a guarantee that every vulnerability is closed.

Fixed: missing script CSP and permissions/isolated-opener headers; oversized and
chunked request bodies before validation; Pydantic errors echoing submitted input;
missing-user login paths skipping password hashing; account existence revealed by
signup conflicts; unbounded active sessions per user; and browser citation URLs
without a final HTTPS/credential check. Signup now returns the same 202 response
for new/existing addresses and asks for sign-in. Existing sessions still work.

Existing controls retained and exercised: scrypt hashes, hashed session tokens,
HttpOnly/Secure production cookies, same-origin write headers and Origin checks,
SQL parameter binding, owner-scoped trips/profiles, reauthentication for deletion,
shared database authentication counters, no-store APIs, trusted Render hostnames,
and a public-assets-only service worker. Fetch Metadata now also rejects explicit
cross-site writes. Both auth counters already incremented correctly; no throttle
short-circuit bug was found.

Validation: Python regression/security tests, bilingual DOM tests and dependency
audit. The current lock file had no known advisories at review time. A tracked-file
scan for private keys, GitHub tokens and credential-bearing MongoDB URLs found no
matches; this is not a full Git-history secret audit. No production accounts were
created or modified during review.

Remaining deployment/release work: email ownership verification, password recovery,
MFA, provider secret rotation, backups/restore tests, retention and processor
agreements. Render's ingress is the trust boundary for its wildcard forwarded-proxy
configuration; do not reuse that setting on a directly reachable standalone server.
The legacy frontend requires inline styles, so CSP permits them while scripts remain
same-origin only. Restrictapp 3 uses a strict style policy and Django CSRF. The old
repository still contains unused historical modules; do not deploy them as entry
points. The new repository copies only explicitly selected active domain assets.
