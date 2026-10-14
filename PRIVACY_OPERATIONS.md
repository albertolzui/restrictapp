# Privacy operations

This implementation supports privacy obligations; it is not a certification of GDPR compliance.

Operator: Albert Olanipekun. Privacy contact: olanipekun_albert@live.com.
Optional Render environment overrides: `RESTRICTAPP_OPERATOR_NAME` and `RESTRICTAPP_PRIVACY_EMAIL`. Keep the HTML fallback notice in sync when changing these.

Before describing the deployment as compliant:

- Confirm and record the actual Render and Neon regions, processor agreements, subprocessors and international transfer safeguards. Frankfurt in the blueprint does not prove the Neon region or that all support and subprocessor processing stays in the EEA.
- Record exact provider log and backup retention periods. Update the privacy notice with these once confirmed. Avoid logging request bodies, passwords, session cookies, or export contents. Review provider access-log settings.
- Maintain a register of privacy requests and deleted accounts outside the public repository. If restoring a backup, reapply deletions before serving users. Do not promise immediate removal from all backups.
- Process access, rectification, restriction, objection, portability and erasure requests through the public privacy email, normally within one month. Verify identity proportionately; do not ask for passport scans by default. The UI handles exports and deletion, but email changes and restriction requests currently require operator action.
- Review whether an inactivity retention policy is appropriate, then implement and disclose it. There is currently no automatic inactive-account deletion.
- Periodically delete expired sessions and authentication counters if the app is inactive: cleanup currently runs on subsequent relevant requests, not a scheduled timer.
- Document the legitimate-interest assessment for security counters, keep processor records, and establish a breach-response procedure, including the GDPR's notification requirements where applicable.
- Audit actual browser cookies and network requests after every hosting or frontend change. The application code has no analytics, ad pixels, embeds or external fonts. Provider-added technologies are outside that code audit.
- Before adding any optional tracking, implement prior consent, equally accessible refusal and withdrawal, and update the notice. Closing the current essential-cookie information panel is not tracking consent.

Account deletion requires an authenticated session, CSRF safeguards and the current password; foreign-key cascades delete the user's active sessions, profile, trips and checklist rows. Temporary pseudonymous security counters may persist until cleanup. Account JSON exports omit hashes and session tokens. Tests exercise these properties against an isolated database, never live user accounts.

Reference: https://eur-lex.europa.eu/eli/reg/2016/679 and https://ico.org.uk/for-organisations/advice-for-small-organisations/privacy-notices-and-cookies/cookies-and-privacy-notices-in-detail/
