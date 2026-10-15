# Phone installation

Restrictapp is a Progressive Web App served from the existing Render service. No app-store account, new hosting service or paid package is required.

- iPhone/iPad: open the public HTTPS address in Safari, choose Share → Add to Home Screen. Keep Open as Web App enabled if shown, then Add.
- Android: open in Chrome and tap Install app in the mobile header or footer. It opens the browser's native prompt directly when available; otherwise it shows Android instructions to use Chrome's menu → Install app / Add to Home screen. Browser wording and install eligibility vary.
- Installed instances open with the manifest's standalone display and the new logo. The Install app footer control is hidden when running standalone. Browser installation prompts occur only after a deliberate button press.

The app requires internet for all planning, guidance, login and account operations. Its service worker caches only the public reconnect page, SVG mark and translation scripts. It never caches API responses, account information, the planner page, or travel advice. Downloaded preparation plans are separate files requested explicitly by the user. The privacy notice describes the public Cache Storage entry. Browser site-data settings can clear it.

The worker is served from `/sw.js`, giving it root scope, with `Cache-Control: no-cache`. Navigations use the network; only a network failure falls back to the reconnect page. Error HTTP responses are not replaced by cached advice. Worker updates follow the browser's normal lifecycle; no forced page reload or skipWaiting interrupts forms. Bump the offline cache version when changing the reconnect page or its cached logo. Updates remove only older Restrictapp offline caches.

PNG icons at 180, 192 and 512 pixels derive from `restrictapp-mark.svg`. The square green background allows OS masking, and the glyph stays within the central safe area. To regenerate, run `node scripts/generate_app_icons.cjs` with Sharp installed locally, or set `RESTRICTAPP_SHARP_MODULE` to the installed Sharp module. This is a build-time helper, not a production dependency.

Checks: `python -m unittest discover -s tests -p test_pwa.py`, `node tests/test_pwa.cjs`, and JavaScript syntax checks. Confirm actual home-screen installation on a physical iPhone and Android phone; desktop viewport simulation cannot verify OS installation or iOS cookie sharing. A newly installed app may require signing in again. The installed icon is often cached by the OS; changing it later may require removing and reinstalling the app.

Sources: [Apple's installation instructions](https://support.apple.com/guide/iphone/iphea86e5236/ios), [web.dev manifest guide](https://web.dev/learn/pwa/web-app-manifest).
