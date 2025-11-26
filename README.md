# 🏨 Hostel Manager - Complete Documentation

A beginner-friendly, full-stack web application for managing hostel students, rooms, payments, and sending email reminders. Built with Python Flask, SQLite, and vanilla HTML/CSS/JavaScript.

## 📋 Table of Contents

1. [Features](#features)
2. [Project Structure](#project-structure)
3. [Installation & Setup](#installation--setup)
4. [Usage](#usage)
5. [Database Schema](#database-schema)
6. [Features Overview](#features-overview)
7. [Troubleshooting](#troubleshooting)

## ✨ Features

### Core Features
- **Admin Login System** - Secure login with hashed passwords and Flask sessions
- **Student Management** - Add, edit, view, search, and delete student records
- **Student Data Validation** - All data is validated before saving to ensure data integrity
- **Room Management** - Create rooms and manage room allocation automatically
- **Dynamic Room Allocation** - Students are automatically assigned to available rooms
- **Installment Tracking** - Divide fees into multiple installments with due dates
- **Payment Management** - Mark payments as paid and track payment status
- **Email Reminders** - Send Gmail reminders for overdue payments
- **Dashboard** - Overview of students, rooms, and payment statistics
- **Responsive Design** - Works on desktop and mobile devices

### Advanced Features
- **Cascading Deletion** - When a student is deleted, their room is automatically vacated
- **Room Capacity Management** - Set how many students per room
- **Bulk Email Reminders** - Send reminders to all students with overdue payments
- **Payment Statistics** - View pending, paid, and overdue payment counts
- **Search & Filter** - Find students by name, admission number, Aadhaar, or email

## 📁 Project Structure

```
hostelmanagment/
├── app/
│   ├── __init__.py                 # Flask app factory
│   ├── templates/
│   │   ├── base.html              # Base template with navigation
│   │   ├── auth/
│   │   │   ├── login.html         # Login page
│   │   │   └── setup.html         # Initial admin setup
│   │   ├── dashboard/
│   │   │   └── index.html         # Main dashboard
│   │   ├── students/
│   │   │   ├── list.html          # List all students
│   │   │   ├── add.html           # Add new student
│   │   │   ├── detail.html        # Student details
│   │   │   └── edit.html          # Edit student
│   │   ├── rooms/
│   │   │   ├── list.html          # List all rooms
│   │   │   └── capacity.html      # Room capacity settings
│   │   ├── installments/
│   │   │   ├── student_installments.html  # Student's installments
│   │   │   ├── pending.html               # Overdue payments
│   │   │   └── upcoming.html              # Upcoming payments
│   │   └── settings/
│   │       └── email.html         # Email configuration
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css          # Main stylesheet
│   │   └── js/
│   │       └── main.js            # JavaScript utilities
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py          # Database connection
│   │   └── models.py              # Student model and database operations
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py                # Login/logout routes
│   │   ├── dashboard.py           # Dashboard route
│   │   ├── students.py            # Student management routes
│   │   ├── rooms.py               # Room management routes
│   │   ├── installments.py        # Payment and installment routes
│   │   └── settings.py            # Settings routes
│   └── utils/
│       ├── __init__.py
│       ├── auth.py                # Password hashing and verification
│       ├── email_service.py       # Email sending functionality
│       ├── room_manager.py        # Room allocation logic
│       └── installment_manager.py # Payment calculations
├── run.py                         # Application entry point
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🚀 Installation & Setup

### Prerequisites
- **Python 3.7+** installed on your machine
- **macOS** (works on other OS too)
- **Terminal/Command Prompt** access

### Step 1: Download/Clone Project

```bash
cd /Users/sandy/Documents/hostelmanagment
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

You should see `(venv)` prefix in your terminal.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
python3 run.py
```

You should see:
```
🏨 Hostel Manager Application
============================================================

✓ Database initialized

🚀 Starting Hostel Manager server...
📍 Access the application at: http://localhost:5000

Initial Setup:
1. Open http://localhost:5000 in your browser
2. Click 'Create an account' to set up your admin account
3. Log in with your credentials
```

### Step 5: Open in Browser

1. Go to `http://localhost:5000` in your web browser
2. Click "Create an account"
3. Create your first admin user (username and password)
4. Log in with your credentials
5. Start managing students!

## 📖 Usage

### Adding a Student

1. Click "Add Student" in the navigation
2. Fill in all required fields:
   - Personal information (name, date of birth, mobile, email)
   - Aadhaar number (must be exactly 12 digits)
   - Parent names and emergency contact
   - Full address
   - College details
   - Registration and session dates
   - Total fee and number of installments
3. Click "Add Student"
4. The system will automatically:
   - Validate all data
   - Allocate a room if available
   - Create installment records

### Viewing Students

1. Click "Students" in navigation to see all students
2. Use the search box to find students by:
   - Full name
   - Admission number
   - Aadhaar number
   - Email address
3. Click "View" to see detailed information
4. Click "Edit" to modify student information
5. Click "Delete" to remove a student (with confirmation)

### Managing Rooms

1. Click "Rooms" in navigation
2. View all rooms with occupancy status
3. Add new rooms with the "Add New Room" button
4. Click "Set Capacity" to configure how many students per room
5. Rooms automatically show:
   - Current occupancy
   - Available capacity
   - Status (Vacant, Partially Occupied, Full)

### Managing Payments

1. Click "Payments" → "Pending Payments" to see overdue payments
2. Click on a student to see their installment details
3. Actions available:
   - **Mark Paid** - Record a payment
   - **Send Reminder** - Email reminder to student
   - **Send All Reminders** - Bulk email to all students with overdue payments
4. View upcoming payments within 30 days

### Configuring Email Reminders

1. Click "Settings" in navigation
2. Enter your Gmail address
3. Generate and enter a Gmail App Password:
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Mac"
   - Copy the 16-character app password
   - Paste it in the "Gmail App Password" field
4. Click "Save Email Settings"
5. Test by sending a reminder email

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
