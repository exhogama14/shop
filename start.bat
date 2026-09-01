@echo off
REM DiamondStore - Production start script (Windows)
REM Usage:   start.bat
setlocal

cd /d "%~dp0"

if not defined PORT set PORT=8000
if not defined WEB_CONCURRENCY set WEB_CONCURRENCY=2
if not defined LOG_LEVEL set LOG_LEVEL=info
set BIND=0.0.0.0:%PORT%

echo Starting DiamondStore (production mode)
echo    -^> bind:      %BIND%
echo    -^> workers:   %WEB_CONCURRENCY%
echo    -^> log level: %LOG_LEVEL%

REM Hypercorn supports WSGI applications and runs natively on Windows.
python -m hypercorn wsgi:app --bind=%BIND% --workers=%WEB_CONCURRENCY% --log-level=%LOG_LEVEL% --access-logfile=- --error-logfile=-
if errorlevel 1 (
    echo.
    echo [ERROR] Hypercorn could not start.
    echo         Run: pip install -r requirements.txt
    exit /b 1
)

endlocal
