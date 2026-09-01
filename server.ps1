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

Write-Host "Starting Hypercorn server..." -ForegroundColor Cyan

$port = if ($env:PORT) { $env:PORT } else { "8080" }
$workers = if ($env:WEB_CONCURRENCY) { $env:WEB_CONCURRENCY } else { "2" }
$logLevel = if ($env:LOG_LEVEL) { $env:LOG_LEVEL } else { "info" }

python -m hypercorn wsgi:app --bind="0.0.0.0:$port" --workers=$workers --log-level=$logLevel --access-logfile=- --error-logfile=-

