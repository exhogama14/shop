@echo off
REM DiamondStore - Production start script (Windows)
REM Usage:   start.bat
setlocal

cd /d "%~dp0"

if not defined PORT set PORT=8000
set BIND=0.0.0.0:%PORT%

echo ?? Starting DiamondStore (production mode)
echo    -^> bind:      %BIND%
echo    -^> workers:   %WEB_CONCURRENCY%
echo    -^> log level: %LOG_LEVEL%

REM gunicorn does not run natively on Windows; use waitress instead.
REM Install with: pip install waitress
where gunicorn >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    gunicorn -c gunicorn_config.py wsgi:app
) else (
    echo.
    echo [INFO] Gunicorn is Unix-only. Falling back to Waitress on Windows.
    echo        pip install waitress  (one-time)
    python -m waitress --listen=%BIND% wsgi:app
)

endlocal
