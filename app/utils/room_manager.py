"""
Room management utilities for Hostel Manager
Handles room allocation and capacity management
"""

import sqlite3
from app.database.connection import get_db_connection

def set_room_capacity(capacity):
    """
    Set the maximum capacity per room
    
    Args:
        capacity: Number of students allowed per room
        
    Returns:
        Tuple (success: bool, message: str)
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)',
                      ('room_capacity', str(capacity)))
        
        conn.commit()
        conn.close()
        
        return True, f"Room capacity set to {capacity} students per room"
        
    except Exception as e:
        return False, f"Error: {str(e)}"

def get_room_capacity():
    """Get the current room capacity setting"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT value FROM settings WHERE key = ?', ('room_capacity',))
    result = cursor.fetchone()
    conn.close()
    
    return int(result[0]) if result else 2  # Default to 2 students per room

def create_room(room_number):
    """
    Create a new room in the system
    
    Args:
        room_number: Room number/identifier
        
    Returns:
        Tuple (success: bool, message: str)
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        capacity = get_room_capacity()
        
        cursor.execute('''
            INSERT INTO rooms (room_number, capacity, occupied_count)
            VALUES (?, ?, 0)
        ''', (room_number, capacity))
        
        conn.commit()
        conn.close()
        
        return True, f"Room {room_number} created successfully"
        
    except sqlite3.IntegrityError:
        return False, f"Room {room_number} already exists"
    except Exception as e:
        return False, f"Error: {str(e)}"

def get_all_rooms():
    """Get all rooms with their occupancy status.

    Occupied counts are computed dynamically by counting students
    allocated to each room to avoid stale `occupied_count` values.
    """
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('''
        SELECT r.room_number, r.capacity,
               COUNT(s.aadhaar_number) as occupied_count,
               (r.capacity - COUNT(s.aadhaar_number)) as vacant_count
        FROM rooms r
        LEFT JOIN students s ON s.room_allocation = r.room_number
        GROUP BY r.room_number, r.capacity
        ORDER BY r.room_number
    ''')

    rooms = cursor.fetchall()
    conn.close()

    # Ensure numeric types and sensible defaults
    result = []
    for r in rooms:
        row = dict(r)
        row['occupied_count'] = int(row.get('occupied_count') or 0)
        row['capacity'] = int(row.get('capacity') or 0)
        row['vacant_count'] = int(row.get('vacant_count') or 0)
        result.append(row)

    return result

def get_available_rooms():
    """Get rooms that have available capacity (computed dynamically)."""
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('''
        SELECT r.room_number, r.capacity,
               COUNT(s.aadhaar_number) as occupied_count,
               (r.capacity - COUNT(s.aadhaar_number)) as vacant_count
        FROM rooms r
        LEFT JOIN students s ON s.room_allocation = r.room_number
        GROUP BY r.room_number, r.capacity
        HAVING occupied_count < r.capacity
        ORDER BY r.room_number
    ''')

    rooms = cursor.fetchall()
    conn.close()

    result = []
    for r in rooms:
        row = dict(r)
        row['occupied_count'] = int(row.get('occupied_count') or 0)
        row['capacity'] = int(row.get('capacity') or 0)
        row['vacant_count'] = int(row.get('vacant_count') or 0)
        result.append(row)

    return result

def allocate_room_to_student(aadhaar_number):
    """
    Automatically allocate an available room to a student
    
    Args:
        aadhaar_number: Student's Aadhaar number
        
    Returns:
        Tuple (success: bool, room_number: str or None, message: str)
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Find an available room (compute occupancy dynamically)
        cursor.execute('''
            SELECT r.room_number, r.capacity, COUNT(s.aadhaar_number) as occupied
            FROM rooms r
            LEFT JOIN students s ON s.room_allocation = r.room_number
            GROUP BY r.room_number, r.capacity
            HAVING occupied < r.capacity
            LIMIT 1
        ''')

        room = cursor.fetchone()
        
        if not room:
            conn.close()
            return False, None, "No available rooms"
        
        room_number = room[0]
        
        # Update student record with allocated room
        cursor.execute('''
            UPDATE students SET room_allocation = ?
            WHERE aadhaar_number = ?
        ''', (room_number, aadhaar_number))
        
        conn.commit()
        conn.close()
        
        return True, room_number, f"Student allocated to room {room_number}"
        
    except Exception as e:
        return False, None, f"Error: {str(e)}"


def vacate_student(aadhaar_number):
    """Vacate a student from their current room allocation."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Find current allocation
        cursor.execute('SELECT room_allocation FROM students WHERE aadhaar_number = ?', (aadhaar_number,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return False, 'Student not found', None

        current = row[0]
        if not current or current == 'Not Allocated':
            conn.close()
            return False, 'Student is not allocated to any room', None

        # Set to Not Allocated
        cursor.execute('UPDATE students SET room_allocation = ? WHERE aadhaar_number = ?', ('Not Allocated', aadhaar_number))
        conn.commit()
        conn.close()

        return True, f'Student vacated from room {current}', current

    except Exception as e:
        return False, f'Error: {str(e)}', None


def assign_student_to_room(aadhaar_number, room_number):
    """Assign or move a student into a specific room, respecting capacity."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verify room exists and get capacity
        cursor.execute('SELECT capacity FROM rooms WHERE room_number = ?', (room_number,))
        room = cursor.fetchone()
        if not room:
            conn.close()
            return False, 'Room not found'

        capacity = int(room[0])

        # Count current occupants
        cursor.execute('SELECT COUNT(*) FROM students WHERE room_allocation = ?', (room_number,))
        occupied = cursor.fetchone()[0]

        if occupied >= capacity:
            conn.close()
            return False, 'Room is full'

        # Assign student
        cursor.execute('UPDATE students SET room_allocation = ? WHERE aadhaar_number = ?', (room_number, aadhaar_number))
        conn.commit()
        conn.close()

        return True, f'Student assigned to room {room_number}'

    except Exception as e:
        return False, f'Error: {str(e)}'

def get_room_statistics():
    """Get room statistics"""
    rooms = get_all_rooms()
    
    total_rooms = len(rooms)
    total_capacity = sum(r['capacity'] for r in rooms)
    occupied_count = sum(r['occupied_count'] for r in rooms)
    vacant_count = total_capacity - occupied_count
    
    return {
        'total_rooms': total_rooms,
        'total_capacity': total_capacity,
        'occupied_rooms': sum(1 for r in rooms if r['occupied_count'] > 0),
        'vacant_rooms': sum(1 for r in rooms if r['occupied_count'] < r['capacity']),
        'total_occupied': occupied_count,
        'total_vacant': vacant_count
    }

def update_room_capacity_for_all(new_capacity):
    """
    Update room capacity for all existing rooms
    
    Args:
        new_capacity: New capacity value
        
    Returns:
        Tuple (success: bool, message: str)
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Update all rooms
        cursor.execute('UPDATE rooms SET capacity = ?', (new_capacity,))
        
        # Update setting
        cursor.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)',
                      ('room_capacity', str(new_capacity)))
        
        conn.commit()
        conn.close()
        
        return True, f"Room capacity updated to {new_capacity} for all rooms"
        
    except Exception as e:
        return False, f"Error: {str(e)}"
