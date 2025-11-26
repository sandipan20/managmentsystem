"""
Authentication utilities for Hostel Manager
Handles password hashing and admin login
"""

import hashlib
import os
import sqlite3
from app.database.connection import get_db_connection

def hash_password(password):
    """
    Hash a password using SHA256
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password string
    """
    salt = os.urandom(32)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt.hex() + pwd_hash.hex()

def verify_password(password, password_hash):
    """
    Verify a password against its hash
    
    Args:
        password: Plain text password to verify
        password_hash: Stored hash to compare against
        
    Returns:
        Boolean indicating if password is correct
    """
    salt = bytes.fromhex(password_hash[:64])
    stored_hash = password_hash[64:]
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()
    return pwd_hash == stored_hash

def create_admin_user(username, password):
    """
    Create a new admin user
    
    Args:
        username: Admin username
        password: Admin password (will be hashed)
        
    Returns:
        Tuple (success: bool, message: str)
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        password_hash = hash_password(password)
        
        cursor.execute('''
            INSERT INTO admin_users (username, password_hash)
            VALUES (?, ?)
        ''', (username, password_hash))
        
        conn.commit()
        conn.close()
        
        return True, "Admin user created successfully"
        
    except sqlite3.IntegrityError:
        return False, "Username already exists"
    except Exception as e:
        return False, f"Error: {str(e)}"

def verify_admin_credentials(username, password):
    """
    Verify admin login credentials
    
    Args:
        username: Admin username
        password: Admin password
        
    Returns:
        Tuple (success: bool, admin_id: int or None, message: str)
    """
    try:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, password_hash FROM admin_users WHERE username = ?', (username,))
        admin = cursor.fetchone()
        conn.close()
        
        if not admin:
            return False, None, "Invalid username or password"
        
        if verify_password(password, admin['password_hash']):
            return True, admin['id'], "Login successful"
        else:
            return False, None, "Invalid username or password"
            
    except Exception as e:
        return False, None, f"Error: {str(e)}"
