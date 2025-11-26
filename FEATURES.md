# 🎯 COMPLETE FEATURES GUIDE

Comprehensive guide to all features in Hostel Manager.

## Dashboard

The first page you see after login shows:

- **Total Students**: Number of students registered
- **Total Rooms**: Number of rooms available
- **Occupied Rooms**: Rooms with students
- **Vacant Rooms**: Empty rooms
- **Pending Payments**: Installments not yet paid
- **Overdue Payments**: Past-due installments
- **Total Pending Amount**: Sum of all unpaid installments

### Quick Actions
- Add New Student
- Manage Rooms
- View Pending Payments

---

## 👥 Student Management

### Adding a Student

Click "Add Student" or "Add New Student" button.

**Personal Information Section:**
- Full Name
- Date of Birth (calendar picker)
- Mobile Number (exactly 10 digits)
- Email Address
- Parent Names (both parents)
- Emergency Contact (name and phone)
- Full Address
- Gender (Male/Female/Other)

**College & Registration Section:**
- College Name
- Admission Number
- Registration Date (when admitted)
- Session Expiration Date (when to vacate)

**Fee & Payment Section:**
- Total Fee (total amount to collect)
- Number of Installments (1-12 options)

**Validation:**
- All fields are required
- Aadhaar must be exactly 12 digits
- Mobile must be exactly 10 digits
- Email must be valid format

**What Happens After Adding:**
1. Student record is saved to database
2. Installments are automatically created
3. Room is automatically allocated if available
4. Student appears in the student list

### Viewing Students

Click "Students" in navigation.

**Features:**
- View all students in a table
- Search by:
  - Full name
  - Admission number
  - Aadhaar number
  - Email address
- Click "View" to see full details
- Click "Edit" to modify information
- Click "Delete" to remove (with confirmation)

### Student Detail Page

Shows complete information including:
- Personal details
- College & hostel information
- Allocated room
- Fee breakdown
- All installments with payment status
- Payment history

### Editing Student

Click "Edit" button on student detail page or list.

**Editable Fields:**
- Full Name
- Mobile Number
- Email
- Parent Names
- Emergency Contact
- Full Address
- Session Expiration Date

**Non-Editable Fields (for data integrity):**
- Aadhaar Number
- Admission Number
- College Name
- Other registration details

### Deleting Student

1. Click "Delete" button (red button)
2. Confirm action
3. System will:
   - Remove all student records
   - Remove all installment records
   - Vacate the room
   - Remove payment history

**⚠️ Important:** Deletion cannot be undone!

---

## 🏠 Room Management

### Viewing Rooms

Click "Rooms" in navigation.

Shows:
- **Statistics Card** showing:
  - Total rooms count
  - Occupied rooms count
  - Vacant rooms count
  - Current capacity (students per room)

- **Room Grid** with each room showing:
  - Room number
  - Current occupancy (e.g., "2 / 2")
  - Status (Vacant, Partially Occupied, or Full)
  - Occupancy progress bar

### Adding Rooms

1. Click "Add New Room" button
2. Enter room number/identifier (e.g., "A-101", "Room-1", "Dorm-A")
3. Click "Create Room"
4. New room appears in the room grid

### Setting Room Capacity

1. Click "Set Capacity" button
2. Enter maximum students per room
3. Click "Update Capacity"
4. All existing rooms are updated
5. New students will be allocated according to new capacity

**Capacity Management:**
- Affects all rooms equally
- Impacts future student allocations
- Student already assigned remain in their rooms
- Can be changed anytime

### Automatic Room Allocation

When a student is added:
1. System finds a room with available capacity
2. Student is assigned to that room
3. Room occupancy is updated
4. Student can see their room in their detail page

---

## 💳 Payment & Installment Management

### Understanding Installments

When you add a student with:
- Total Fee: ₹6000
- Number of Installments: 3

System creates:
- Installment 1: ₹2000 due 30 days from registration
- Installment 2: ₹2000 due 60 days from registration
- Installment 3: ₹2000 due 90 days from registration

### Viewing Installments

**Student Installments Page:**
- Click on "View Details" on student's detail page
- Shows all installments for that student
- Status (Paid/Pending)
- Payment date if paid

**Pending Payments:**
- Click "Payments" → "Pending Payments"
- Shows all overdue payments across all students
- Click on student to view details
- Send individual reminders

**Upcoming Payments:**
- Click "Payments" → "Upcoming Payments"
- Shows payments due in next 30 days
- Early warning system

### Marking Payment as Paid

1. Find the installment
2. Click "Mark Paid" button
3. Payment is recorded with today's date
4. Status changes to "Paid"
5. Installment appears in statistics as paid

### Payment Statistics

View in:
- Dashboard (overview)
- Payments → Statistics page

Shows:
- Total installments
- Paid installments (count)
- Pending installments (count)
- Total pending amount (sum of unpaid)
- Overdue count

---

## 📧 Email Reminders

### Setting Up Email

1. Click "Settings" in navigation
2. Enter Gmail address
3. Generate App Password:
   - Visit https://myaccount.google.com/apppasswords
   - Sign in if needed
   - Select "Mail" from dropdown
   - Select "Mac" from device dropdown
   - Google generates 16-character password
   - Copy the password
4. Paste password in the form
5. Click "Save Email Settings"

**⚠️ Important:** Use an App Password, not your regular Gmail password!

### Sending Individual Reminders

1. Go to "Payments" → "Pending Payments"
2. Find the student
3. Click "Send Reminder" button
4. Email is sent to student with:
   - Amount due
   - Due date
   - Friendly reminder message

### Sending Bulk Reminders

1. Go to "Payments" → "Pending Payments"
2. Click "Send All Reminders" button
3. System sends emails to all students with overdue payments
4. Shows summary of sent/failed

### Email Content

Students receive:
```
Subject: Hostel Fee Reminder - Payment Overdue

Dear [Student Name],

This is a reminder that your hostel fee payment is overdue.

Payment Details:
- Amount Due: ₹[Amount]
- Due Date: [Date]

Please make the payment as soon as possible. 
Contact the hostel office if you have any questions.

Best regards,
Hostel Management
```

---

## ⚙️ Settings

### Email Configuration

- Gmail Address: Your Gmail email
- Gmail App Password: 16-character app password
- SMTP Server: smtp.gmail.com (default)
- SMTP Port: 587 (default)

### Why Email Matters

- Automate payment reminders
- Reduce follow-up work
- Ensure timely payments
- Professional communication

---

## 🔐 Security & Sessions

### Admin Login

- Username and password required
- Passwords are securely hashed
- Cannot see password in database
- Sessions expire after 1 hour of inactivity

### Protected Pages

All pages require login except:
- /login (login page)
- /setup (initial admin account creation)

### Logout

- Click "Logout" in navigation
- Session is cleared
- Must login again to access dashboard

---

## 📊 Dashboard Statistics

### Understanding the Numbers

**Total Students**: All registered students in system

**Total Rooms**: All rooms created in system

**Occupied Rooms**: Rooms with at least one student

**Vacant Rooms**: Rooms with zero students

**Pending Payments**: Unpaid installments

**Overdue Payments**: Payments past their due date

### Real-Time Updates

- Click "Dashboard" to refresh statistics
- Counts update automatically
- Based on current database state

---

## 🔍 Search & Filter

### Quick Search

On students list page:
1. Type in search box
2. Minimum 2 characters required
3. Search across:
   - Full name
   - Admission number
   - Aadhaar number
   - Email address
4. Results appear instantly

### Sorting

Tables are sortable by:
- Clicking column headers (in some tables)
- Data sorted automatically

---

## 📱 Mobile & Responsive

The application works on:
- Desktop computers
- Tablets
- Mobile phones

Layout adapts automatically for smaller screens.

---

## 💾 Data Persistence

### Database

- All data stored in `hostel_manager.db` file
- SQLite format
- Located in project root directory
- Automatically created on first run

### Backup

To backup your data:
```bash
cp hostel_manager.db hostel_manager.db.backup
```

To restore:
```bash
cp hostel_manager.db.backup hostel_manager.db
```

---

## ✨ Best Practices

### For Administrators

1. **Regular Backups**: Backup database regularly
2. **Email Configuration**: Set up email for reminders
3. **Room Planning**: Create enough rooms for expected students
4. **Payment Tracking**: Check pending payments weekly
5. **Security**: Change default admin password
6. **Testing**: Add a test student first to get familiar

### For Data Entry

1. **Verify Data**: Double-check before saving
2. **Aadhaar Format**: Always use 12 digits
3. **Phone Format**: Always use 10 digits
4. **Dates**: Use calendar picker for consistency
5. **Email Format**: Ensure valid email addresses

### For Payment Tracking

1. **Set Due Dates**: Carefully plan installment schedules
2. **Send Reminders**: Send at least 5 days before due date
3. **Mark Payments**: Record immediately after receipt
4. **Follow Up**: Check overdue payments weekly
5. **Archive**: Keep payment records for audit trail

---

## 🆘 Feature Troubleshooting

### Students not getting emails
1. Check Settings → Email Configuration
2. Verify Gmail address and app password
3. Check Gmail account has 2-Step Verification enabled
4. Try sending test email

### Room allocation failing
1. Check if rooms exist (go to Rooms)
2. Check room capacity (should be > 0)
3. Check if rooms have available slots
4. Add more rooms if needed

### Can't delete student
1. Check if student exists
2. Ensure you have admin access
3. Try refreshing the page
4. Check browser console for errors

### Payment statistics incorrect
1. Refresh the page
2. Check installment status (Paid/Pending)
3. Ensure students were added with installments
4. Try deleting and re-adding test student

---

## 📞 Help & Support

For detailed help:
1. Check README.md (complete documentation)
2. Check QUICKSTART.md (quick setup)
3. Check INSTALLATION.md (setup guide)
4. Review error messages in browser console

---

**Master all features and become a Hostel Manager expert! 🏨**
