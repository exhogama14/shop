Write-Host "Activating virtual environment..." -ForegroundColor Cyan

# Activate venv
$venvPath = ".\venv\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    & $venvPath
    Write-Host "Virtual environment activated." -ForegroundColor Green
} else {
    Write-Host "ERROR: venv not found at $venvPath" -ForegroundColor Red
    exit 1
}

Write-Host "Starting Waitress server..." -ForegroundColor Cyan

waitress-serve --host=0.0.0.0 --port=8080 app:app

