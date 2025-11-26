"""
Room management routes for Hostel Manager
"""

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from app.routes.auth import login_required
from app.utils.room_manager import (
    create_room, get_all_rooms, get_available_rooms,
    get_room_statistics, set_room_capacity, get_room_capacity,
    update_room_capacity_for_all
)
from app.utils.room_manager import vacate_student

rooms_bp = Blueprint('rooms', __name__, url_prefix='/rooms')

@rooms_bp.route('/')
@login_required
def list_rooms():
    """Display all rooms"""
    rooms = get_all_rooms()
    stats = get_room_statistics()
    current_capacity = get_room_capacity()
    
    return render_template('rooms/list.html',
                         rooms=rooms,
                         stats=stats,
                         current_capacity=current_capacity)

@rooms_bp.route('/create', methods=['POST'])
@login_required
def add_room():
    """Create a new room"""
    room_number = request.form.get('room_number', '').strip()
    
    if not room_number:
        flash('Room number is required', 'error')
        return redirect(url_for('rooms.list_rooms'))
    
    success, message = create_room(room_number)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    return redirect(url_for('rooms.list_rooms'))

@rooms_bp.route('/available')
@login_required
def get_available():
    """Get list of available rooms"""
    rooms = get_available_rooms()
    return jsonify({'rooms': rooms})

@rooms_bp.route('/capacity', methods=['GET', 'POST'])
@login_required
def manage_capacity():
    """Manage room capacity settings"""
    if request.method == 'POST':
        capacity = request.form.get('capacity', '').strip()
        
        if not capacity:
            return render_template('rooms/capacity.html',
                                 error='Capacity is required',
                                 current_capacity=get_room_capacity())
        
        try:
            capacity = int(capacity)
            if capacity <= 0:
                return render_template('rooms/capacity.html',
                                     error='Capacity must be greater than 0',
                                     current_capacity=get_room_capacity())
            
            success, message = update_room_capacity_for_all(capacity)
            
            if success:
                return render_template('rooms/capacity.html',
                                     success='Room capacity updated successfully!',
                                     current_capacity=capacity)
            else:
                return render_template('rooms/capacity.html',
                                     error=message,
                                     current_capacity=get_room_capacity())
                
        except ValueError:
            return render_template('rooms/capacity.html',
                                 error='Capacity must be a valid number',
                                 current_capacity=get_room_capacity())
    
    return render_template('rooms/capacity.html',
                         current_capacity=get_room_capacity())

@rooms_bp.route('/<room_number>')
@login_required
def view_room(room_number):
    """View a specific room with occupancy details"""
    rooms = get_all_rooms()
    room = next((r for r in rooms if r.get('room_number') == room_number), None)
    
    if not room:
        flash(f'Room {room_number} not found', 'error')
        return redirect(url_for('rooms.list_rooms')), 404
    
    # Get students in this room
    from app.database.connection import get_db_connection
    import sqlite3
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        SELECT aadhaar_number, full_name, email, mobile_number
        FROM students
        WHERE room_allocation = ?
        ORDER BY full_name
    ''', (room_number,))
    students_in_room = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return render_template('rooms/detail.html', room=room, students=students_in_room)


@rooms_bp.route('/<room_number>/vacate/<aadhaar>', methods=['POST'])
@login_required
def vacate_student_route(room_number, aadhaar):
    """Vacate a student from a room (called from room detail page)"""
    success, message, prev_room = vacate_student(aadhaar)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    return redirect(url_for('rooms.view_room', room_number=room_number))

@rooms_bp.route('/<room_number>/edit', methods=['GET', 'POST'])
@login_required
def edit_room(room_number):
    """Edit room capacity"""
    rooms = get_all_rooms()
    room = next((r for r in rooms if r.get('room_number') == room_number), None)
    
    if not room:
        flash(f'Room {room_number} not found', 'error')
        return redirect(url_for('rooms.list_rooms')), 404
    
    if request.method == 'POST':
        new_capacity = request.form.get('capacity', '').strip()
        
        if not new_capacity:
            return render_template('rooms/edit.html', room=room, error='Capacity is required')
        
        try:
            capacity = int(new_capacity)
            if capacity <= 0:
                return render_template('rooms/edit.html', room=room, error='Capacity must be greater than 0')
            
            # Update this specific room's capacity
            from app.database.connection import get_db_connection
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE rooms SET capacity = ? WHERE room_number = ?', (capacity, room_number))
            conn.commit()
            conn.close()
            
            flash(f'Room {room_number} capacity updated to {capacity}', 'success')
            return redirect(url_for('rooms.list_rooms'))
        
        except ValueError:
            return render_template('rooms/edit.html', room=room, error='Capacity must be a valid number')
    
    return render_template('rooms/edit.html', room=room)

@rooms_bp.route('/<room_number>/delete', methods=['POST'])
@login_required
def delete_room(room_number):
    """Delete a room"""
    try:
        from app.database.connection import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if room has students
        cursor.execute('SELECT COUNT(*) FROM students WHERE room_allocation = ?', (room_number,))
        count = cursor.fetchone()[0]
        
        if count > 0:
            conn.close()
            flash(f'Cannot delete room {room_number}: {count} student(s) allocated to it', 'error')
            return redirect(url_for('rooms.list_rooms'))
        
        # Delete the room
        cursor.execute('DELETE FROM rooms WHERE room_number = ?', (room_number,))
        conn.commit()
        conn.close()
        
        flash(f'Room {room_number} deleted successfully', 'success')
        return redirect(url_for('rooms.list_rooms'))
    
    except Exception as e:
        flash(f'Error deleting room: {str(e)}', 'error')
        return redirect(url_for('rooms.list_rooms'))
