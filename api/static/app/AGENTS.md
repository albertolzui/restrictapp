# Browser interface

Root and api/AGENTS.md apply. Use app.js for planner/account state, i18n.js for
language behavior and install.js for installation. Render untrusted text through
textContent; pass citation URLs through safeSource. Never cache private API data.
Preserve canonical country IDs, state across language switches, focus, keyboard
controls and mobile layout. Rebuild locale-data.js after catalog changes. Keep
offline, install, privacy and source limitations accurate. Update root
DOCUMENTATION.md for changes to navigation, dialogs, storage or workflows.
# Recovery and account language

Follow ../../../ERROR_HANDLING.md. Centralize requests and handle HTML gateways,
offline failures and timeouts with reviewed EN/DE copy. Retain entered values;
never replay mutations automatically. Serialize language preference saves and
explain failed account saves honestly. Keep printed privacy contacts on fetch
failure. Rebuild generated locale/error bundles after catalogue edits.
