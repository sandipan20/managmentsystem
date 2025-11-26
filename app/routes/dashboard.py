"""
Dashboard routes for Hostel Manager
"""

from flask import Blueprint, render_template, session, redirect, url_for
from app.routes.auth import login_required
from app.database.models import Student
from app.utils.room_manager import get_room_statistics
from app.utils.installment_manager import (
    get_payment_statistics,
    get_pending_installments,
    get_overdue_installments,
)

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def index():
    """Display the main dashboard"""
    # Get statistics
    total_students = Student.get_total_students_count()
    room_stats = get_room_statistics()
    # Use installment-based counts so dashboard matches Pending Payments page
    payment_stats = get_payment_statistics()

    pending_installments = get_pending_installments()
    overdue_installments = get_overdue_installments()

    try:
        total_pending = int(len(pending_installments))
    except Exception:
        total_pending = len(pending_installments)

    try:
        total_overdue = int(len(overdue_installments))
    except Exception:
        total_overdue = len(overdue_installments)

    # Sum amounts from pending_installments
    total_amount = 0.0
    for inst in pending_installments:
        try:
            total_amount += float(inst.get('amount') or 0)
        except Exception:
            continue

    stats = {
        'total_students': total_students,
        'total_rooms': room_stats['total_rooms'],
        'occupied_rooms': room_stats['occupied_rooms'],
        'vacant_rooms': room_stats['vacant_rooms'],
        'pending_payments': total_pending,
        'overdue_payments': total_overdue,
        'total_pending_amount': f"{total_amount:.2f}"
    }
    
    # Also pass explicit totals for templates or other consumers
    return render_template('dashboard/index.html',
                           stats=stats,
                           total_pending=total_pending,
                           total_overdue=total_overdue,
                           total_amount=total_amount)
