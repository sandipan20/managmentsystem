# 📂 PROJECT FILE STRUCTURE & DOCUMENTATION

Complete reference for all files in the Hostel Manager project.

## Directory Tree

```
hostelmanagment/
├── app/                           # Main application package
│   ├── __init__.py               # Flask app factory
│   │
│   ├── database/                 # Database layer
│   │   ├── __init__.py
│   │   ├── connection.py         # SQLite connection & initialization
│   │   └── models.py             # Student model & database operations
│   │
│   ├── routes/                   # Flask blueprints & routes
│   │   ├── __init__.py
│   │   ├── auth.py              # Login/logout/setup routes
│   │   ├── dashboard.py         # Dashboard route
│   │   ├── students.py          # Student CRUD operations
│   │   ├── rooms.py             # Room management routes
│   │   ├── installments.py      # Payment & installment routes
│   │   └── settings.py          # Settings & configuration routes
│   │
│   ├── utils/                    # Utility functions
│   │   ├── __init__.py
│   │   ├── auth.py              # Password hashing & verification
│   │   ├── email_service.py     # Gmail integration & email sending
│   │   ├── room_manager.py      # Room allocation logic
│   │   └── installment_manager.py # Payment calculations & tracking
│   │
│   ├── templates/               # HTML templates
│   │   ├── base.html            # Base template with navigation
│   │   ├── error.html           # Error page
│   │   │
│   │   ├── auth/                # Authentication templates
│   │   │   ├── login.html       # Login page
│   │   │   └── setup.html       # Admin account setup
│   │   │
│   │   ├── dashboard/           # Dashboard templates
│   │   │   └── index.html       # Main dashboard
│   │   │
│   │   ├── students/            # Student management templates
│   │   │   ├── list.html        # List all students
│   │   │   ├── add.html         # Add new student form
│   │   │   ├── detail.html      # Student detail view
│   │   │   └── edit.html        # Edit student form
│   │   │
│   │   ├── rooms/               # Room management templates
│   │   │   ├── list.html        # List all rooms
│   │   │   └── capacity.html    # Set room capacity
│   │   │
│   │   ├── installments/        # Payment templates
│   │   │   ├── student_installments.html # Student's installments
│   │   │   ├── pending.html     # Overdue payments
│   │   │   └── upcoming.html    # Upcoming payments
│   │   │
│   │   └── settings/            # Settings templates
│   │       └── email.html       # Email configuration
│   │
│   └── static/                  # Static files (CSS, JS, images)
│       ├── css/
│       │   └── style.css        # Main stylesheet
│       └── js/
│           └── main.js          # JavaScript utilities
│
├── venv/                        # Python virtual environment (created at setup)
│
├── run.py                       # Application entry point
├── config.py                    # Configuration settings
├── requirements.txt             # Python package dependencies
│
├── init_sample_data.py          # Sample data initialization script
│
├── start.sh                     # Quick start bash script
│
├── README.md                    # Complete documentation
├── QUICKSTART.md               # 5-minute quick start guide
├── INSTALLATION.md             # Detailed installation guide
├── FEATURES.md                 # Complete features guide
├── FILE_STRUCTURE.md           # This file
│
└── hostel_manager.db           # SQLite database (created at first run)
```

## File Descriptions

### Core Application Files

#### `run.py`
- **Purpose**: Entry point for the Flask application
- **Usage**: `python3 run.py` to start the server
- **Contains**: Flask app initialization and server startup
- **Do Not Modify**: Unless changing port or debug settings

#### `config.py`
- **Purpose**: Centralized configuration settings
- **Usage**: Import and use for app configuration
- **Contains**: Database path, Flask settings, defaults
- **Can Modify**: To change defaults (room capacity, session timeout, etc.)

#### `requirements.txt`
- **Purpose**: List of Python package dependencies
- **Usage**: `pip install -r requirements.txt`
- **Contains**: Flask==2.3.3, Werkzeug==2.3.7, Jinja2==3.1.2
- **Do Not Modify**: Unless adding new Python packages

### Application Package (`app/`)

#### `app/__init__.py`
- **Purpose**: Flask app factory
- **Usage**: Creates Flask app and registers blueprints
- **Contains**: Flask configuration and blueprint registration
- **Key Function**: `create_app()` returns Flask application instance

#### `app/database/connection.py`
- **Purpose**: Database connection management
- **Usage**: Provides `get_db_connection()` function
- **Contains**: SQLite connection initialization
- **Key Function**: `get_db_connection()` returns database connection

#### `app/database/models.py`
- **Purpose**: Student model and database operations
- **Usage**: Student CRUD operations
- **Contains**: Student class with all database methods
- **Key Methods**:
  - `add_student()`: Insert new student
  - `get_all_students()`: Retrieve all students
  - `search_students()`: Search functionality
  - `update_student()`: Modify student info
  - `delete_student()`: Remove student record

#### `app/utils/auth.py`
- **Purpose**: Authentication and password management
- **Usage**: Login verification and password hashing
- **Contains**: Password hashing, admin verification
- **Key Functions**:
  - `hash_password()`: Secure password hashing
  - `verify_password()`: Check password validity
  - `create_admin_user()`: Create new admin
  - `verify_admin_credentials()`: Login verification

#### `app/utils/email_service.py`
- **Purpose**: Email sending functionality
- **Usage**: Send payment reminder emails via Gmail
- **Contains**: Gmail SMTP integration
- **Key Functions**:
  - `send_reminder_email()`: Send to single student
  - `send_bulk_reminders()`: Send to multiple students
  - `get_email_config()`: Retrieve email settings
  - `save_email_config()`: Store email settings

#### `app/utils/room_manager.py`
- **Purpose**: Room allocation and management
- **Usage**: Manage rooms, allocate students, track occupancy
- **Contains**: Room CRUD and allocation logic
- **Key Functions**:
  - `create_room()`: Create new room
  - `allocate_room_to_student()`: Assign room automatically
  - `get_all_rooms()`: List all rooms
  - `set_room_capacity()`: Configure capacity
  - `get_room_statistics()`: Get occupancy stats

#### `app/utils/installment_manager.py`
- **Purpose**: Payment and installment tracking
- **Usage**: Create, track, and update installments
- **Contains**: Installment calculations and payment tracking
- **Key Functions**:
  - `create_installments()`: Generate installment records
  - `get_student_installments()`: List student's payments
  - `mark_installment_paid()`: Record payment
  - `get_overdue_installments()`: Find late payments
  - `get_payment_statistics()`: Payment summary

### Routes (Blueprints)

#### `app/routes/auth.py`
- **Purpose**: Authentication routes
- **Routes**:
  - `/login` (GET/POST): Admin login
  - `/logout` (GET): Logout
  - `/setup` (GET/POST): Initial admin setup
- **Contains**: Login decorator for protected routes

#### `app/routes/dashboard.py`
- **Purpose**: Dashboard route
- **Routes**:
  - `/` or `/dashboard` (GET): Main dashboard
- **Contains**: Statistics gathering and display

#### `app/routes/students.py`
- **Purpose**: Student management routes
- **Routes**:
  - `/students/` (GET): List students
  - `/students/add` (GET/POST): Add new student
  - `/students/<aadhaar>` (GET): View student details
  - `/students/<aadhaar>/edit` (GET/POST): Edit student
  - `/students/<aadhaar>/delete` (POST): Delete student
  - `/students/search` (GET): Search students

#### `app/routes/rooms.py`
- **Purpose**: Room management routes
- **Routes**:
  - `/rooms/` (GET): List rooms
  - `/rooms/create` (POST): Create room
  - `/rooms/capacity` (GET/POST): Manage capacity
  - `/rooms/available` (GET): Get available rooms

#### `app/routes/installments.py`
- **Purpose**: Payment management routes
- **Routes**:
  - `/installments/student/<aadhaar>` (GET): Student's payments
  - `/installments/mark-paid` (POST): Record payment
  - `/installments/pending` (GET): Overdue payments
  - `/installments/upcoming` (GET): Upcoming payments
  - `/installments/send-reminder/<aadhaar>/<number>` (POST): Send email

#### `app/routes/settings.py`
- **Purpose**: Settings routes
- **Routes**:
  - `/settings/email` (GET/POST): Email configuration

### Templates

#### `app/templates/base.html`
- **Purpose**: Base template with navigation
- **Extends**: Nothing (base for all pages)
- **Contains**: Navigation bar, container structure
- **Used By**: All other templates extend this

#### `app/templates/auth/login.html`
- **Purpose**: Admin login page
- **Features**: Username/password form, error messages
- **Route**: `/login`

#### `app/templates/auth/setup.html`
- **Purpose**: Initial admin account setup
- **Features**: Setup form, success message
- **Route**: `/setup`

#### `app/templates/dashboard/index.html`
- **Purpose**: Main dashboard
- **Features**: Statistics cards, quick actions
- **Route**: `/` or `/dashboard`

#### `app/templates/students/list.html`
- **Purpose**: List all students
- **Features**: Table, search functionality, action buttons
- **Route**: `/students/`

#### `app/templates/students/add.html`
- **Purpose**: Add new student form
- **Features**: Comprehensive form, validation, error messages
- **Route**: `/students/add`

#### `app/templates/students/detail.html`
- **Purpose**: View student full details
- **Features**: Complete profile, installments, actions
- **Route**: `/students/<aadhaar>`

#### `app/templates/students/edit.html`
- **Purpose**: Edit student information
- **Features**: Pre-filled form, editable fields
- **Route**: `/students/<aadhaar>/edit`

#### `app/templates/rooms/list.html`
- **Purpose**: List and manage rooms
- **Features**: Room grid, occupancy status, add room form
- **Route**: `/rooms/`

#### `app/templates/rooms/capacity.html`
- **Purpose**: Configure room capacity
- **Features**: Capacity input, information panel
- **Route**: `/rooms/capacity`

#### `app/templates/installments/student_installments.html`
- **Purpose**: View student's installments
- **Features**: Payment table, mark paid, send reminder
- **Route**: `/installments/student/<aadhaar>`

#### `app/templates/installments/pending.html`
- **Purpose**: View overdue payments
- **Features**: All overdue payments, bulk actions, statistics
- **Route**: `/installments/pending`

#### `app/templates/installments/upcoming.html`
- **Purpose**: View upcoming payments
- **Features**: Payments due within 30 days
- **Route**: `/installments/upcoming`

#### `app/templates/settings/email.html`
- **Purpose**: Email configuration page
- **Features**: Email form, help text, status
- **Route**: `/settings/email`

### Static Files

#### `app/static/css/style.css`
- **Purpose**: Main stylesheet
- **Contains**: All CSS styles, responsive design, theme
- **Features**: Variables, responsive grid, animations
- **Colors**: Primary (#667eea), secondary (#764ba2), danger (#f56565)

#### `app/static/js/main.js`
- **Purpose**: JavaScript utilities
- **Contains**: Helper functions for common operations
- **Key Functions**:
  - `showAlert()`: Display messages
  - `formatCurrency()`: Format rupees
  - `isValidEmail()`: Email validation
  - `isValidPhone()`: Phone validation

### Documentation Files

#### `README.md`
- **Purpose**: Complete project documentation
- **Contents**: Features, setup, usage, troubleshooting, database schema
- **For**: Comprehensive understanding of the system

#### `QUICKSTART.md`
- **Purpose**: Get started in 5 minutes
- **Contents**: Quick setup steps, basic usage
- **For**: New users wanting to start immediately

#### `INSTALLATION.md`
- **Purpose**: Detailed installation guide
- **Contents**: System requirements, step-by-step setup, troubleshooting
- **For**: Users needing detailed installation help

#### `FEATURES.md`
- **Purpose**: Complete features reference
- **Contents**: Detailed explanation of each feature
- **For**: Users learning about system capabilities

### Utility Scripts

#### `start.sh`
- **Purpose**: Quick start shell script
- **Usage**: `./start.sh` to start application
- **Contains**: Virtual environment setup and startup commands
- **For**: macOS/Linux users (one-command startup)

#### `init_sample_data.py`
- **Purpose**: Add sample data to database
- **Usage**: `python3 init_sample_data.py` after admin setup
- **Contains**: 5 sample students with installments
- **For**: Testing and demonstration

### Database File

#### `hostel_manager.db`
- **Purpose**: SQLite database
- **Format**: Binary SQLite 3 database
- **Created**: Automatically on first run
- **Contains**: All application data
- **Backup**: Copy this file to backup all data

## Dependencies (requirements.txt)

### Flask 2.3.3
- Web framework
- Handles HTTP requests and routing
- Manages sessions and cookies

### Werkzeug 2.3.7
- WSGI utilities
- Password hashing support
- Request/response handling

### Jinja2 3.1.2
- Template engine
- Renders HTML templates
- Supports loops, conditionals, filters

## Database Schema

### tables:
1. **students** - Student records
2. **installments** - Payment installments
3. **rooms** - Room information
4. **admin_users** - Admin login accounts
5. **settings** - System configuration

See database schema in README.md for complete details.

## Key Design Decisions

### Single App vs. Separated Concerns
- Used blueprints for modular routes
- Separated database, utilities, and routes
- Easy to understand and modify

### Database Choice
- SQLite (no separate database server needed)
- Works on all operating systems
- File-based (easy backup)
- Suitable for small to medium deployments

### Authentication
- Session-based (not token-based)
- Simpler for web application
- Suitable for internal use

### UI Framework
- Vanilla HTML/CSS/JavaScript (no heavy frameworks)
- Responsive grid layout
- Fast loading times
- Easy to understand and modify

## Adding New Features

To add new features, follow this pattern:

1. **Model**: Add database operations in `app/database/models.py` or create utility
2. **Route**: Create route in appropriate `app/routes/*.py` file
3. **Template**: Create HTML template in `app/templates/`
4. **Style**: Add CSS to `app/static/css/style.css`
5. **JavaScript**: Add functions to `app/static/js/main.js` if needed

## Modifying Existing Features

To modify features:

1. Find relevant file from this structure
2. Make changes
3. Test thoroughly
4. Restart server (`python3 run.py`)
5. Refresh browser to see changes

## File Modification Guide

### Safe to Modify
- `config.py` - Change settings
- `app/static/css/style.css` - Change styles
- `app/static/js/main.js` - Add JavaScript
- HTML templates - Change layout/content
- `start.sh` - Change startup commands

### Careful When Modifying
- `app/database/models.py` - Database schema changes
- `app/routes/*.py` - API changes
- `app/utils/*.py` - Core logic

### DO NOT Modify
- `app/__init__.py` - Unless adding new routes
- `requirements.txt` - Unless adding new packages
- `run.py` - Unless changing port/debug mode

---

**Complete project structure documented! Ready to build. 🏨**
