# English and German

The interface supports `en` and `de`. A language selector is present on the planner, privacy/cookie page, and public offline page. First visit: explicit valid `?lang=en` / `?lang=de`, then this device's saved choice, then browser language, otherwise English. Language selection is saved locally as `restrictapp_language`; the privacy notice discloses this. Switching does not refresh the page. Signed-in changes save to users.preferred_language; login restores that preference unless a language was explicitly chosen on the current page. A one-year en/de cookie also lets server errors follow the selected language. See ERROR_HANDLING.md.

`api/static/app/de.json` contains reviewed German interface and app-generated planning messages. `privacy-de.json` contains the German privacy notice. English messages in the HTML/JavaScript are catalogue keys. After changing either catalogue, run:

```
python -m scripts.build_locales
```

Commit the generated `locale-data.js` too: it bundles the reviewed messages and ISO country codes, so the interface needs no translation service or external font. Country labels use `Intl.DisplayNames`, but requests and saved data retain the existing country identifiers. Both English and German country names are accepted. Dates use en-GB or de-DE. Country identifiers remain canonical in API/storage. API errors carry stable codes and reviewed English/German text selected by X-Restrictapp-Language, the preference cookie or Accept-Language. Raw account JSON exports preserve their original machine-readable keys and identifiers.

The app translates its own checklists, warnings, metadata, error messages, install instructions, downloadable preparation plans and privacy content. Government guidance, source names, publisher-supplied notes and custom travel feeds remain in their published language with an explicit original-language notice. They are not machine translated or presented as independently verified German immigration advice. External links may lead to pages in other languages.

Manifest metadata follows the selected language; both manifests share the same app identity and launch URL. The public offline cache includes only the reconnect page, mark and translation scripts. No accounts, routes, passport details or government advice are added to that cache. The offline cache version changed to v2; existing workers update through the normal browser lifecycle.

Checks:

```
npm install --prefix api/data/i18n-tools --no-save jsdom
node tests/test_i18n.cjs
node tests/test_install.cjs
node tests/test_pwa.cjs
python -m unittest discover -s tests -v
```

The jsdom dependency is for development tests only, under the ignored data directory; Render remains a Python deployment. DOM tests verify country IDs, form retention, language switching, plan/checklist rendering, downloads, dialogs, privacy and offline messages. They do not emulate mobile browser layout or OS installation. Check both languages visually on desktop and phone when browser inspection is available, especially longer German labels.
