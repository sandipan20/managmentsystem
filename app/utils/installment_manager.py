"""
Installment management utilities for Hostel Manager
Handles payment tracking and installment calculations
"""

import sqlite3
from datetime import datetime, timedelta
from app.database.connection import get_db_connection

def create_installments(aadhaar_number, total_fee, installment_count, start_date_str):
    """
    Create installment records for a student
    
    Args:
        aadhaar_number: Student's Aadhaar number
        total_fee: Total amount to be paid
        installment_count: Number of installments
        start_date_str: Start date in format 'YYYY-MM-DD'
        
    Returns:
        Tuple (success: bool, message: str)
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Calculate amount per installment
        amount_per_installment = total_fee / installment_count
        
        # Parse start date
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        
        # Create installment records
        for i in range(1, installment_count + 1):
            # Due date is one month after previous due date
            due_date = start_date + timedelta(days=30 * i)
            
            cursor.execute('''
                INSERT INTO installments 
                (aadhaar_number, installment_number, due_date, amount, payment_status)
                VALUES (?, ?, ?, ?, 'Pending')
            ''', (aadhaar_number, i, due_date.strftime('%Y-%m-%d'), amount_per_installment))
        
        conn.commit()
        conn.close()
        
        return True, f"Created {installment_count} installments"
        
    except Exception as e:
        return False, f"Error: {str(e)}"

def get_student_installments(aadhaar_number):
    """Get all installments for a student"""
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM installments
        WHERE aadhaar_number = ?
        ORDER BY installment_number
    ''', (aadhaar_number,))
    
    installments = cursor.fetchall()
    conn.close()
    
    return [dict(inst) for inst in installments]

def mark_installment_paid(aadhaar_number, installment_number):
    """
    Mark an installment as paid
    
    Args:
        aadhaar_number: Student's Aadhaar number
        installment_number: Installment number
        
    Returns:
        Tuple (success: bool, message: str)
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        cursor.execute('''
            UPDATE installments
            SET payment_status = 'Paid', paid_date = ?
            WHERE aadhaar_number = ? AND installment_number = ?
        ''', (today, aadhaar_number, installment_number))
        
        conn.commit()
        conn.close()
        
        return True, "Installment marked as paid"
        
    except Exception as e:
        return False, f"Error: {str(e)}"

def get_overdue_installments():
    """Get all overdue installments across all students"""
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    cursor.execute('''
        SELECT s.full_name, s.email, s.aadhaar_number,
               i.installment_number, i.due_date, i.amount, i.payment_status
        FROM installments i
        JOIN students s ON i.aadhaar_number = s.aadhaar_number
        WHERE LOWER(i.payment_status) = 'pending' AND i.due_date < ?
        ORDER BY i.due_date ASC
    ''', (today,))
    
    installments = cursor.fetchall()
    conn.close()
    
    return [dict(inst) for inst in installments]

def get_pending_installments():
    """Get all pending installments across all students (regardless of due date)"""
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('''
        SELECT s.full_name, s.email, s.aadhaar_number,
               i.installment_number, i.due_date, i.amount, i.payment_status
        FROM installments i
        JOIN students s ON i.aadhaar_number = s.aadhaar_number
        WHERE LOWER(i.payment_status) = 'pending'
        ORDER BY i.due_date ASC
    ''')

    installments = cursor.fetchall()
    conn.close()

    return [dict(inst) for inst in installments]

def get_upcoming_installments(days_ahead=7):
    """Get installments due within the next N days"""
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    today = datetime.now().strftime('%Y-%m-%d')
    future_date = (datetime.now() + timedelta(days=days_ahead)).strftime('%Y-%m-%d')
    
    cursor.execute('''
        SELECT s.full_name, s.email, s.aadhaar_number,
               i.installment_number, i.due_date, i.amount, i.payment_status
        FROM installments i
        JOIN students s ON i.aadhaar_number = s.aadhaar_number
        WHERE LOWER(i.payment_status) = 'pending' AND i.due_date BETWEEN ? AND ?
        ORDER BY i.due_date ASC
    ''', (today, future_date))
    
    installments = cursor.fetchall()
    conn.close()
    
    return [dict(inst) for inst in installments]

def get_payment_statistics():
    """Get payment statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Total payments
    cursor.execute('SELECT COUNT(*) FROM installments')
    total_installments = cursor.fetchone()[0]
    
    # Paid payments
    cursor.execute('SELECT COUNT(*) FROM installments WHERE LOWER(payment_status) = ?', ('paid',))
    paid_installments = cursor.fetchone()[0]
    
    # Pending payments
    cursor.execute('SELECT COUNT(*) FROM installments WHERE LOWER(payment_status) = ?', ('pending',))
    pending_installments = cursor.fetchone()[0]
    
    # Total amount pending
    cursor.execute('SELECT SUM(amount) FROM installments WHERE LOWER(payment_status) = ?', ('pending',))
    total_pending = cursor.fetchone()[0] or 0
    
    # Overdue count
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('''
        SELECT COUNT(*) FROM installments 
        WHERE LOWER(payment_status) = 'pending' AND due_date < ?
    ''', (today,))
    overdue_count = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'total_installments': total_installments,
        'paid_installments': paid_installments,
        'pending_installments': pending_installments,
        'total_pending_amount': total_pending,
        'overdue_count': overdue_count
    }

def delete_student_installments(aadhaar_number):
    """Delete all installments for a student (called when student is deleted)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM installments WHERE aadhaar_number = ?', (aadhaar_number,))
        
        conn.commit()
        conn.close()
        
        return True, "Installments deleted"
        
    except Exception as e:
        return False, f"Error: {str(e)}"
