# FocusFlow Backend Configuration

# Server Configuration
HOST = "0.0.0.0"
PORT = 8000
DEBUG = True
RELOAD = True

# Database Configuration
import os
DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'focusflow.db')

# Security Configuration
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# CORS Configuration
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8080",
    "https://*.vercel.app",
    os.getenv("FRONTEND_URL", "http://localhost:3000")
]

# API Configuration
API_PREFIX = "/api"
API_VERSION = "1.0.0"

# Logging
LOG_LEVEL = "INFO"
