# FocusFlow - Smart Study Task and Distraction Tracker

A comprehensive web-based application designed to help students manage their study tasks, track focus time, monitor distractions, and build better study habits.

## 📋 Project Overview

FocusFlow combines three key features:
- **Task Manager**: Create, manage, and track study tasks
- **Study Timer**: Track focus time during study sessions
- **Distraction Tracker**: Log interruptions and analyze productivity patterns

## 🏗️ Technology Stack

- **Frontend**: Vue.js 3 + Vite
- **Backend**: FastAPI (Python)
- **Database**: SQLite
- **Package Manager**: npm (frontend), pip (backend)

## 📁 Project Structure

```
Midterm/
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── css/
│   │   ├── style.css
│   │   ├── auth.css
│   │   ├── dashboard.css
│   │   ├── tasks.css
│   │   ├── profile.css
│   │   └── study-session.css
│   └── js/
│       ├── app.js
│       ├── App.vue
│       ├── api.js
│       ├── router.js
│       ├── components/
│       │   └── Navigation.vue
│       └── views/
│           ├── Login.vue
│           ├── SignUp.vue
│           ├── Dashboard.vue
│           ├── Tasks.vue
│           ├── Profile.vue
│           └── StudySession.vue
├── api/
│   ├── requirements.txt
│   ├── main.py
│   └── models.py
├── database/
│   ├── db.py
│   ├── schema.sql
│   └── focusflow.db (generated on first run)
└── backend/
    └── (configuration files if needed)
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm

### Backend Setup

1. **Install Python dependencies**
```bash
cd api
pip install -r requirements.txt
```

2. **Initialize the database**
```bash
cd database
python db.py
```

This will create a `focusflow.db` file in the database folder with the schema.

3. **Start the FastAPI server**
```bash
cd api
python main.py
```

The API will run on `http://localhost:8000`

### Frontend Setup

1. **Install Node.js dependencies**
```bash
cd frontend
npm install
```

2. **Start the development server**
```bash
npm run dev
```

The frontend will run on `http://localhost:3000`

3. **Build for production**
```bash
npm run build
```

This creates an optimized build in the `dist/` folder.

## 🔐 Authentication

- Users can create new accounts via Sign Up page
- Login with username and password
- Session stored in browser localStorage
- Passwords are hashed using bcrypt

## 📱 Features

### Dashboard
- View study time statistics
- Track completed tasks
- Monitor distractions
- See active tasks count
- Visual distribution overview of task statuses

### Tasks Management
- Create new study tasks with title, description, priority
- Assign due dates to tasks
- Update task status (To Do, Active, Done)
- Delete tasks
- Filter and search tasks
- View task statistics

### Study Session
- Start/pause/stop study sessions with timer
- Associate sessions with specific tasks
- Track total daily study time
- Progress visualization
- Recent sessions history
- Log distractions with duration and description

### User Profile
- View user information
- Check achievement level
- View study streak
- Monitor daily study goal progress
- See total study time and completed tasks

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

### User
- `GET /api/users/{user_id}` - Get user profile
- `PUT /api/users/{user_id}` - Update profile
- `GET /api/dashboard/{user_id}` - Get dashboard stats

### Tasks
- `POST /api/tasks` - Create task
- `GET /api/tasks/{task_id}` - Get task
- `GET /api/users/{user_id}/tasks` - Get user tasks
- `PUT /api/tasks/{task_id}` - Update task
- `DELETE /api/tasks/{task_id}` - Delete task

### Study Sessions
- `POST /api/study-sessions` - Create session
- `GET /api/study-sessions/{session_id}` - Get session
- `GET /api/users/{user_id}/study-sessions` - Get user sessions

### Distractions
- `POST /api/distractions` - Log distraction
- `GET /api/distractions/{distraction_id}` - Get distraction
- `GET /api/users/{user_id}/distractions` - Get user distractions

## 💾 Database Schema

### Users Table
- id, username, email, password
- level, streak, total_study_time, tasks_completed
- daily_goal, created_at, updated_at

### Tasks Table
- id, user_id, title, description
- status (To Do, Active, Done)
- priority (Low, Medium, High)
- due_date, created_at, updated_at

### Study Sessions Table
- id, user_id, task_id
- duration_seconds, start_time, end_time
- created_at

### Distractions Table
- id, user_id, session_id
- duration_seconds, description
- start_time, end_time, created_at

## 🎨 UI Design

The application uses a modern, clean design with:
- Azure/cyan gradient accent colors
- Smooth transitions and hover effects
- Responsive layout (desktop and tablet optimized)
- Card-based interface
- Progress bars and statistics visualization
- Accessible form inputs

## 🔧 Development Tips

1. **Access the API documentation**: Navigate to `http://localhost:8000/docs` for interactive API docs

2. **Reset database**: Delete `focusflow.db` and run `python database/db.py` again

3. **Debug frontend**: Use Vue DevTools browser extension

4. **CORS issues**: Make sure the FastAPI server is running on `localhost:8000`

## 📝 Usage Guide

1. **Create an Account**: Go to Sign Up page and register with username, email, and password

2. **Login**: Use your credentials to login

3. **Create Tasks**: In Tasks page, add study tasks with title, description, priority, and due date

4. **Start Study Session**: Go to Study Session, select a task (optional), and click "Start Study Session"

5. **Track Distractions**: Log any distractions during your study with duration

6. **Monitor Progress**: Check Dashboard to see your study stats and habits

7. **Update Profile**: Visit Profile page to see your achievements and daily goal progress

## 🐛 Troubleshooting

### Database connection error
- Ensure `focusflow.db` exists in the database folder
- Run `python database/db.py` to initialize

### API not responding
- Check that FastAPI server is running on `http://localhost:8000`
- Verify `http://localhost:8000/api/health` in browser

### CORS errors
- Ensure FastAPI has CORS middleware enabled
- Check that frontend is accessing correct API URL

### Frontend not loading
- Ensure `npm install` was run and dependencies installed
- Check that `npm run dev` is running
- Clear browser cache

## 📄 License

This project is part of a midterm examination.

## 👤 Author

Jerome Mark B. Salud (jeromemark.salud@unc.edu.ph)

## 🤝 Support

For issues or questions, please refer to the project documentation or contact the development team.

---

**Stay Focus, Stay Productive with FocusFlow!** 🚀
