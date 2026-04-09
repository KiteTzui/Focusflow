from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import bcrypt
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db import init_db
from api.config import CORS_ORIGINS
from api.models import User, Task, StudySession, Distraction

# Initialize database
init_db()

app = FastAPI(title="FocusFlow API", version="1.0.0")

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ PYDANTIC MODELS ============

class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserProfile(BaseModel):
    id: int
    username: str
    email: str
    level: str
    streak: int
    total_study_time: int
    tasks_completed: int
    daily_goal: int
    created_at: str

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "To Do"
    priority: str = "Medium"
    due_date: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[str] = None

class TaskResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    due_date: Optional[str]
    created_at: str
    updated_at: str

class StudySessionCreate(BaseModel):
    duration_seconds: int
    start_time: str
    end_time: str
    task_id: Optional[int] = None

class StudySessionResponse(BaseModel):
    id: int
    user_id: int
    task_id: Optional[int]
    duration_seconds: int
    start_time: str
    end_time: str
    created_at: str

class DistractionCreate(BaseModel):
    duration_seconds: int
    start_time: str
    end_time: str
    session_id: Optional[int] = None
    description: Optional[str] = None

class DistractionResponse(BaseModel):
    id: int
    user_id: int
    session_id: Optional[int]
    duration_seconds: int
    start_time: str
    end_time: str
    description: Optional[str]
    created_at: str

class DashboardStats(BaseModel):
    study_time: int
    completed_tasks: int
    distractions: int
    active_tasks: int

# ============ UTILITY FUNCTIONS ============

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode(), hashed.encode())

def format_user(user_dict) -> UserProfile:
    """Format user dict to response"""
    if not user_dict:
        return None
    return UserProfile(
        id=user_dict['id'],
        username=user_dict['username'],
        email=user_dict['email'],
        level=user_dict['level'],
        streak=user_dict['streak'],
        total_study_time=user_dict['total_study_time'],
        tasks_completed=user_dict['tasks_completed'],
        daily_goal=user_dict['daily_goal'],
        created_at=user_dict['created_at']
    )

# ============ AUTH ROUTES ============

@app.post("/api/auth/register")
async def register(user_data: UserRegister):
    """Register a new user"""
    # Check if username exists
    if User.get_by_username(user_data.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Check if email exists
    if User.get_by_email(user_data.email):
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Create user
    hashed_password = hash_password(user_data.password)
    user = User.create(user_data.username, user_data.email, hashed_password)
    
    if not user:
        raise HTTPException(status_code=500, detail="Error creating user")
    
    return {
        "message": "User registered successfully",
        "user_id": user['id'],
        "username": user['username']
    }

@app.post("/api/auth/login")
async def login(user_data: UserLogin):
    """Login user"""
    user = User.get_by_username(user_data.username)
    
    if not user or not verify_password(user_data.password, user['password']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {
        "message": "Login successful",
        "user_id": user['id'],
        "username": user['username'],
        "email": user['email']
    }

# ============ USER ROUTES ============

@app.get("/api/users/{user_id}")
async def get_user(user_id: int):
    """Get user profile"""
    user = User.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return format_user(user)

@app.put("/api/users/{user_id}")
async def update_user(user_id: int, updates: dict):
    """Update user profile"""
    if User.update_profile(user_id, **updates):
        user = User.get_by_id(user_id)
        return format_user(user)
    raise HTTPException(status_code=500, detail="Error updating user")

# ============ TASK ROUTES ============

@app.post("/api/tasks")
async def create_task(user_id: int, task: TaskCreate):
    """Create a new task"""
    new_task = Task.create(user_id, task.title, task.description, 
                          task.status, task.priority, task.due_date)
    if not new_task:
        raise HTTPException(status_code=500, detail="Error creating task")
    return new_task

@app.get("/api/tasks/{task_id}")
async def get_task(task_id: int):
    """Get task by ID"""
    task = Task.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.get("/api/users/{user_id}/tasks")
async def get_user_tasks(user_id: int, status: Optional[str] = None):
    """Get all tasks for a user"""
    tasks = Task.get_user_tasks(user_id, status)
    return {"tasks": tasks, "total": len(tasks)}

@app.put("/api/tasks/{task_id}")
async def update_task(task_id: int, task_update: TaskUpdate):
    """Update a task"""
    updates = task_update.dict(exclude_unset=True)
    if Task.update(task_id, **updates):
        return Task.get_by_id(task_id)
    raise HTTPException(status_code=500, detail="Error updating task")

@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: int):
    """Delete a task"""
    if Task.delete(task_id):
        return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")

# ============ STUDY SESSION ROUTES ============

@app.post("/api/study-sessions")
async def create_study_session(user_id: int, session: StudySessionCreate):
    """Create a new study session"""
    new_session = StudySession.create(user_id, session.duration_seconds,
                                     session.start_time, session.end_time, session.task_id)
    if not new_session:
        raise HTTPException(status_code=500, detail="Error creating session")
    return new_session

@app.get("/api/study-sessions/{session_id}")
async def get_study_session(session_id: int):
    """Get study session by ID"""
    session = StudySession.get_by_id(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@app.get("/api/users/{user_id}/study-sessions")
async def get_user_study_sessions(user_id: int):
    """Get recent study sessions for a user"""
    sessions = StudySession.get_user_sessions(user_id)
    total_time = StudySession.get_total_study_time(user_id)
    return {"sessions": sessions, "total_study_time": total_time}

# ============ DISTRACTION ROUTES ============

@app.post("/api/distractions")
async def create_distraction(user_id: int, distraction: DistractionCreate):
    """Create a new distraction record"""
    new_distraction = Distraction.create(user_id, distraction.duration_seconds,
                                        distraction.start_time, distraction.end_time,
                                        distraction.session_id, distraction.description)
    if not new_distraction:
        raise HTTPException(status_code=500, detail="Error creating distraction")
    return new_distraction

@app.get("/api/distractions/{distraction_id}")
async def get_distraction(distraction_id: int):
    """Get distraction by ID"""
    distraction = Distraction.get_by_id(distraction_id)
    if not distraction:
        raise HTTPException(status_code=404, detail="Distraction not found")
    return distraction

@app.get("/api/users/{user_id}/distractions")
async def get_user_distractions(user_id: int):
    """Get recent distractions for a user"""
    distractions = Distraction.get_user_distractions(user_id)
    total_distractions = Distraction.get_total_distractions(user_id)
    total_time = Distraction.get_total_distraction_time(user_id)
    return {
        "distractions": distractions,
        "total_count": total_distractions,
        "total_time": total_time
    }

# ============ DASHBOARD ROUTES ============

@app.get("/api/dashboard/{user_id}")
async def get_dashboard_stats(user_id: int):
    """Get dashboard statistics"""
    user = User.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    study_time = StudySession.get_total_study_time(user_id)
    completed_tasks = len(Task.get_user_tasks(user_id, "Done"))
    total_distractions = Distraction.get_total_distractions(user_id)
    active_tasks = len(Task.get_user_tasks(user_id, "Active"))
    
    return {
        "user": format_user(user),
        "study_time": study_time,
        "completed_tasks": completed_tasks,
        "distractions": total_distractions,
        "active_tasks": active_tasks
    }

# ============ HEALTH CHECK ============

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "FocusFlow API is running"}

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "FocusFlow API", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
