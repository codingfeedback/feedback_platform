$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$Backend = Join-Path $Root "backend"

Set-Location $Backend

Write-Host ""
Write-Host "Feedback Platform local server"
Write-Host "Local: http://127.0.0.1:8000/"
Write-Host "App:   http://127.0.0.1:8000/app/"
Write-Host ""
Write-Host "Keep this window open while testing. Press Ctrl+C to stop."
Write-Host ""

python manage.py runserver 127.0.0.1:8000
