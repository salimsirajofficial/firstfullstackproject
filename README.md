Project split for Netlify frontend + backend API

Structure

- frontend/  -> static site to deploy to Netlify
  - index.html, register.html, login.html
  - static/css/*

- backend/  -> Flask API to host on Render, Railway, Fly, or similar
  - app.py  (POST /api/register)
  - requirements.txt, Procfile, Dockerfile

Deployment notes

- Frontend: deploy the `frontend/` folder to Netlify. Set environment variable `API_BASE` in the Netlify site (or edit `register.html` to set `const API_BASE = 'https://your-backend.example.com'`) so fetch points to your backend.

- Backend: choose a host (Render, Railway, Fly). This repo includes a `Dockerfile` and `Procfile` for easy deploy. Using SQLite (`registrations.db`) is preserved in this setup; consider switching to Postgres for production durability.

- Security: keep secrets out of the repo (use env vars). No OAuth is included (as requested).

Local testing

- Run backend locally (either directly or via the wrapper):
  - Option A (recommended):
    cd backend
    python app.py
  - Option B (convenience wrapper in project root):
    python app.py

- Set API base for the frontend at runtime:
  - For local testing in the browser console: run
    window.API_BASE = 'http://localhost:5000'
  - Or edit `frontend/static/js/env.js` to set `window.API_BASE` before deploying.

- Open `frontend/register.html` in your browser and submit the form; check backend logs to confirm the POST and the created record.

Netlify deployment notes

- Publish directory: set Netlify to publish the `frontend/` folder.
- Runtime API base: you can inject the remote API base by replacing `frontend/static/js/env.js` at build time. Example (Netlify build command):

  sed -i "s|window.API_BASE = window.API_BASE || '';|window.API_BASE = '${API_BASE}';|" frontend/static/js/env.js || true

  This will set `window.API_BASE` to the Netlify environment variable `API_BASE`.

- Alternatively, edit `frontend/static/js/env.js` in the repo (or set `window.API_BASE` in a small custom script) before deploy.

Production notes

- SQLite is fine for small projects, but consider Postgres for durability and when scaling. Use `DATABASE_URL` to point to a managed DB if you switch.
- Backend: use the provided `Procfile` for Heroku/Render or Dockerfile for container hosts. The backend already exposes `/api/health`, `/api/register`, and `/api/registrants`.

Next steps

- Add optional DB migration (Alembic) and add a managed DB if desired.
- Add tests and simple smoke checks.
- Remove or protect `frontend/admin.html` in production if needed.

