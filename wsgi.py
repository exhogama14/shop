"""
WSGI Entry Point for Gunicorn / Production Servers
---------------------------------------------------
This module exposes the Flask application instance as `app`.
It is the standard entry point for production WSGI servers
(Gunicorn, uWSGI, mod_wsgi, Waitress, etc.).

Usage with Gunicorn:
    gunicorn -c gunicorn_config.py wsgi:app

Environment variables consumed (set these in your hosting platform):
    SECRET_KEY       Flask session secret (REQUIRED in production)
    DATABASE_URL     SQLAlchemy URI (defaults to sqlite:///site.db)
    PORT             Listen port (default 8000)
"""
import os

# Ensure instance folder exists before app imports (SQLite needs it)
_INSTANCE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "instance")
os.makedirs(_INSTANCE_DIR, exist_ok=True)

from app import app  # noqa: E402  (the Flask instance)

if __name__ == "__main__":
    # Convenience for local production testing:
    #     python wsgi.py
    import argparse
    parser = argparse.ArgumentParser(description="Run DiamondStore in production mode (Gunicorn preferred).")
    parser.add_argument("--host", default=os.environ.get("HOST", "0.0.0.0"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8000")))
    args = parser.parse_args()
    print("[WSGI] Starting dev-WSGI server (use Gunicorn in production).")
    app.run(host=args.host, port=args.port, debug=False)
