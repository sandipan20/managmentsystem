"""
Database connection utility for Hostel Manager
Handles SQLite database initialization and connection
"""

import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'hostel_manager.db')

def get_db_connection():
    """
    Get a connection to the SQLite database with foreign keys enabled
    
    Returns:
        sqlite3.Connection object
    """
    conn = sqlite3.connect(DATABASE_PATH)
    # Enable foreign key constraints for cascading deletes
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """Initialize the database with all tables"""
    from app.database.models import Student
    Student.create_table()
