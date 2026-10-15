# Active backend

Root AGENTS.md applies. main.py is the active app; old routers/scrapers are
historical. storage.py supports SQLite locally and PostgreSQL in deployment.
Use parameterized SQL, preserve ownership and cascade behavior, and add migration
compatibility for existing databases. Do not assume Django models or migrations
exist here. Keep source fetches fixed-country, bounded and honest on failure.
Update DOCUMENTATION.md's schema/API/workflows in the same commit as changes.
