import sqlite3
import os
from pathlib import Path

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'focusflow.db')

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def add_column_if_missing(conn, table: str, column_definition: str):
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table})")
    existing_columns = [row['name'] for row in cursor.fetchall()]
    column_name = column_definition.split()[0]
    if column_name not in existing_columns:
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column_definition}")


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
        # Add reward columns if the DB already existed before this feature
        add_column_if_missing(conn, 'users', 'points INTEGER DEFAULT 0')
        add_column_if_missing(conn, 'users', 'last_check_in TEXT')
        add_column_if_missing(conn, 'users', 'selected_border TEXT')
        add_column_if_missing(conn, 'users', 'owned_borders TEXT DEFAULT ""')
        add_column_if_missing(conn, 'users', 'last_goal_reward_date TEXT')
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
