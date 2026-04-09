import sqlite3
from typing import List, Optional, Dict, Any
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from database.db import get_db_connection

class User:
    @staticmethod
    def create(username: str, email: str, hashed_password: str) -> Dict[str, Any]:
        """Create a new user"""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                '''INSERT INTO users (username, email, password) 
                   VALUES (?, ?, ?)''',
                (username, email, hashed_password)
            )
            conn.commit()
            user_id = cursor.lastrowid
            return User.get_by_id(user_id)
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_id(user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def get_by_username(username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def get_by_email(email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def update_profile(user_id: int, level: str = None, streak: int = None, 
                      daily_goal: int = None) -> bool:
        """Update user profile"""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            updates = []
            params = []
            if level:
                updates.append('level = ?')
                params.append(level)
            if streak is not None:
                updates.append('streak = ?')
                params.append(streak)
            if daily_goal is not None:
                updates.append('daily_goal = ?')
                params.append(daily_goal)
            
            if updates:
                params.append(user_id)
                cursor.execute(
                    f'UPDATE users SET {", ".join(updates)}, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                    params
                )
                conn.commit()
                return True
            return False
        finally:
            conn.close()

class Task:
    @staticmethod
    def create(user_id: int, title: str, description: str = None, 
              status: str = 'To Do', priority: str = 'Medium',
              due_date: str = None) -> Dict[str, Any]:
        """Create a new task"""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                '''INSERT INTO tasks (user_id, title, description, status, priority, due_date)
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (user_id, title, description, status, priority, due_date)
            )
            conn.commit()
            task_id = cursor.lastrowid
            return Task.get_by_id(task_id)
        finally:
            conn.close()

    @staticmethod
    def get_by_id(task_id: int) -> Optional[Dict[str, Any]]:
        """Get task by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def get_user_tasks(user_id: int, status: str = None) -> List[Dict[str, Any]]:
        """Get all tasks for a user"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if status:
            cursor.execute('SELECT * FROM tasks WHERE user_id = ? AND status = ? ORDER BY created_at DESC',
                         (user_id, status))
        else:
            cursor.execute('SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
        
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def update(task_id: int, **kwargs) -> bool:
        """Update a task"""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            allowed_fields = {'title', 'description', 'status', 'priority', 'due_date'}
            updates = []
            params = []
            
            for field, value in kwargs.items():
                if field in allowed_fields:
                    updates.append(f'{field} = ?')
                    params.append(value)
            
            if updates:
                params.append(task_id)
                cursor.execute(
                    f'UPDATE tasks SET {", ".join(updates)}, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                    params
                )
                conn.commit()
                return True
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(task_id: int) -> bool:
        """Delete a task"""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

class StudySession:
    @staticmethod
    def create(user_id: int, duration_seconds: int, start_time: str,
              end_time: str, task_id: int = None) -> Dict[str, Any]:
        """Create a new study session"""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                '''INSERT INTO study_sessions (user_id, task_id, duration_seconds, start_time, end_time)
                   VALUES (?, ?, ?, ?, ?)''',
                (user_id, task_id, duration_seconds, start_time, end_time)
            )
            conn.commit()
            session_id = cursor.lastrowid
            return StudySession.get_by_id(session_id)
        finally:
            conn.close()

    @staticmethod
    def get_by_id(session_id: int) -> Optional[Dict[str, Any]]:
        """Get session by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM study_sessions WHERE id = ?', (session_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def get_user_sessions(user_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent study sessions for a user"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''SELECT * FROM study_sessions WHERE user_id = ? 
               ORDER BY created_at DESC LIMIT ?''',
            (user_id, limit)
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_total_study_time(user_id: int) -> int:
        """Get total study time in seconds"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT COALESCE(SUM(duration_seconds), 0) as total FROM study_sessions WHERE user_id = ?',
            (user_id,)
        )
        result = cursor.fetchone()
        conn.close()
        return result['total'] if result else 0

class Distraction:
    @staticmethod
    def create(user_id: int, duration_seconds: int, start_time: str,
              end_time: str, session_id: int = None, description: str = None) -> Dict[str, Any]:
        """Create a new distraction record"""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                '''INSERT INTO distractions (user_id, session_id, duration_seconds, start_time, end_time, description)
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (user_id, session_id, duration_seconds, start_time, end_time, description)
            )
            conn.commit()
            distraction_id = cursor.lastrowid
            return Distraction.get_by_id(distraction_id)
        finally:
            conn.close()

    @staticmethod
    def get_by_id(distraction_id: int) -> Optional[Dict[str, Any]]:
        """Get distraction by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM distractions WHERE id = ?', (distraction_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def get_user_distractions(user_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent distractions for a user"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''SELECT * FROM distractions WHERE user_id = ? 
               ORDER BY created_at DESC LIMIT ?''',
            (user_id, limit)
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_total_distractions(user_id: int) -> int:
        """Get total distraction count"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) as count FROM distractions WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result['count'] if result else 0

    @staticmethod
    def get_total_distraction_time(user_id: int) -> int:
        """Get total distraction time in seconds"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT COALESCE(SUM(duration_seconds), 0) as total FROM distractions WHERE user_id = ?',
            (user_id,)
        )
        result = cursor.fetchone()
        conn.close()
        return result['total'] if result else 0
