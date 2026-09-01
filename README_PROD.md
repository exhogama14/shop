# DiamondStore — Production Deployment Guide

This document explains how to run DiamondStore with a production WSGI server instead of Flask's built-in development server. Gunicorn is used on Linux; Hypercorn is used on Windows.

The Flask dev server (`flask run` / `app.run()`) is great for hacking on the project but **must not** be used in production — it is single-threaded, doesn't scale, lacks robust logging, and is not hardened.

---

## 1. Prerequisites

- Python 3.9 or newer
- A virtual environment (recommended)

```bash
python -m venv venv
# Linux / macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs Flask, Flask-SQLAlchemy, Flask-Login, Werkzeug, Gunicorn, and Hypercorn.

## 3. Configure Environment (REQUIRED in production)

Set these environment variables before starting Gunicorn:

| Variable       | Required | Default                  | Purpose                                                  |
|----------------|----------|--------------------------|----------------------------------------------------------|
| `SECRET_KEY`   | **YES**  | `diamond-store-secret-…` | Flask session signing key. **Change for production.**    |
| `DATABASE_URL` | no       | `sqlite:///site.db`      | Any SQLAlchemy URI (Postgres, MySQL, etc.)               |
| `PORT`         | no       | `8000`                   | Port Gunicorn listens on                                 |
| `WEB_CONCURRENCY` | no    | `(2 × CPU) + 1`          | Number of worker processes                               |
| `BIND`         | no       | `0.0.0.0:8000`           | Full bind address                                        |
| `LOG_LEVEL`    | no       | `info`                   | `debug`, `info`, `warning`, `error`, `critical`          |

Example:
```bash
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
export DATABASE_URL="postgresql://user:pass@localhost/diamondstore"
export PORT=8000
```

## 4. Run Gunicorn

### Quick start
```bash
gunicorn -c gunicorn_config.py wsgi:app
```

### Or use the helper script
```bash
./start.sh         # Linux / macOS
start.bat          # Windows (Hypercorn)
```

You should see:
```
💎 DiamondStore starting — bind=0.0.0.0:8000 workers=5
[INFO] Booting worker with pid: 12345
```

## 5. Behind a Reverse Proxy (recommended)

For HTTPS, rate limiting, static-asset caching, etc., put Gunicorn behind Nginx, Caddy, or a cloud load balancer.

Minimal Nginx snippet:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /static/ {
        alias /path/to/diamondstore/static/;
        expires 30d;
        access_log off;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 6. Windows

Gunicorn does not support Windows natively. Hypercorn supports this WSGI app on Windows:

```powershell
python -m hypercorn wsgi:app --bind=0.0.0.0:8000 --workers=2 --log-level=info --access-logfile=- --error-logfile=-
```

Or use the helper script:

```cmd
start.bat
```

WSL is another option if you specifically want to run Gunicorn on Windows.

## 7. Systemd Service (Linux servers)

`/etc/systemd/system/diamondstore.service`:
```ini
[Unit]
Description=DiamondStore Gunicorn
After=network.target

[Service]
User=diamondstore
WorkingDirectory=/opt/diamondstore
Environment="SECRET_KEY=your-secret-here"
Environment="DATABASE_URL=sqlite:///site.db"
ExecStart=/opt/diamondstore/venv/bin/gunicorn -c gunicorn_config.py wsgi:app
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now diamondstore
sudo systemctl status diamondstore
```

## 8. File Map

| File                  | Purpose                                        |
|-----------------------|------------------------------------------------|
| `wsgi.py`             | Production WSGI entry point — exposes `app`    |
| `gunicorn_config.py`  | Production config (workers, timeouts, logging)  |
| `requirements.txt`    | Pinned dependencies including `gunicorn`       |
| `start.sh`            | Convenience launcher (Unix)                    |
| `start.bat`           | Convenience launcher (Windows; uses Hypercorn)  |
| `Procfile`            | PaaS declaration (Heroku / Render / Fly.io)    |
| `app.py`              | **Unchanged** — still works with `python app.py` for local dev |

---

Happy shipping! 💎
