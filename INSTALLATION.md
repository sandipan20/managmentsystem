# 📦 INSTALLATION GUIDE

Detailed step-by-step installation instructions for Hostel Manager.

## System Requirements

- **Operating System**: macOS, Linux, or Windows
- **Python**: Python 3.7 or higher
- **Storage**: ~50 MB free disk space
- **RAM**: 512 MB minimum
- **Browser**: Any modern browser (Chrome, Firefox, Safari, Edge)

## Verification: Check if Python is Installed

Open Terminal and run:
```bash
python3 --version
```

You should see something like:
```
Python 3.13.7
```

If you see "command not found", install Python from https://www.python.org/downloads/

## Complete Installation (macOS)

### Option 1: Using the Start Script (Recommended)

```bash
# Step 1: Navigate to project folder
cd /Users/sandy/Documents/hostelmanagment

# Step 2: Make script executable (first time only)
chmod +x start.sh

# Step 3: Run the script
./start.sh
```

The script will automatically:
- Create a Python virtual environment
- Install all dependencies
- Start the application server

### Option 2: Manual Installation

#### Step 1: Open Terminal
Press `Cmd + Space`, type "Terminal", and press Enter

#### Step 2: Navigate to Project Directory
```bash
cd /Users/sandy/Documents/hostelmanagment
```

#### Step 3: Create Virtual Environment
A virtual environment isolates this project's dependencies:
```bash
python3 -m venv venv
```

#### Step 4: Activate Virtual Environment
```bash
source venv/bin/activate
```

You should see `(venv)` at the beginning of your terminal line, like:
```
(venv) sandy@MacBook hostelmanagment %
```

#### Step 5: Install Python Dependencies
```bash
pip install -r requirements.txt
```

This installs Flask and other required packages.

#### Step 6: Run the Application
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
```

## Accessing the Application

1. Open your web browser
2. Go to: `http://localhost:5000`
3. You should see the Hostel Manager login page

## Initial Setup

### Creating Admin Account (First Time Only)

1. On the login page, click "Create an account" or go to http://localhost:5000/setup
2. Fill in:
   - **Username**: Enter a username (minimum 3 characters)
   - **Password**: Enter a password (minimum 6 characters)
   - **Confirm Password**: Re-enter the password
3. Click "Create Admin Account"
4. Go back to login and enter your credentials

### After Login

You'll see the dashboard with:
- Total Students count
- Total Rooms count
- Occupied/Vacant rooms
- Pending payments

## File Structure After Installation

```
hostelmanagment/
├── venv/                    # Virtual environment (created during setup)
├── app/                     # Application code
│   ├── templates/          # HTML files
│   ├── static/             # CSS, JavaScript
│   ├── database/           # Database models
│   ├── routes/             # Application routes
│   └── utils/              # Utility functions
├── run.py                  # Main application file
├── requirements.txt        # Python dependencies
├── config.py              # Configuration settings
├── README.md              # Full documentation
├── QUICKSTART.md          # Quick start guide
├── start.sh               # Start script
└── hostel_manager.db      # SQLite database (created after first run)
```

## Stopping the Application

1. Go to the Terminal window where the server is running
2. Press **Ctrl + C**
3. You should see "KeyboardInterrupt"

The server will stop, and you can safely close Terminal.

## Starting Again (Next Time)

### Quick Start
```bash
cd /Users/sandy/Documents/hostelmanagment
./start.sh
```

### Manual Start
```bash
cd /Users/sandy/Documents/hostelmanagment
source venv/bin/activate
python3 run.py
```

## Installing Optional Features

### Email Reminders (Gmail)

To enable email reminders:

1. Login to the application
2. Go to Settings → Email Configuration
3. Enter your Gmail address
4. Generate an App Password:
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Mac"
   - Copy the 16-character password
5. Paste it in the Email Configuration form
6. Click "Save Email Settings"

## Troubleshooting Installation

### Problem: "python3: command not found"
**Solution**: Install Python from https://www.python.org/downloads/

### Problem: "Permission denied" for start.sh
**Solution**:
```bash
chmod +x start.sh
./start.sh
```

### Problem: Virtual environment won't activate
**Solution**:
```bash
# Delete and recreate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
```

### Problem: "ModuleNotFoundError: No module named 'flask'"
**Solution**:
```bash
# Make sure venv is activated
source venv/bin/activate

# Reinstall packages
pip install -r requirements.txt
```

### Problem: "Port 5000 already in use"
**Solution**:
```bash
# Find and kill the process
lsof -ti:5000 | xargs kill -9

# Or restart your computer
```

### Problem: Database errors
**Solution**:
```bash
# Delete the database and restart
rm hostel_manager.db
python3 run.py
```

## Verify Installation

To verify everything is installed correctly:

```bash
cd /Users/sandy/Documents/hostelmanagment
source venv/bin/activate
python3 -c "from app import create_app; app = create_app(); print('✅ Installation successful!')"
```

You should see:
```
✅ Installation successful!
```

## Next Steps

1. Read the QUICKSTART.md for a 5-minute quick start
2. Read README.md for detailed feature documentation
3. Check out the Settings page to configure email
4. Add sample data by running: `python3 init_sample_data.py`

## Getting Help

If you encounter any issues:

1. **Check Terminal Output**: Read error messages carefully
2. **Verify Python Version**: `python3 --version` (should be 3.7+)
3. **Check Virtual Environment**: Look for `(venv)` in terminal
4. **Review README.md**: Contains troubleshooting section
5. **Try Fresh Installation**: Delete venv and start over

## System-Specific Notes

### macOS
- Use `python3` (not `python`)
- Terminal is in `/Applications/Utilities/`
- Use `cmd + space` to open Spotlight and search for Terminal

### Linux
- Same as macOS instructions
- May need to install `python3-venv`: `sudo apt-get install python3-venv`

### Windows
- Use `python` instead of `python3`
- Use `venv\Scripts\activate` instead of `source venv/bin/activate`
- Use backslashes for paths

---

**Installation Complete! Ready to manage your hostel. 🏨**
