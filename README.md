# Hostel Management System (Flask + SQLite)

This repository contains a small but scalable hostel management system built with Flask and SQLAlchemy. It is configured for an initial scale of 100 students and is easy to migrate to PostgreSQL/MySQL for larger deployments.

Quick start (macOS / zsh):

1. Create and activate a virtualenv (recommended):
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Seed the database (creates `hostel.db`):
```bash
python seed.py
```

4. Run the app:
```bash
python app.py
```

Open http://127.0.0.1:5000 in your browser.

Notes:
- To use PostgreSQL, set `DATABASE_URL` environment variable (e.g. `postgresql://user:pass@host/dbname`).
- The UI is Bootstrap-based and simple; replace templates in `templates/` for a richer portal or integrate a React/Next frontend.
# managmentsystem