"""
Configuration file for Hostel Manager
Customize settings here
"""

import os

# Application Settings
DEBUG = True  # Set to False in production
SECRET_KEY = 'hostel-manager-secret-key-change-in-production'  # Change this!
PERMANENT_SESSION_LIFETIME = 3600  # Session timeout in seconds (1 hour)

# Database Settings
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'hostel_manager.db')

# Application Settings
APP_NAME = 'Hostel Manager'
APP_VERSION = '1.0.0'

# Room Settings
DEFAULT_ROOM_CAPACITY = 2  # Number of students per room

# Payment Settings
DEFAULT_INSTALLMENTS = 2  # Default number of installments

# Email Settings (Override in application settings page)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

# Flask Settings
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False  # Set to True if using HTTPS
SESSION_COOKIE_SAMESITE = 'Lax'

# Server Settings
HOST = 'localhost'
PORT = 5000

# UI Settings
ITEMS_PER_PAGE = 20
