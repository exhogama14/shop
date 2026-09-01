@echo off
cd /d "%~dp0"
"%CD%\venv\Scripts\python.exe" -m waitress --listen=0.0.0.0:8000 app:app
