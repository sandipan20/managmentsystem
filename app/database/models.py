"""
Database models for Hostel Manager
Defines the Student table structure with all required fields
"""

import sqlite3
from datetime import datetime
from app.database.connection import get_db_connection

class Student:
    """Student model for database operations"""
    
    @staticmethod
    def create_table():
        """Create the students table with all required fields"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                aadhaar_number TEXT PRIMARY KEY,
                full_name TEXT NOT NULL,
                date_of_birth TEXT NOT NULL,
                mobile_number TEXT NOT NULL,
                college_name TEXT NOT NULL,
                admission_number TEXT NOT NULL UNIQUE,
                parent_names TEXT NOT NULL,
                gender TEXT NOT NULL,
                registration_date TEXT NOT NULL,
                session_expiration_date TEXT NOT NULL,
                full_address TEXT NOT NULL,
                email TEXT NOT NULL,
                emergency_contact TEXT NOT NULL,
                room_allocation TEXT,
                total_fee REAL NOT NULL,
                installment_count INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create installments table for tracking payments
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS installments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aadhaar_number TEXT NOT NULL,
                installment_number INTEGER NOT NULL,
                due_date TEXT NOT NULL,
                amount REAL NOT NULL,
                payment_status TEXT DEFAULT 'Pending',
                paid_date TEXT,
                FOREIGN KEY (aadhaar_number) REFERENCES students(aadhaar_number) ON DELETE CASCADE,
                UNIQUE(aadhaar_number, installment_number)
            )
        ''')
        
        # Create room allocation table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rooms (
                room_number TEXT PRIMARY KEY,
                capacity INTEGER NOT NULL,
                occupied_count INTEGER DEFAULT 0
            )
        ''')
        
        # Create admin table for login
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admin_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create settings table for capacity and email config
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def add_student(data):
        """
        Add a new student to the database
        
        Args:
            data: Dictionary containing student information
            
        Returns:
            Tuple (success: bool, message: str)
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Validate 12-digit Aadhaar number
            aadhaar = data.get('aadhaar_number', '').strip()
            if not aadhaar.isdigit() or len(aadhaar) != 12:
                return False, "Aadhaar number must be exactly 12 digits"
            
            # Validate mobile number (10 digits)
            mobile = data.get('mobile_number', '').strip()
            if not mobile.isdigit() or len(mobile) != 10:
                return False, "Mobile number must be exactly 10 digits"
            
            cursor.execute('''
                INSERT INTO students (
                    aadhaar_number, full_name, date_of_birth, mobile_number,
                    college_name, admission_number, parent_names, gender,
                    registration_date, session_expiration_date, full_address,
                    email, emergency_contact, room_allocation, total_fee,
                    installment_count
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                aadhaar,
                data.get('full_name'),
                data.get('date_of_birth'),
                mobile,
                data.get('college_name'),
                data.get('admission_number'),
                data.get('parent_names'),
                data.get('gender'),
                data.get('registration_date'),
                data.get('session_expiration_date'),
                data.get('full_address'),
                data.get('email'),
                data.get('emergency_contact'),
                data.get('room_allocation', 'Not Allocated'),
                float(data.get('total_fee', 0)),
                int(data.get('installment_count', 1))
            ))
            
            conn.commit()
            conn.close()
            return True, "Student added successfully"
            
        except sqlite3.IntegrityError as e:
            return False, f"Error: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"
    
    @staticmethod
    def get_all_students():
        """Get all students from the database"""
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM students ORDER BY registration_date DESC')
        students = cursor.fetchall()
        conn.close()
        
        return [dict(student) for student in students]
    
    @staticmethod
    def search_students(query):
        """
        Search students by name, admission number, or Aadhaar
        
        Args:
            query: Search string
            
        Returns:
            List of matching student records
        """
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        search_param = f"%{query}%"
        cursor.execute('''
            SELECT * FROM students 
            WHERE full_name LIKE ? OR admission_number LIKE ? 
               OR aadhaar_number LIKE ? OR email LIKE ?
            ORDER BY registration_date DESC
        ''', (search_param, search_param, search_param, search_param))
        
        students = cursor.fetchall()
        conn.close()
        
        return [dict(student) for student in students]
    
    @staticmethod
    def get_student_by_aadhaar(aadhaar_number):
        """Get a specific student by Aadhaar number"""
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM students WHERE aadhaar_number = ?', (aadhaar_number,))
        student = cursor.fetchone()
        conn.close()
        
        return dict(student) if student else None
    
    @staticmethod
    def update_student(aadhaar_number, data):
        """
        Update student information
        
        Args:
            aadhaar_number: Student's Aadhaar number (primary key)
            data: Dictionary with fields to update
            
        Returns:
            Tuple (success: bool, message: str)
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Validate mobile number if provided
            if 'mobile_number' in data:
                mobile = data['mobile_number'].strip()
                if not mobile.isdigit() or len(mobile) != 10:
                    return False, "Mobile number must be exactly 10 digits"
            
            # Build dynamic UPDATE query
            update_fields = []
            values = []
            
            for key, value in data.items():
                if key != 'aadhaar_number':
                    update_fields.append(f"{key} = ?")
                    values.append(value)
            
            if not update_fields:
                return False, "No fields to update"
            
            values.append(aadhaar_number)
            query = f"UPDATE students SET {', '.join(update_fields)} WHERE aadhaar_number = ?"
            
            cursor.execute(query, values)
            conn.commit()
            conn.close()
            
            return True, "Student updated successfully"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def delete_student(aadhaar_number):
        """
        Delete a student and their installment records
        
        Args:
            aadhaar_number: Student's Aadhaar number
            
        Returns:
            Tuple (success: bool, message: str)
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Get student's room allocation before deletion
            cursor.execute('SELECT room_allocation FROM students WHERE aadhaar_number = ?', 
                          (aadhaar_number,))
            student = cursor.fetchone()
            
            if student and student[0] and student[0] != 'Not Allocated':
                # Vacate the room
                cursor.execute('''
                    UPDATE rooms SET occupied_count = occupied_count - 1 
                    WHERE room_number = ?
                ''', (student[0],))
            
            # Delete student (cascade delete will handle installments)
            cursor.execute('DELETE FROM students WHERE aadhaar_number = ?', (aadhaar_number,))
            
            conn.commit()
            conn.close()
            
            return True, "Student deleted successfully"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def get_total_students_count():
        """Get total number of students"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM students')
        count = cursor.fetchone()[0]
        conn.close()
        return count
