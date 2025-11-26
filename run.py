"""
Main entry point for Hostel Manager application
Run this file to start the Flask server
"""

import os
from app import create_app
from app.database.connection import init_db

# Create Flask app
app = create_app()

if __name__ == '__main__':
    # Initialize database and create tables
    init_db()

    # Allow overriding host/port via environment variables for flexibility
    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', os.environ.get('PYTHON_PORT', 5000)))

    print("=" * 60)
    print("🏨 Hostel Manager Application")
    print("=" * 60)
    print("\n✓ Database initialized")

    # Start the Flask development server
    print(f"\n🚀 Starting Hostel Manager server on http://{host}:{port} ...")
    print("\n⚠️  Press Ctrl+C to stop the server")
    print("\nInitial Setup:")
    print(f"1. Open http://{host}:{port} in your browser")
    print("2. Click 'Create an account' to set up your admin account")
    print("3. Log in with your credentials")
    print("\n" + "=" * 60 + "\n")

    # Run app (debug mode by default for development)
    app.run(debug=True, host=host, port=port)
