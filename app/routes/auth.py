"""
Authentication routes for Hostel Manager
Handles login, logout, and protected route decorators
"""

from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from functools import wraps
from app.utils.auth import verify_admin_credentials, create_admin_user

auth_bp = Blueprint('auth', __name__)

def login_required(f):
    """
    Decorator to protect routes - requires admin login
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle admin login"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            return render_template('auth/login.html', 
                                 error='Username and password are required')
        
        success, admin_id, message = verify_admin_credentials(username, password)
        
        if success:
            session['admin_id'] = admin_id
            session['username'] = username
            session.permanent = True
            return redirect(url_for('dashboard.index'))
        else:
            return render_template('auth/login.html', error=message)
    
    # Already logged in
    if 'admin_id' in session:
        return redirect(url_for('dashboard.index'))
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    """Handle admin logout"""
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bp.route('/setup', methods=['GET', 'POST'])
def setup():
    """
    Initial setup page to create first admin user
    Only accessible if no admin users exist
    """
    from app.database.connection import get_db_connection
    import sqlite3
    
    # Check if any admin exists
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM admin_users')
    admin_count = cursor.fetchone()[0]
    conn.close()
    
    if admin_count > 0:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        
        if not username or not password:
            return render_template('auth/setup.html', 
                                 error='Username and password are required')
        
        if len(username) < 3:
            return render_template('auth/setup.html',
                                 error='Username must be at least 3 characters')
        
        if len(password) < 6:
            return render_template('auth/setup.html',
                                 error='Password must be at least 6 characters')
        
        if password != password_confirm:
            return render_template('auth/setup.html',
                                 error='Passwords do not match')
        
        success, message = create_admin_user(username, password)
        
        if success:
            # Create some sample rooms
            from app.utils.room_manager import create_room
            for i in range(1, 6):
                create_room(f"Room-{i}")
            
            return render_template('auth/setup.html',
                                 success='Admin user created successfully. You can now login.')
        else:
            return render_template('auth/setup.html', error=message)
    
    return render_template('auth/setup.html')
