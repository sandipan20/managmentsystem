"""
Email utilities for Hostel Manager
Handles sending reminder emails for overdue payments
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.database.connection import get_db_connection

def get_email_config():
    """
    Get email configuration from settings table
    
    Returns:
        Dictionary with email config (sender_email, sender_password, smtp_server, smtp_port)
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT key, value FROM settings WHERE key LIKE ?', ('%email%',))
    settings = cursor.fetchall()
    conn.close()
    
    config = {}
    for key, value in settings:
        config[key] = value
    
    return config

def save_email_config(sender_email, sender_password, smtp_server='smtp.gmail.com', smtp_port='587'):
    """
    Save email configuration to settings table
    
    Args:
        sender_email: Gmail email address
        sender_password: Gmail app password or password
        smtp_server: SMTP server address
        smtp_port: SMTP port
        
    Returns:
        Tuple (success: bool, message: str)
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Save or update email settings
        cursor.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)',
                      ('email_sender', sender_email))
        cursor.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)',
                      ('email_password', sender_password))
        cursor.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)',
                      ('smtp_server', smtp_server))
        cursor.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)',
                      ('smtp_port', smtp_port))
        
        conn.commit()
        conn.close()
        
        return True, "Email configuration saved successfully"
        
    except Exception as e:
        return False, f"Error: {str(e)}"

def send_reminder_email(recipient_email, student_name, amount, due_date):
    """
    Send a reminder email for overdue payment
    
    Args:
        recipient_email: Email address to send to
        student_name: Name of the student
        amount: Amount due
        due_date: Due date of the payment
        
    Returns:
        Tuple (success: bool, message: str)
    """
    try:
        config = get_email_config()
        
        if not config.get('email_sender') or not config.get('email_password'):
            return False, "Email configuration not set. Please configure email settings first."
        
        sender_email = config['email_sender']
        sender_password = config['email_password']
        smtp_server = config.get('smtp_server', 'smtp.gmail.com')
        smtp_port = int(config.get('smtp_port', 587))
        
        # Create email message
        subject = f"Hostel Fee Reminder - Payment Overdue"
        body = f"""
Dear {student_name},

This is a reminder that your hostel fee payment is overdue.

Payment Details:
- Amount Due: ₹{amount}
- Due Date: {due_date}

Please make the payment as soon as possible. Contact the hostel office if you have any questions.

Best regards,
Hostel Management
        """
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        
        return True, f"Reminder email sent to {recipient_email}"
        
    except smtplib.SMTPAuthenticationError:
        return False, "Email authentication failed. Check your email and password."
    except Exception as e:
        return False, f"Error sending email: {str(e)}"

def send_bulk_reminders(overdue_students):
    """
    Send reminder emails to multiple students with overdue payments
    
    Args:
        overdue_students: List of dictionaries with student and payment info
        
    Returns:
        Tuple (total: int, sent: int, failed: int, errors: list)
    """
    total = len(overdue_students)
    sent = 0
    failed = 0
    errors = []
    
    for student in overdue_students:
        success, message = send_reminder_email(
            student['email'],
            student['full_name'],
            student['amount'],
            student['due_date']
        )
        
        if success:
            sent += 1
        else:
            failed += 1
            errors.append(f"{student['full_name']}: {message}")
    
    return total, sent, failed, errors
