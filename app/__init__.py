"""
Flask application factory for Hostel Manager
"""

from flask import Flask
from app.database.connection import init_db

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__, template_folder='templates', static_folder='static')
    
    # Configuration
    app.config['SECRET_KEY'] = 'hostel-manager-secret-key-change-in-production'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour
    
    # Initialize database
    init_db()
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.students import students_bp
    from app.routes.rooms import rooms_bp
    from app.routes.installments import installments_bp
    from app.routes.settings import settings_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(rooms_bp)
    app.register_blueprint(installments_bp)
    app.register_blueprint(settings_bp)
    
    return app
