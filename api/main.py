from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta
import bcrypt
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db import init_db
from api.config import CORS_ORIGINS, ALLOW_ORIGIN_REGEX
from api.models import User, Task, StudySession, Distraction

# Initialize database
init_db()

app = FastAPI(title="FocusFlow API", version="1.0.0")

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_origin_regex=ALLOW_ORIGIN_REGEX,
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
    points: int = 0
    selected_border: Optional[str] = None
    owned_borders: Optional[str] = None
    last_check_in: Optional[str] = None
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

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    level: Optional[str] = None
    streak: Optional[int] = None
    total_study_time: Optional[int] = None
    tasks_completed: Optional[int] = None
    daily_goal: Optional[int] = None
    points: Optional[int] = None
    selected_border: Optional[str] = None
    owned_borders: Optional[str] = None
    last_check_in: Optional[str] = None
    last_goal_reward_date: Optional[str] = None

class PurchaseItem(BaseModel):
    item_id: str

class SelectBorder(BaseModel):
    item_id: str

# ============ UTILITY FUNCTIONS ============

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode(), hashed.encode())

BORDER_ITEMS = [
    {
        'id': 'blue-glow',
        'name': 'Ocean Glow',
        'cost': 30,
        'css': 'border-blue',
        'description': 'A cool blue glow for your profile avatar.'
    },
    {
        'id': 'gold-ring',
        'name': 'Golden Ring',
        'cost': 60,
        'css': 'border-gold',
        'description': 'A premium golden frame for your profile.'
    },
    {
        'id': 'sparkle',
        'name': 'Sparkle Frame',
        'cost': 100,
        'css': 'border-sparkle',
        'description': 'A sparkling reward border.'
    }
]


def parse_owned_borders(raw: Optional[str]) -> List[str]:
    if not raw:
        return []
    return [item for item in raw.split(',') if item.strip()]


def build_store_items(user):
    owned = set(parse_owned_borders(user.get('owned_borders')))
    selected = user.get('selected_border')
    items = []
    for item in BORDER_ITEMS:
        items.append({
            'id': item['id'],
            'name': item['name'],
            'cost': item['cost'],
            'css': item['css'],
            'description': item['description'],
            'owned': item['id'] in owned,
            'selected': item['id'] == selected
        })
    return items


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
        points=user_dict.get('points', 0),
        selected_border=user_dict.get('selected_border'),
        owned_borders=user_dict.get('owned_borders'),
        last_check_in=user_dict.get('last_check_in'),
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
async def update_user(user_id: int, updates: UserUpdate):
    """Update user profile"""
    user = User.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = updates.dict(exclude_unset=True)

    if 'username' in update_data and update_data['username'] != user['username']:
        existing = User.get_by_username(update_data['username'])
        if existing and existing['id'] != user_id:
            raise HTTPException(status_code=400, detail="Username already taken")

    if 'email' in update_data and update_data['email'] != user['email']:
        existing = User.get_by_email(update_data['email'])
        if existing and existing['id'] != user_id:
            raise HTTPException(status_code=400, detail="Email already taken")

    if User.update_profile(user_id, **update_data):
        user = User.get_by_id(user_id)
        return format_user(user)
    raise HTTPException(status_code=400, detail="No changes to update")

@app.get("/api/users/{user_id}/rewards")
async def get_user_rewards(user_id: int):
    """Get user reward information and available store items"""
    user = User.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "points": user.get('points', 0),
        "selected_border": user.get('selected_border'),
        "owned_borders": parse_owned_borders(user.get('owned_borders')),
        "store_items": build_store_items(user)
    }

@app.post("/api/users/{user_id}/check-in")
@app.post("/api/users/{user_id}/checkin")
async def daily_check_in(user_id: int):
    """Daily check-in to earn points"""
    user = User.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    today = datetime.utcnow().date().isoformat()
    yesterday = (datetime.utcnow().date() - timedelta(days=1)).isoformat()
    if user.get('last_check_in') == today:
        raise HTTPException(status_code=400, detail="Already checked in today")

    streak = 1
    if user.get('last_check_in') == yesterday:
        streak = (user.get('streak') or 0) + 1

    points = (user.get('points') or 0) + 10
    User.update_profile(user_id, points=points, streak=streak, last_check_in=today)
    user = User.get_by_id(user_id)
    return {
        "message": "Daily check-in complete! +10 points",
        "points": user.get('points', 0),
        "streak": user.get('streak', 0),
        "last_check_in": user.get('last_check_in')
    }

@app.post("/api/users/{user_id}/purchase-border")
async def purchase_border(user_id: int, item: PurchaseItem):
    """Purchase a profile border from the store"""
    user = User.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    item_data = next((item for item in BORDER_ITEMS if item['id'] == item.item_id), None)
    if not item_data:
        raise HTTPException(status_code=404, detail="Border not found")

    owned = set(parse_owned_borders(user.get('owned_borders')))
    if item_data['id'] in owned:
        return {"message": "Border already owned", "points": user.get('points', 0), "owned_borders": list(owned)}

    if user.get('points', 0) < item_data['cost']:
        raise HTTPException(status_code=400, detail="Not enough points to purchase this border")

    owned.add(item_data['id'])
    points = user.get('points', 0) - item_data['cost']
    owned_borders = ','.join(sorted(owned))
    User.update_profile(user_id, points=points, owned_borders=owned_borders)
    return {"message": f"Purchased {item_data['name']}!", "points": points, "owned_borders": list(owned)}

@app.post("/api/users/{user_id}/select-border")
async def select_border(user_id: int, selection: SelectBorder):
    """Select an owned border for the profile avatar"""
    user = User.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    owned = set(parse_owned_borders(user.get('owned_borders')))
    if selection.item_id not in owned:
        raise HTTPException(status_code=400, detail="Border not owned")

    User.update_profile(user_id, selected_border=selection.item_id)
    user = User.get_by_id(user_id)
    return {"message": "Border selected", "selected_border": user.get('selected_border')}

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

    user = User.get_by_id(user_id)
    if user:
        today = datetime.utcnow().date().isoformat()
        today_total = StudySession.get_today_study_time(user_id)
        if user.get('daily_goal') and today_total >= user.get('daily_goal', 0):
            if user.get('last_goal_reward_date') != today:
                reward_points = 20
                User.update_profile(user_id,
                                    points=(user.get('points', 0) + reward_points),
                                    last_goal_reward_date=today)
                new_session['goal_reward'] = {
                    'message': 'Daily goal reached! +20 points awarded.',
                    'points_awarded': reward_points
                }
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
