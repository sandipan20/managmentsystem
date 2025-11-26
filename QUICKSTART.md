# 🚀 QUICK START GUIDE

Welcome to Hostel Manager! This guide will get you up and running in 5 minutes.

## Prerequisites
- macOS with Terminal
- Python 3.7 or higher (check with `python3 --version`)

## 5-Minute Setup

### Step 1: Navigate to the Project
```bash
cd /Users/sandy/Documents/hostelmanagment
```

### Step 2: Make Start Script Executable (First Time Only)
```bash
chmod +x start.sh
```

### Step 3: Run the Start Script
```bash
./start.sh
```

The script will:
- ✅ Create a virtual environment
- ✅ Install all dependencies
- ✅ Start the Flask server

### Step 4: Open in Browser
Once you see "Starting Hostel Manager...", open:
```
http://localhost:5000
```

### Step 5: Create Admin Account
1. Click "Create an account" (or go to http://localhost:5000/setup)
2. Enter a username and password
3. Click "Create Admin Account"
4. You'll see "Admin user created successfully"
5. Click the login button or go back to http://localhost:5000/login
6. Enter your credentials and login

### Step 6: Start Using!
You're now logged in to the Hostel Manager dashboard!

- 📚 **Add Students**: Click "Add Student" to register new students
- 🏠 **Manage Rooms**: Click "Rooms" to view and manage rooms
- 💳 **Track Payments**: Click "Payments" to track installments
- ⚙️ **Configure Email**: Click "Settings" to set up email reminders

## Manual Setup (If start.sh doesn't work)

```bash
# Step 1: Navigate to project
cd /Users/sandy/Documents/hostelmanagment

# Step 2: Create virtual environment
python3 -m venv venv

# Step 3: Activate virtual environment
source venv/bin/activate

# Step 4: Install dependencies
pip install -r requirements.txt

# Step 5: Run the application
python3 run.py
```

## Stopping the Server

Press **Ctrl+C** in the terminal where the server is running.

## Next Time You Start

Just run:
```bash
cd /Users/sandy/Documents/hostelmanagment
./start.sh
```

Or manually:
```bash
cd /Users/sandy/Documents/hostelmanagment
source venv/bin/activate
python3 run.py
```

## Sample Data

5 sample rooms (Room-1 through Room-5) are automatically created when you first set up the admin account. You can add more rooms or modify the existing ones through the "Rooms" section.

## Common Issues

**❌ "Port 5000 already in use"**
```bash
# Kill the process
lsof -ti:5000 | xargs kill -9
# Then run again
python3 run.py
```

**❌ "ModuleNotFoundError: No module named 'flask'"**
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**❌ Can't create admin account**
- Check if you're at http://localhost:5000/setup
- Make sure the database file is writable
- Clear your browser cache

## Need Help?

1. Check the README.md for detailed documentation
2. Verify Python 3.7+ is installed
3. Make sure you've activated the virtual environment
4. Check terminal for error messages

---

**Happy Hostel Managing! 🏨**
