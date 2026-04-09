# FocusFlow Backend Configuration

# Server Configuration
HOST = "0.0.0.0"
PORT = 8000
DEBUG = True
RELOAD = True

# Database Configuration
DATABASE_PATH = "../database/focusflow.db"

# Security Configuration
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# CORS Configuration
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8080"
]

# API Configuration
API_PREFIX = "/api"
API_VERSION = "1.0.0"

# Logging
LOG_LEVEL = "INFO"
