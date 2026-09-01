# DiamondStore

DiamondStore is a Python Flask storefront with a shopping cart, checkout form, user login/registration, and admin panel.

## Project overview

- Frontend: Flask templates + static CSS/JS
- Backend: Flask + SQLAlchemy + Flask-Login
- Database: SQLite by default
- Run mode: local development via Flask or production via Waitress/Gunicorn

## Requirements

- Python 3.9+
- pip

## Setup

1. Open a terminal in this folder.
2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate it:

Windows PowerShell:
```powershell
venv\Scripts\Activate.ps1
```

Windows Command Prompt:
```cmd
venv\Scripts\activate.bat
```

Linux/macOS:
```bash
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run locally

Start the app in development mode:

```bash
python app.py
```

Then open:

```text
http://localhost:5000
```

## Production / hosted run

This project includes a production-ready WSGI entry point in `wsgi.py` and config in `gunicorn_config.py`.

### With Gunicorn

```bash
gunicorn -c gunicorn_config.py wsgi:app
```

### With Waitress on Windows

```bash
waitress-serve --listen=0.0.0.0:8000 wsgi:app
```

## Important app behavior

- The checkout form currently submits and redirects to the payment failure page.
- This is intentional for the storefront flow and is handled in the app route for `/checkout`.
- Do not change the checkout data flow unless you intend to rework payment logic.

## Default admin user

The app creates an admin account automatically:

- Username: `exhog`
- Password: `root`

## Useful commands

Create the database tables:

```bash
python -c "from app import app, db; db.create_all()"
```

Run a simple server:

```bash
python app.py
```

## Project files

- `app.py` — Flask app and routes
- `wsgi.py` — WSGI entry point
- `gunicorn_config.py` — production server config
- `templates/` — HTML pages
- `static/` — CSS, JS, images
- `instance/` — local database and generated data

## Cleanup note

This project was simplified and unnecessary build or temporary files were removed where possible to keep the workspace cleaner.
