# Restrictapp 2 contributor instructions

Follow ERROR_HANDLING.md for every endpoint/browser change. Preserve HTTP statuses,
stable codes, safe EN/DE messages and request references. Never expose raw exceptions
or gateway HTML; preserve entered values and never automatically replay mutations.
Keep language preferences owner-scoped and test restoration after fresh login.

Read README.md, DOCUMENTATION.md and SECURITY_REVIEW.md before editing. This is
the live FastAPI/vanilla-JavaScript v2 repository, not the separate Django/React
v3 project. Inspect git status first and preserve unrelated user edits. Do not
modify sibling projects or import the historical MongoDB/credential modules.

Every commit must include meaningful updates to root DOCUMENTATION.md and README.md. Update
entities, relationships, workflows, API behavior, frontend navigation and user
expectations alongside code. For maintenance/docs-only work, record what was
reviewed and its impact in revision notes. Do not use whitespace-only edits.
Keep README concise; update affected instructions or its maintenance note every commit, and keep specialist guides accurate.

Run `python scripts/check_docs.py --staged` before committing. After inspecting
existing hooks, install the local guard with `git config core.hooksPath .githooks`.
CI checks commits from other clients too. Do not bypass the policy unless directed
by the user. Never claim pushed changes are live without checking deployment.

Use root requirements-lock.txt and api.main:app; api/requirements.txt is legacy.
Bind SQL parameters and scope account queries to the authenticated user. Preserve
same-origin writes, cookies, hashing/resource budgets, no-store APIs and deletion
reauthentication. Never commit/print .env, credentials, databases, real exports,
virtual environments, IDE data, screenshots or attachments unrelated to the task.
Use disposable databases in tests; production accounts are not test fixtures.

Preserve English/German, keyboard/mobile access and source provenance. App-owned
copy needs reviewed German text and a rebuilt locale bundle. External advice stays
in its published language. Preparation tasks do not establish entry eligibility.

Use relevant Python tests, language/install/service-worker checks and syntax/build
checks appropriate to the change. Report checks, skips, visual inspection limits,
deployment state and remaining work accurately. Documentation checks enforce a
changed file, not the truth or completeness of its prose.
