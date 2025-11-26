"""
Installment and payment routes for Hostel Manager
"""

from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
from app.routes.auth import login_required
from app.utils.installment_manager import (
    get_student_installments, mark_installment_paid,
    get_overdue_installments, get_upcoming_installments,
    get_payment_statistics, get_pending_installments
)
from app.utils.email_service import send_reminder_email, send_bulk_reminders
from app.database.models import Student

installments_bp = Blueprint('installments', __name__, url_prefix='/installments')

def calculate_overdue_days(due_date_str):
    """
    Calculate number of days overdue given a due date string.
    
    Args:
        due_date_str: Date string in 'YYYY-MM-DD' format
        
    Returns:
        Number of days overdue (positive if past due, 0 if today, negative if future)
    """
    try:
        if isinstance(due_date_str, str):
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        else:
            due_date = due_date_str
        today = datetime.now().date()
        return (today - due_date).days
    except Exception:
        return 0

@installments_bp.route('/student/<aadhaar>')
@login_required
def student_installments(aadhaar):
    """View installments for a specific student"""
    student = Student.get_student_by_aadhaar(aadhaar)
    
    if not student:
        return render_template('error.html', error='Student not found'), 404
    
    installments = get_student_installments(aadhaar)
    
    return render_template('installments/student_installments.html',
                         student=student,
                         installments=installments)

@installments_bp.route('/mark-paid', methods=['POST'])
@login_required
def mark_paid():
    """Mark an installment as paid"""
    aadhaar = request.form.get('aadhaar_number', '').strip()
    installment_number = request.form.get('installment_number', '').strip()
    
    if not aadhaar or not installment_number:
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400
    
    try:
        success, message = mark_installment_paid(aadhaar, int(installment_number))
        
        if success:
            return jsonify({'success': True, 'message': message}), 200
        else:
            return jsonify({'success': False, 'message': message}), 400
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@installments_bp.route('/pending')
@login_required
def view_pending():
    """View all pending payments"""
    # Get all pending installments regardless of due date
    pending_installments = get_pending_installments()
    stats = get_payment_statistics()

    overdue_installments = []
    total_amount = 0.0
    today = datetime.now().date()

    # Normalize status comparisons and parse due dates into date objects
    for inst in pending_installments:
        # Ensure status comparison is case-insensitive
        status = inst.get('payment_status') or ''
        inst['payment_status_normalized'] = status.strip().lower()

        # Parse due_date into a date object when possible
        due_date = inst.get('due_date')
        try:
            if isinstance(due_date, str):
                due_date_obj = datetime.strptime(due_date, '%Y-%m-%d').date()
            else:
                due_date_obj = due_date
        except Exception:
            due_date_obj = None

        inst['due_date_obj'] = due_date_obj

        # Compute overdue
        if due_date_obj and due_date_obj < today:
            inst['overdue_days'] = (today - due_date_obj).days
            overdue_installments.append(inst)
        else:
            inst['overdue_days'] = 0

        # Sum amount safely
        try:
            amt = float(inst.get('amount') or 0)
        except Exception:
            amt = 0.0
        total_amount += amt

    total_pending = len(pending_installments)
    total_overdue = len(overdue_installments)

    # Update stats dict so the summary banners (which read from `stats`) reflect
    # the same computed values used for the table below.
    try:
        stats['pending_installments'] = int(total_pending)
    except Exception:
        stats['pending_installments'] = total_pending

    try:
        stats['overdue_count'] = int(total_overdue)
    except Exception:
        stats['overdue_count'] = total_overdue

    try:
        stats['total_pending_amount'] = float(total_amount)
    except Exception:
        stats['total_pending_amount'] = total_amount

    return render_template('installments/pending.html',
                         pending_installments=pending_installments,
                         installments=pending_installments,
                         overdue_installments=overdue_installments,
                         total_pending=total_pending,
                         total_overdue=total_overdue,
                         total_amount=total_amount,
                         stats=stats,
                         type='pending')

@installments_bp.route('/upcoming')
@login_required
def view_upcoming():
    """View upcoming payments"""
    installments = get_upcoming_installments(days_ahead=30)
    stats = get_payment_statistics()
    
    # Add days_until_due to each installment for cleaner template rendering
    for inst in installments:
        days_until = -calculate_overdue_days(inst.get('due_date', ''))
        inst['days_until_due'] = max(0, days_until)
    
    return render_template('installments/upcoming.html',
                         installments=installments,
                         stats=stats,
                         type='upcoming')

@installments_bp.route('/send-reminder/<aadhaar>/<int:installment_number>', methods=['POST'])
@login_required
def send_reminder(aadhaar, installment_number):
    """Send a reminder email for a specific installment"""
    student = Student.get_student_by_aadhaar(aadhaar)
    installments = get_student_installments(aadhaar)
    
    if not student:
        return jsonify({'success': False, 'message': 'Student not found'}), 404
    
    # Find the specific installment
    installment = None
    for inst in installments:
        if inst['installment_number'] == installment_number:
            installment = inst
            break
    
    if not installment:
        return jsonify({'success': False, 'message': 'Installment not found'}), 404
    
    success, message = send_reminder_email(
        student['email'],
        student['full_name'],
        installment['amount'],
        installment['due_date']
    )
    
    if success:
        return jsonify({'success': True, 'message': message}), 200
    else:
        return jsonify({'success': False, 'message': message}), 400

@installments_bp.route('/send-bulk-reminders', methods=['POST'])
@login_required
def send_bulk_reminders_route():
    """Send reminder emails to all students with overdue payments"""
    overdue_installments = get_overdue_installments()
    
    # Group by student
    students_dict = {}
    for inst in overdue_installments:
        aadhaar = inst['aadhaar_number']
        if aadhaar not in students_dict:
            students_dict[aadhaar] = {
                'full_name': inst['full_name'],
                'email': inst['email'],
                'amount': inst['amount'],
                'due_date': inst['due_date']
            }
    
    overdue_students = list(students_dict.values())
    total, sent, failed, errors = send_bulk_reminders(overdue_students)
    
    return jsonify({
        'success': True,
        'total': total,
        'sent': sent,
        'failed': failed,
        'errors': errors
    }), 200

@installments_bp.route('/statistics')
@login_required
def statistics():
    """View payment statistics"""
    stats = get_payment_statistics()
    overdue = get_overdue_installments()
    upcoming = get_upcoming_installments(days_ahead=30)
    
    return render_template('installments/statistics.html',
                         stats=stats,
                         overdue_count=len(overdue),
                         upcoming_count=len(upcoming))
