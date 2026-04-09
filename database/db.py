import sqlite3
import os
from pathlib import Path

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'focusflow.db')

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with schema"""
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    
    if not os.path.exists(schema_path):
        print(f"Schema file not found at {schema_path}")
        return False
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        with open(schema_path, 'r') as f:
            sql_script = f.read()
        
        cursor.executescript(sql_script)
        conn.commit()
        print("Database initialized successfully!")
        return True
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
        return False
    finally:
        conn.close()

def drop_db():
    """Drop database (for testing/reset)"""
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
        print("Database dropped successfully!")

if __name__ == "__main__":
    init_db()
