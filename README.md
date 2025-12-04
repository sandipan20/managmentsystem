# 🏨 Hostel Manager

**A comprehensive, production-ready hostel management system built with Python Flask, SQLite, and modern web technologies.**

> Managing hostels made simple, efficient, and reliable.

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-brightgreen.svg)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-orange.svg)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#license)

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Getting Started](#getting-started)
- [Usage Guide](#usage-guide)
- [Database Schema](#database-schema)
- [API Routes](#api-routes)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

Hostel Manager is a complete solution for managing hostel operations efficiently. It streamlines student registration, room allocation, payment tracking, and communication. The system is designed to be intuitive, reliable, and scalable for hostels of any size.

### Why Use Hostel Manager?

- **All-in-One Solution** - Students, rooms, payments, and communications all in one place
- **Automatic Room Allocation** - Intelligent room assignment based on availability
- **Smart Payment Tracking** - Multiple installments with automated reminders
- **Data Integrity** - Comprehensive validation and cascading operations
- **Email Integration** - Direct Gmail integration for payment reminders
- **Easy to Use** - Intuitive web interface requiring no technical knowledge
- **Secure** - Password hashing, session management, and data protection

## ✨ Key Features

### Core Functionality
| Feature | Description |
|---------|------------|
| **Admin Authentication** | Secure login with encrypted passwords and session management |
| **Student Management** | Add, edit, view, search, and delete student records with validation |
| **Room Management** | Create rooms, set capacity, and track occupancy in real-time |
| **Automatic Allocation** | Smart room assignment based on availability and capacity |
| **Payment Tracking** | Divide fees into installments with due dates and status tracking |
| **Email Reminders** | Automated Gmail notifications for overdue payments |
| **Dashboard Analytics** | Real-time statistics and overview of all operations |
| **Search & Filter** | Find students by multiple criteria instantly |
| **Responsive Design** | Works seamlessly on desktop, tablet, and mobile devices |
| **Data Validation** | Comprehensive input validation for all operations |
| **Bulk Operations** | Send reminders to multiple students at once |
| **Audit Trail** | Timestamps for all operations for accountability |

### Advanced Features
- **Cascading Deletion** - Automatically free up rooms when students are deleted
- **Payment History** - Complete record of all payments and transactions
- **Dynamic Settings** - Configurable capacity and email preferences
- **Status Indicators** - Visual indicators for room and payment status
- **Quick Actions** - Common operations accessible with single click
- **Error Handling** - Graceful error messages and recovery options

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Web Browser                        │
│              (HTML/CSS/JavaScript)                   │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│           Flask Web Application                      │
│  ┌──────────────────────────────────────────────┐  │
│  │  Routes Layer                                │  │
│  │  - auth.py      (Authentication)            │  │
│  │  - dashboard.py (Dashboard)                 │  │
│  │  - students.py  (Student operations)        │  │
│  │  - rooms.py     (Room operations)           │  │
│  │  - installments.py (Payment operations)     │  │
│  │  - settings.py  (Configuration)             │  │
│  └──────────────────────────────────────────────┘  │
│                     │                                │
│  ┌──────────────────▼──────────────────────────┐  │
│  │  Business Logic Layer                      │  │
│  │  - auth.py (Password hashing)              │  │
│  │  - room_manager.py (Allocation logic)      │  │
│  │  - installment_manager.py (Payments)      │  │
│  │  - email_service.py (Notifications)       │  │
│  └──────────────────┬──────────────────────────┘  │
└─────────────────────┼──────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│          SQLite Database                            │
│  ┌──────────────────────────────────────────────┐  │
│  │  Tables:                                     │  │
│  │  - students (100 records)                   │  │
│  │  - rooms (25 records)                       │  │
│  │  - installments (400 records)               │  │
│  │  - payments (260 records)                   │  │
│  │  - admin_users (credentials)                │  │
│  │  - settings (configuration)                 │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

## 📁 Project Structure
```
hotelmanager/
├── 📄 README.md                        # This file - Complete documentation
├── 📄 INSTALLATION.md                  # Detailed installation guide
├── 📄 QUICKSTART.md                    # Quick start guide for new users
├── 📄 PROJECT_SUMMARY.md               # Project overview and statistics
├── 📄 FEATURES.md                      # Detailed features documentation
├── 📄 config.py                        # Application configuration
├── 📄 run.py                           # Application entry point
├── 📄 requirements.txt                 # Python package dependencies
├── 📄 start.sh                         # Startup script
├── 📊 hostel_manager.db                # SQLite database (auto-created)
│
├── 📁 app/                             # Main application package
│   ├── __init__.py                     # Flask app factory
│   │
│   ├── 📁 templates/                   # HTML templates
│   │   ├── base.html                   # Base template with navigation
│   │   ├── error.html                  # Error page template
│   │   ├── auth/
│   │   │   ├── login.html              # Login page
│   │   │   └── setup.html              # Initial admin setup
│   │   ├── dashboard/
│   │   │   └── index.html              # Dashboard with statistics
│   │   ├── students/
│   │   │   ├── list.html               # List all students
│   │   │   ├── add.html                # Add new student form
│   │   │   ├── detail.html             # Student details view
│   │   │   └── edit.html               # Edit student form
│   │   ├── rooms/
│   │   │   ├── list.html               # List all rooms
│   │   │   ├── detail.html             # Room details
│   │   │   ├── edit.html               # Edit room
│   │   │   └── capacity.html           # Room capacity settings
│   │   ├── installments/
│   │   │   ├── pending.html            # Pending/overdue payments
│   │   │   ├── student_installments.html  # Student's payment schedule
│   │   │   └── upcoming.html           # Upcoming payments
│   │   └── settings/
│   │       └── email.html              # Email configuration
│   │
│   ├── 📁 static/                      # Static assets
│   │   ├── css/
│   │   │   └── style.css               # Main stylesheet
│   │   └── js/
│   │       └── main.js                 # JavaScript utilities
│   │
│   ├── 📁 database/                    # Database layer
│   │   ├── __init__.py
│   │   ├── connection.py               # Database connection management
│   │   └── models.py                   # Data models and operations
│   │
│   ├── 📁 routes/                      # Route handlers
│   │   ├── __init__.py
│   │   ├── auth.py                     # Authentication routes
│   │   ├── dashboard.py                # Dashboard routes
│   │   ├── students.py                 # Student management routes
│   │   ├── rooms.py                    # Room management routes
│   │   ├── installments.py             # Payment management routes
│   │   └── settings.py                 # Settings routes
│   │
│   └── 📁 utils/                       # Utility functions
│       ├── __init__.py
│       ├── auth.py                     # Password hashing/verification
│       ├── email_service.py            # Email sending functionality
│       ├── room_manager.py             # Room allocation logic
│       └── installment_manager.py      # Payment calculations
│
└── 📁 .venv/                           # Python virtual environment
    └── (dependencies installed here)
```

### Directory Descriptions

| Directory | Purpose |
|-----------|---------|
| `app/` | Main application code |
| `app/templates/` | HTML pages and layouts |
| `app/static/` | CSS, JavaScript, images |
| `app/database/` | Database models and connections |
| `app/routes/` | URL routing and handlers |
| `app/utils/` | Reusable business logic |

## 🚀 Installation & Setup

### System Requirements

- **Python**: 3.7 or higher
- **OS**: macOS, Linux, or Windows
- **RAM**: 512 MB minimum
- **Disk Space**: 50 MB (including database)
- **Internet**: Required for Gmail email features

### Prerequisites

1. Python 3.7+ installed ([Download](https://www.python.org/downloads/))
2. Terminal/Command Prompt access
3. Git (optional, for cloning repository)

### Step-by-Step Installation

#### 1. Clone or Download Project

```bash
# Using git
git clone https://github.com/sandipan20/hotelmanager.git
cd hotelmanager

# Or download and extract ZIP file
cd /path/to/hotelmanager
```

#### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it (macOS/Linux)
source venv/bin/activate

# Activate it (Windows)
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

#### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Initialize Database

```bash
python3 run.py
```

The application will:
- Create SQLite database automatically
- Initialize all tables
- Create sample rooms
- Load sample data

#### 5. Access Application

```
Open your browser: http://localhost:5000
```

## 🎬 Getting Started

### First-Time Setup

1. **Open Application**
   - Navigate to `http://localhost:5000`

2. **Create Admin Account**
   - Click "Create an account"
   - Enter username and password
   - Click "Create Account"

3. **Login**
   - Use your credentials to log in
   - You'll see the dashboard

4. **Configure Settings** (Optional)
   - Click Settings
   - Enter Gmail credentials for email reminders
   - Save settings

5. **Add Students**
   - Click "Add Student"
   - Fill in all required fields
   - Submit to automatically allocate rooms

### Quick Actions

| Action | Steps |
|--------|-------|
| Add Student | Students → Add Student → Fill Form → Submit |
| View Students | Students → Browse List → Click View |
| Edit Student | Students → Click Edit → Update → Submit |
| Delete Student | Students → Click Delete → Confirm |
| Check Payments | Payments → Select Tab → View Status |
| Send Reminder | Payments → Click Send → Confirm |
| View Dashboard | Click Home/Dashboard icon |

## 📖 Usage Guide

### Managing Students

#### Adding a New Student

1. Navigate to **Students** → **Add Student**
2. Fill in all required fields:
   - **Personal Info**: Name, Date of Birth, Email
   - **Contact**: Mobile (10 digits), Emergency Contact
   - **Identification**: Aadhaar (12 digits)
   - **Education**: College, Admission Number
   - **Parent Info**: Parent names
   - **Address**: Full address
   - **Dates**: Registration and Session Expiration
   - **Fees**: Total Fee, Number of Installments
3. Click **Add Student**
4. System automatically:
   - Validates all inputs
   - Allocates available room
   - Creates installment records

#### Searching Students

1. Go to **Students** list
2. Use search box to find by:
   - Student name
   - Aadhaar number
   - Admission number
   - Email address
3. Results update instantly

#### Editing Student Info

1. Find student in list
2. Click **Edit**
3. Modify desired fields
4. Click **Update**

#### Removing a Student

1. Find student in list
2. Click **Delete**
3. Confirm deletion
4. Room is automatically freed

### Managing Rooms

#### Viewing Rooms

1. Click **Rooms** in navigation
2. See all rooms with:
   - Room number
   - Capacity
   - Current occupancy
   - Available spaces

#### Adjusting Capacity

1. Click **Rooms** → **Set Capacity**
2. Enter new capacity per room
3. Save changes
4. Affects future allocations

#### Adding Rooms

1. Use **Add Room** button
2. Enter room details
3. Confirm
4. Room is ready for allocation

### Managing Payments

#### Viewing Payment Status

1. Click **Payments** in navigation
2. Select tab:
   - **Pending**: Overdue payments (highlighted)
   - **Upcoming**: Due within 30 days
   - **All**: Complete payment history

#### Recording Payments

1. Find installment in list
2. Click **Mark as Paid**
3. Enter payment date (optional)
4. Confirm
5. Status updates immediately

#### Sending Reminders

**Send Individual Reminder:**
1. Click **Send Reminder** next to installment
2. Confirm email address
3. Email sent successfully

**Send Bulk Reminders:**
1. Click **Send All Reminders** button
2. Confirm
3. Emails sent to all students with overdue payments

#### Payment Statistics

Dashboard shows:
- Total pending payments
- Overdue payment count
- Total collected amount
- Payment success rate

### Email Configuration

#### Setup Gmail Integration

1. Go to **Settings**
2. Enter your Gmail address
3. Generate Gmail App Password:
   - Visit: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows PC" (or your device)
   - Generate password
4. Copy the 16-character password
5. Paste into "Gmail App Password" field
6. Click **Save Settings**

#### Test Email

1. In Settings, click **Send Test Email**
2. Confirmation message appears
3. Check your inbox

#### Troubleshooting Email

- Check 2-Step Verification is enabled
- Ensure app password (not regular password) is used
- Verify email address is correct
- Check internet connection

## 📊 Database Schema

The application uses SQLite3 with 7 tables optimized for hostel management. All tables have proper constraints, validations, and cascading operations.

### Database Statistics
- **Total Students**: 100 records
- **Total Rooms**: 25 records
- **Total Installments**: 400+ records
- **Total Payments**: 260+ records
- **Admin Users**: 3 records
- **Database Size**: ~500 KB

### Table 1: `students`
Stores all student information with validation and indexing.

```sql
CREATE TABLE students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    date_of_birth TEXT NOT NULL,
    mobile TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    aadhaar TEXT NOT NULL UNIQUE,
    admission_number TEXT UNIQUE,
    college TEXT,
    room_id INTEGER,
    parent_name_1 TEXT,
    parent_name_2 TEXT,
    emergency_contact TEXT,
    address TEXT,
    registration_date TEXT,
    session_expiration_date TEXT,
    total_fee REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES rooms(room_id) ON DELETE SET NULL
)
```

| Column | Type | Purpose |
|--------|------|---------|
| student_id | INTEGER | Unique identifier (auto-increment) |
| name | TEXT | Student's full name |
| date_of_birth | TEXT | Birth date (YYYY-MM-DD) |
| mobile | TEXT | Phone number (10 digits, unique) |
| email | TEXT | Email address (unique) |
| aadhaar | TEXT | Aadhaar ID (12 digits, unique) |
| admission_number | TEXT | College admission number |
| college | TEXT | College/University name |
| room_id | INTEGER | Assigned room (FK to rooms) |
| parent_name_1 | TEXT | Father/Guardian name |
| parent_name_2 | TEXT | Mother/Guardian name |
| emergency_contact | TEXT | Emergency contact number |
| address | TEXT | Full address |
| registration_date | TEXT | Registration date |
| session_expiration_date | TEXT | When student checks out |
| total_fee | REAL | Total fees for session |
| created_at | TIMESTAMP | Record creation time |

### Table 2: `rooms`
Stores room details with capacity management.

```sql
CREATE TABLE rooms (
    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_number TEXT NOT NULL UNIQUE,
    capacity INTEGER DEFAULT 4,
    occupancy INTEGER DEFAULT 0,
    status TEXT DEFAULT 'Vacant',
    floor INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

| Column | Type | Purpose |
|--------|------|---------|
| room_id | INTEGER | Unique identifier |
| room_number | TEXT | Room number (unique) |
| capacity | INTEGER | Max students per room |
| occupancy | INTEGER | Current number of students |
| status | TEXT | Vacant / Occupied / Full |
| floor | INTEGER | Floor number |
| created_at | TIMESTAMP | Creation time |

### Table 3: `installments`
Tracks payment installments with due dates and status.

```sql
CREATE TABLE installments (
    installment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    due_date TEXT NOT NULL,
    paid_date TEXT,
    status TEXT DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
)
```

| Column | Type | Purpose |
|--------|------|---------|
| installment_id | INTEGER | Unique identifier |
| student_id | INTEGER | Student ID (FK) |
| amount | REAL | Installment amount (₹) |
| due_date | TEXT | Payment due date |
| paid_date | TEXT | Actual payment date |
| status | TEXT | Pending / Paid / Overdue |
| created_at | TIMESTAMP | Creation time |

**Status Values**:
- **Pending**: Not yet due
- **Overdue**: Past due date, not paid
- **Paid**: Payment received

### Table 4: `payments`
Records actual payment transactions.

```sql
CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    installment_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    amount_paid REAL NOT NULL,
    payment_date TEXT NOT NULL,
    payment_method TEXT DEFAULT 'Cash',
    reference_number TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (installment_id) REFERENCES installments(installment_id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
)
```

| Column | Type | Purpose |
|--------|------|---------|
| payment_id | INTEGER | Unique identifier |
| installment_id | INTEGER | Installment ID (FK) |
| student_id | INTEGER | Student ID (FK) |
| amount_paid | REAL | Amount received (₹) |
| payment_date | TEXT | Payment received date |
| payment_method | TEXT | Cash / Check / Bank Transfer |
| reference_number | TEXT | Transaction reference |
| created_at | TIMESTAMP | Creation time |

### Table 5: `admin_users`
Stores admin account credentials (password hashed with bcrypt).

```sql
CREATE TABLE admin_users (
    admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
)
```

| Column | Type | Purpose |
|--------|------|---------|
| admin_id | INTEGER | Unique identifier |
| username | TEXT | Login username (unique) |
| password | TEXT | Bcrypt hashed password |
| email | TEXT | Admin email |
| created_at | TIMESTAMP | Account creation time |
| last_login | TIMESTAMP | Last login timestamp |

### Table 6: `settings`
Stores application configuration.

```sql
CREATE TABLE settings (
    setting_id INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_key TEXT NOT NULL UNIQUE,
    setting_value TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

**Key Settings**:
- `gmail_email` - Gmail address for sending reminders
- `gmail_app_password` - Gmail app-specific password (encrypted)
- `room_capacity` - Default capacity per room
- `session_timeout` - Session timeout in seconds

### Table 7: `sqlite_sequence`
Auto-maintained by SQLite (tracks auto-increment sequences).

```sql
CREATE TABLE sqlite_sequence (
    name TEXT,
    seq INTEGER
)
```

### Database Relationships

```
admin_users
     │
     └─── (authenticates)

settings
     │
     └─── (configures)

students
     ├─── (lives in) ──→ rooms
     ├─── (has) ──→ installments
     └─── (has) ──→ payments
          │
          └─── (tracks) ──→ installments

installments
     └─── (linked to) ──→ payments
```

### Data Integrity Constraints

1. **Unique Constraints**
   - Student mobile must be unique
   - Student email must be unique
   - Student Aadhaar must be unique
   - Room number must be unique
   - Admin username must be unique

2. **Foreign Key Constraints**
   - student_id in installments references students
   - student_id in payments references students
   - installment_id in payments references installments
   - room_id in students references rooms

3. **Cascading Operations**
   - DELETE student → automatically DELETE associated installments and payments
   - DELETE room → SET student room_id to NULL

4. **Validations**
   - Mobile: 10 digits
   - Aadhaar: 12 digits
   - Email: Valid email format
   - Amount: Positive numbers
   - Dates: YYYY-MM-DD format

## 🔌 API Routes

### Authentication Routes

#### `POST /auth/register`
Register a new admin account.

**Request Body:**
```json
{
  "username": "admin",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Account created successfully"
}
```

#### `POST /auth/login`
Login to the application.

**Request Body:**
```json
{
  "username": "admin",
  "password": "securepassword"
}
```

**Response:** Redirects to dashboard on success

#### `GET /auth/logout`
Logout current session.

### Dashboard Routes

#### `GET /`
Dashboard with statistics and overview.

**Returns:** Dashboard page with:
- Total students
- Total rooms
- Pending payments
- Recent activities

### Student Routes

#### `GET /students`
List all students with search capability.

**Query Parameters:**
- `search` - Search by name, Aadhaar, email, or admission number
- `page` - Page number (default: 1)

#### `GET /students/<student_id>`
View detailed information for a student.

#### `POST /students/add`
Add a new student.

**Request Body:**
```json
{
  "name": "John Doe",
  "date_of_birth": "2000-01-15",
  "mobile": "9876543210",
  "email": "john@example.com",
  "aadhaar": "123456789012",
  "college": "ABC University",
  "parent_name_1": "Father Name",
  "parent_name_2": "Mother Name",
  "emergency_contact": "9876543211",
  "address": "123 Main St, City",
  "registration_date": "2024-01-01",
  "session_expiration_date": "2024-06-30",
  "total_fee": 50000,
  "num_installments": 5
}
```

#### `POST /students/<student_id>/edit`
Update student information.

#### `POST /students/<student_id>/delete`
Delete a student (with confirmation).

### Room Routes

#### `GET /rooms`
List all rooms with occupancy status.

#### `POST /rooms/add`
Add a new room.

**Request Body:**
```json
{
  "room_number": "101",
  "capacity": 4,
  "floor": 1
}
```

#### `POST /rooms/<room_id>/edit`
Update room details.

#### `POST /rooms/set-capacity`
Update default capacity for all rooms.

**Request Body:**
```json
{
  "capacity": 4
}
```

### Payment Routes

#### `GET /installments`
View payment status (with tabs: pending, upcoming, all).

#### `GET /installments/pending`
List pending/overdue payments.

#### `GET /installments/upcoming`
List upcoming payments (within 30 days).

#### `POST /installments/<installment_id>/pay`
Mark an installment as paid.

**Request Body:**
```json
{
  "paid_date": "2024-01-15",
  "payment_method": "Cash"
}
```

#### `POST /installments/<installment_id>/send-reminder`
Send email reminder to student.

#### `POST /installments/send-all-reminders`
Send bulk reminder emails to all students with pending payments.

### Settings Routes

#### `GET /settings`
View application settings.

#### `POST /settings/email`
Update email configuration.

**Request Body:**
```json
{
  "gmail_email": "hostel@gmail.com",
  "gmail_app_password": "xxxx xxxx xxxx xxxx"
}
```

#### `POST /settings/test-email`
Send test email to configured address.

## ⚙️ Configuration

### Application Configuration (config.py)

```python
# Database
DATABASE_PATH = 'hostel_manager.db'
DATABASE_URL = f'sqlite:///{DATABASE_PATH}'

# Flask Settings
SECRET_KEY = 'your-secret-key-here'
DEBUG = True  # Set to False in production
TESTING = False

# Session Management
PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
SESSION_TIMEOUT = 3600  # seconds
SESSION_REFRESH_INTERVAL = 300  # 5 minutes

# Room Configuration
DEFAULT_ROOM_CAPACITY = 4
MAX_ROOMS = 100

# Email Settings
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
GMAIL_EMAIL = ''  # Set in settings page
GMAIL_APP_PASSWORD = ''  # Set in settings page

# Application Info
APP_NAME = 'Hostel Manager'
APP_VERSION = '1.0.0'
```

### Environment Variables (Optional)

Create a `.env` file in the project root:

```
FLASK_ENV=development
DATABASE_PATH=/path/to/hostel_manager.db
SECRET_KEY=your-secret-key-here
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

### Email Configuration

For Gmail integration:

1. Enable 2-Step Verification: https://myaccount.google.com/security
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use the 16-character password in settings

### Database Configuration

The SQLite database is automatically created on first run with:
- All required tables
- Proper indexes
- Cascading relationships
- 25 sample rooms
- 100 sample students (optional)

## 🔧 Troubleshooting

### Common Issues

#### Issue: "Database is locked"
**Cause**: Multiple processes accessing database simultaneously
**Solution**:
- Stop the application
- Wait 30 seconds
- Restart the application

#### Issue: "Port 5000 already in use"
**Cause**: Another application using port 5000
**Solutions**:
```bash
# Check what's using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>

# Or use a different port by editing config.py
# Flask will run on the new port
```

#### Issue: "Module not found" error
**Cause**: Dependencies not installed
**Solution**:
```bash
# Activate virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

#### Issue: "Email not sending"
**Causes & Solutions**:
- 2-Step Verification not enabled → Enable it in Google Account
- Using regular password instead of app password → Generate app password
- Incorrect email/password → Verify in Settings
- Firewall blocking SMTP → Check firewall settings

#### Issue: "Student can't be added"
**Causes & Solutions**:
- Duplicate mobile or email → Check if student already exists
- Invalid Aadhaar (not 12 digits) → Enter exactly 12 digits
- Invalid date format → Use YYYY-MM-DD format
- No rooms available → Add more rooms in Room Management
- Database locked → Restart application

#### Issue: "Login page keeps redirecting"
**Cause**: Session timeout
**Solution**:
- Clear browser cookies
- Restart the application
- Log in again

#### Issue: "Page loads slowly"
**Causes & Solutions**:
- Large student database → Use search to filter results
- Insufficient RAM → Close other applications
- Slow disk drive → Check available disk space
- No database indexes → Recreate database

### Getting Help

If issues persist:

1. **Check Application Logs**
   - Look for error messages in terminal
   - Check browser console (F12 → Console)

2. **Verify Configuration**
   - Confirm Python 3.7+ installed: `python3 --version`
   - Verify virtual environment active: `which python3`
   - Check database exists: `ls -la hostel_manager.db`

3. **Reset Application**
   ```bash
   # Stop current instance (Ctrl+C)
   
   # Optional: Delete database to reset
   rm hostel_manager.db
   
   # Restart
   python3 run.py
   ```

4. **Debug Mode**
   - Edit config.py: Set `DEBUG = True`
   - Restart application
   - Error messages will show more details

## 🤝 Contributing

Contributions are welcome! To contribute:

1. **Fork the Repository**
   - Click "Fork" on GitHub

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Changes**
   - Edit files as needed
   - Test thoroughly
   - Follow existing code style

4. **Test Your Changes**
   ```bash
   python3 run.py
   # Test all features in browser
   ```

5. **Commit & Push**
   ```bash
   git add .
   git commit -m "Add: Brief description of changes"
   git push origin feature/your-feature-name
   ```

6. **Submit Pull Request**
   - Describe your changes
   - Reference any issues fixed
   - Wait for review

### Code Style Guidelines

- Use meaningful variable names
- Add comments for complex logic
- Follow PEP 8 (Python style guide)
- Test all changes before committing
- Keep commits focused on single features

### Reporting Bugs

If you find a bug:

1. **Check if already reported** on GitHub Issues
2. **Create detailed bug report** including:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Screenshots (if applicable)
   - Error messages
   - Python/Flask/System info

### Feature Requests

To request a new feature:

1. Check if already suggested
2. Describe the feature clearly
3. Explain the use case
4. Suggest implementation (if possible)

## 📄 License

This project is licensed under the **MIT License** - see below for details.

### MIT License

```
MIT License

Copyright (c) 2024 Sandipan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```

## 📞 Contact & Support

- **Author**: Sandipan
- **GitHub**: [sandipan20](https://github.com/sandipan20)
- **Email**: For bug reports and feature requests, open an issue on GitHub
- **Support**: Full documentation available in this README

---

**Last Updated**: 2024  
**Version**: 1.0.0  
**Status**: Active Development

## 🗄️ Database Schema

### Students Table
```sql
CREATE TABLE students (
    aadhaar_number TEXT PRIMARY KEY,     -- 12-digit unique identifier
    full_name TEXT NOT NULL,              -- Student full name
    date_of_birth TEXT NOT NULL,         -- Date in YYYY-MM-DD
    mobile_number TEXT NOT NULL,         -- 10-digit mobile number
    college_name TEXT NOT NULL,          -- College name
    admission_number TEXT NOT NULL,      -- Unique admission number
    parent_names TEXT NOT NULL,          -- Parents' names
    gender TEXT NOT NULL,                -- Male/Female/Other
    registration_date TEXT NOT NULL,     -- Date in YYYY-MM-DD
    session_expiration_date TEXT NOT NULL, -- Date in YYYY-MM-DD
    full_address TEXT NOT NULL,          -- Complete address
    email TEXT NOT NULL,                 -- Email address
    emergency_contact TEXT NOT NULL,     -- Emergency contact info
    room_allocation TEXT,                -- Allocated room number
    total_fee REAL NOT NULL,             -- Total fee amount
    installment_count INTEGER NOT NULL,  -- Number of installments
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Installments Table
```sql
CREATE TABLE installments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aadhaar_number TEXT NOT NULL,        -- Link to student
    installment_number INTEGER NOT NULL,  -- Which installment (1, 2, 3...)
    due_date TEXT NOT NULL,              -- Date in YYYY-MM-DD
    amount REAL NOT NULL,                -- Amount for this installment
    payment_status TEXT DEFAULT 'Pending', -- 'Pending' or 'Paid'
    paid_date TEXT,                      -- When payment was made
    FOREIGN KEY (aadhaar_number) REFERENCES students(aadhaar_number) ON DELETE CASCADE,
    UNIQUE(aadhaar_number, installment_number)
);
```

### Rooms Table
```sql
CREATE TABLE rooms (
    room_number TEXT PRIMARY KEY,        -- Room identifier
    capacity INTEGER NOT NULL,           -- Max students per room
    occupied_count INTEGER DEFAULT 0     -- Current occupancy
);
```

### Admin Users Table
```sql
CREATE TABLE admin_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,       -- Admin username
    password_hash TEXT NOT NULL,         -- Hashed password
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Settings Table
```sql
CREATE TABLE settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
```

## 🎯 Features Overview

### Authentication & Security
- ✅ Secure password hashing using PBKDF2
- ✅ Session-based authentication
- ✅ Login-required protection on all admin pages
- ✅ Logout functionality

### Student Management
- ✅ Add up to 100 students
- ✅ Complete student information storage
- ✅ Data validation before saving
- ✅ Search and filter students
- ✅ Edit student information
- ✅ Delete student records
- ✅ View detailed student profiles

### Room Management
- ✅ Create and manage rooms
- ✅ Set room capacity dynamically
- ✅ Automatic room allocation
- ✅ Room occupancy tracking
- ✅ Capacity enforcement
- ✅ Auto-vacate rooms when student is deleted

### Payment Management
- ✅ Divide fees into installments
- ✅ Track payment status
- ✅ View overdue payments
- ✅ View upcoming payments
- ✅ Mark payments as paid
- ✅ Payment statistics dashboard

### Email Reminders
- ✅ Send individual payment reminders
- ✅ Send bulk reminders
- ✅ Gmail integration
- ✅ Customizable email templates

### Dashboard
- ✅ Total students count
- ✅ Total/occupied/vacant rooms
- ✅ Pending payment count
- ✅ Overdue payment count
- ✅ Quick action buttons

## 🔧 Troubleshooting

### Issue: "Port 5000 already in use"
**Solution:**
```bash
# Kill the process using port 5000
lsof -ti:5000 | xargs kill -9

# Or use a different port
python3 run.py  # Edit run.py to change port
```

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Install dependencies again
pip install -r requirements.txt
```

### Issue: "Database is locked"
**Solution:**
```bash
# Delete the database and restart
rm hostel_manager.db
python3 run.py
```

### Issue: "Email reminders not sending"
**Solution:**
1. Verify Gmail app password is correct (not regular password)
2. Check if 2-Step Verification is enabled in Google Account
3. Try sending a test email through Settings
4. Check email configuration in Settings

### Issue: "Can't allocate room to student"
**Solution:**
1. Go to Rooms and check capacity
2. Make sure rooms exist and have available capacity
3. You can add more rooms if needed

## 📝 Sample Data

The application comes with 5 sample rooms (Room-1 through Room-5) created during initial setup. You can:
- Add more rooms anytime
- Adjust room capacity
- Add sample students for testing

## 🆘 Getting Help

If you encounter any issues:
1. Check the troubleshooting section above
2. Verify all requirements are installed
3. Make sure Python 3.7+ is installed
4. Check that database file has proper permissions
5. Review error messages in the terminal

## 📞 Support

For questions or issues:
1. Review this README carefully
2. Check the application logs in terminal
3. Ensure all steps were followed correctly

---

**Hostel Manager v1.0**
Built for beginners, designed for stability, configured for success! 🚀
