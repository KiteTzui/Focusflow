@echo off
REM FocusFlow Application Startup Script for Windows

echo.
echo ===============================================
echo   FocusFlow - Smart Study Task Tracker
echo   Starting Application...
echo ===============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Node.js is not installed or not in PATH
    echo Please install Node.js 14+ and try again
    pause
    exit /b 1
)

echo [1/4] Checking dependencies...
echo.

REM Initialize database
echo [2/4] Initializing database...
cd database
python db.py
if %errorlevel% neq 0 (
    echo Error: Database initialization failed
    cd ..
    pause
    exit /b 1
)
cd ..
echo Database initialized successfully!
echo.

REM Install backend dependencies
echo [3/4] Installing/updating backend dependencies...
cd api
python -m pip install -q -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install backend dependencies
    cd ..
    pause
    exit /b 1
)
cd ..
echo Backend dependencies ready!
echo.

REM Install frontend dependencies
echo [4/4] Installing/updating frontend dependencies...
cd frontend
call npm install --silent
if %errorlevel% neq 0 (
    echo Error: Failed to install frontend dependencies
    cd ..
    pause
    exit /b 1
)
cd ..
echo Frontend dependencies ready!
echo.

echo ===============================================
echo   Setup complete! Starting servers...
echo ===============================================
echo.
echo Starting FastAPI backend on http://localhost:8000
echo Starting Vite frontend on http://localhost:3000
echo.
echo Press Ctrl+C in either terminal to stop the application
echo.

REM Start backend in a new window
start "FocusFlow Backend" cmd /k "cd api && python main.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak

REM Start frontend in a new window
start "FocusFlow Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ✓ Application started successfully!
echo.
echo Frontend: http://localhost:3000
echo Backend: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
pause
