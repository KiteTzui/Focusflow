# FocusFlow - Quick Start Guide

## 🚀 Quick Start (2 Minutes)

### Windows Users
Simply double-click the startup script:
```
start.bat
```

Or run in PowerShell:
```powershell
.\start.ps1
```

This will:
1. Initialize the database
2. Install all dependencies
3. Start the backend (FastAPI) on `http://localhost:8000`
4. Start the frontend (Vue) on `http://localhost:3000`

### Mac/Linux Users
Run the startup script:
```bash
chmod +x start.sh
./start.sh
```

## 📱 First Steps

1. **Open your browser** and go to: `http://localhost:3000`

2. **Create an Account**
   - Click "Sign Up"
   - Enter username, email, and password
   - Click "SIGN-UP"

3. **Login**
   - Use your credentials to login
   - You'll be redirected to the Dashboard

4. **Create Your First Task**
   - Go to "Tasks" in the sidebar
   - Fill in the task details
   - Click "+ Add Task"

5. **Start a Study Session**
   - Go to "Study Session"
   - Select a task (optional)
   - Click "▶ Start Study Session"
   - Click "⏹ Stop" when done

6. **View Your Progress**
   - Go to "Dashboard" to see your stats
   - Check "Profile" for your achievements

## 🧪 API Testing

### Interactive API Documentation
After starting the backend, visit:
```
http://localhost:8000/docs
```

This provides an interactive interface to test all API endpoints.

## 🔧 Manual Start (If using startup script fails)

### Terminal 1 - Backend
```bash
cd api
python main.py
```

### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```

## 📚 Default Test Account

You can test with these credentials after creating an account:
- **Username**: testuser
- **Password**: password123

## 🆘 Common Issues

### "Cannot find module 'vue'"
Solution:
```bash
cd frontend
npm install
```

### "Port 3000/8000 already in use"
Solution: Close other applications using these ports or change the port in:
- Frontend: Edit `frontend/vite.config.js`
- Backend: Edit `api/main.py` and change port in `uvicorn.run()`

### "Database error"
Solution:
```bash
rm database/focusflow.db
cd database
python db.py
```

### CORS Error in browser console
Solution: Make sure both backend and frontend are running:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000

## 📊 Example Workflow

1. Create a task: "Math Assignment - Chapter 5"
2. Set priority to "High"
3. Set due date: Tomorrow
4. Go to Study Session
5. Select the task
6. Click "Start Study Session"
7. Study for 25 minutes
8. Log any distractions
9. Click "Stop"
10. Check Dashboard to see progress

## 🎯 Features to Try

- ✅ Create multiple tasks with different priorities
- ⏱️ Use the study timer to track focus time
- 📊 View real-time statistics on Dashboard
- 🎯 Complete tasks and track progress
- 🚫 Log distractions to identify patterns
- 👤 Update your profile and daily goals

## 💡 Tips

1. **Daily Goal**: Set your daily study goal in profile settings (default: 2 hours)
2. **Task Priority**: Use priorities to focus on what matters most
3. **Regular Tracking**: Log all distractions for accurate insights
4. **Daily Sessions**: Start a new session each study day for best tracking

## 🔗 Useful Links

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Database: database/focusflow.db

## 📝 Project Files

- **Source Code**: `/api` (FastAPI backend), `/frontend` (Vue.js)
- **Database**: `/database/focusflow.db`
- **Documentation**: README.md

## 🆘 Need Help?

Check the README.md file for detailed documentation and troubleshooting guide.

---

**Enjoy using FocusFlow! Stay focused, stay productive! 🚀**
