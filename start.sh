#!/bin/bash

# FocusFlow Application Startup Script for Mac/Linux

echo ""
echo "==============================================="
echo "  FocusFlow - Smart Study Task Tracker"
echo "  Starting Application..."
echo "==============================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

echo "[✓] Python found: $(python3 --version)"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "Error: Node.js is not installed"
    echo "Please install Node.js 14+ and try again"
    exit 1
fi

echo "[✓] Node.js found: $(node --version)"

echo ""
echo "[1/4] Initializing database..."
cd database
python3 db.py
if [ $? -ne 0 ]; then
    echo "Error: Database initialization failed"
    exit 1
fi
cd ..
echo "[✓] Database initialized successfully!"
echo ""

echo "[2/4] Installing backend dependencies..."
cd api
pip3 install -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install backend dependencies"
    exit 1
fi
cd ..
echo "[✓] Backend dependencies ready!"
echo ""

echo "[3/4] Installing frontend dependencies..."
cd frontend
npm install --silent
if [ $? -ne 0 ]; then
    echo "Error: Failed to install frontend dependencies"
    exit 1
fi
cd ..
echo "[✓] Frontend dependencies ready!"
echo ""

echo "==============================================="
echo "  Setup complete! Starting servers..."
echo "==============================================="
echo ""

echo "Starting FastAPI backend on http://localhost:8000"
echo "Starting Vite frontend on http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

# Start backend in background
echo "Starting backend..."
cd api
python3 main.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start frontend in new terminal (Mac) or same terminal (Linux)
echo "Starting frontend..."
cd frontend
if [[ "$OSTYPE" == "darwin"* ]]; then
    # Mac
    open -a Terminal "$(pwd)/npm run dev"
    npm run dev > /dev/null 2>&1 &
else
    # Linux
    npm run dev &
fi
FRONTEND_PID=$!
cd ..

echo ""
echo "✓ Application started successfully!"
echo ""
echo "Frontend: http://localhost:3000"
echo "Backend:  http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""

# Wait for processes
wait $BACKEND_PID $FRONTEND_PID
