#!/usr/bin/env pwsh

# FocusFlow Application Startup Script for PowerShell

Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  FocusFlow - Smart Study Task Tracker" -ForegroundColor Green
Write-Host "  Starting Application..." -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[✓] Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[✗] Error: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ and try again" -ForegroundColor Yellow
    exit 1
}

# Check Node.js
try {
    $nodeVersion = node --version 2>&1
    Write-Host "[✓] Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "[✗] Error: Node.js is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Node.js 14+ and try again" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "[1/4] Initializing database..." -ForegroundColor Cyan
Push-Location database
python db.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "[✗] Database initialization failed" -ForegroundColor Red
    Pop-Location
    exit 1
}
Pop-Location
Write-Host "[✓] Database initialized successfully!" -ForegroundColor Green
Write-Host ""

Write-Host "[2/4] Installing backend dependencies..." -ForegroundColor Cyan
Push-Location api
pip install -q -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "[✗] Failed to install backend dependencies" -ForegroundColor Red
    Pop-Location
    exit 1
}
Pop-Location
Write-Host "[✓] Backend dependencies ready!" -ForegroundColor Green
Write-Host ""

Write-Host "[3/4] Installing frontend dependencies..." -ForegroundColor Cyan
Push-Location frontend
npm install --silent
if ($LASTEXITCODE -ne 0) {
    Write-Host "[✗] Failed to install frontend dependencies" -ForegroundColor Red
    Pop-Location
    exit 1
}
Pop-Location
Write-Host "[✓] Frontend dependencies ready!" -ForegroundColor Green
Write-Host ""

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  Setup complete! Starting servers..." -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Starting FastAPI backend..." -ForegroundColor Yellow
Write-Host "Starting Vite frontend..." -ForegroundColor Yellow
Write-Host ""

# Start backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd $(Get-Location)\api; python main.py" -WindowStyle Normal

# Wait for backend to start
Start-Sleep -Seconds 3

# Start frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd $(Get-Location)\frontend; npm run dev" -WindowStyle Normal

Write-Host ""
Write-Host "✓ Application started successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C in either terminal to stop the application" -ForegroundColor Yellow
Write-Host ""
