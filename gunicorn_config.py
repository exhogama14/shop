"""
Gunicorn Production Configuration
---------------------------------
Run with:
    gunicorn -c gunicorn_config.py wsgi:app

All values can be overridden via environment variables — useful for
container platforms (Docker, Render, Fly.io, Railway, Heroku, etc.).
"""
import multiprocessing
import os

# ---------- Bind / Network ----------
# Override with: BIND="0.0.0.0:8000"
bind = os.environ.get("BIND", "0.0.0.0:8000")

# ---------- Worker Model ----------
# Recommended formula: (2 x CPU cores) + 1
# Override with: WEB_CONCURRENCY=4
workers = int(os.environ.get("WEB_CONCURRENCY", multiprocessing.cpu_count() * 2 + 1))
worker_class = os.environ.get("WORKER_CLASS", "sync")   # sync|gthread|gevent
# Threads only used if worker_class is gthread:
threads = int(os.environ.get("THREADS", "2"))

# ---------- Worker Behavior ----------
# Restart workers after this many requests (defends against memory leaks)
max_requests = int(os.environ.get("MAX_REQUESTS", "1000"))
max_requests_jitter = int(os.environ.get("MAX_REQUESTS_JITTER", "100"))

# Graceful timeout for worker shutdown
graceful_timeout = int(os.environ.get("GRACEFUL_TIMEOUT", "30"))
# Per-request timeout in seconds (sync workers block here)
timeout = int(os.environ.get("TIMEOUT", "60"))
# Keep-alive for HTTP/1.1 connections
keepalive = int(os.environ.get("KEEPALIVE", "5"))

# ---------- Preload ----------
# Load app before fork — saves memory but disables in-process state sharing.
# Safe for this app since it's stateless across workers.
preload_app = os.environ.get("PRELOAD_APP", "true").lower() == "true"

# ---------- Security ----------
# Don't allow privileged ports in config; require them via env.
# umask: files written by gunicorn get 0o640
umask = 0o077

# ---------- Logging ----------
accesslog = os.environ.get("ACCESS_LOG", "-")        # "-" = stdout
errorlog = os.environ.get("ERROR_LOG", "-")          # "-" = stderr
loglevel = os.environ.get("LOG_LEVEL", "info")
access_log_format = (
    '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s '
    '"%(f)s" "%(a)s" %(L)s'
)

# ---------- Process Naming ----------
proc_name = os.environ.get("PROC_NAME", "diamondstore")

# ---------- Server Hooks ----------
def on_starting(server):
    server.log.info("💎 DiamondStore starting — bind=%s workers=%s", bind, workers)

def post_fork(server, worker):
    server.log.info("Worker spawned (pid=%s)", worker.pid)

def worker_int(worker):
    worker.log.info("Worker received SIGINT — graceful shutdown")

def worker_abort(worker):
    worker.log.warning("Worker aborted (pid=%s)", worker.pid)
