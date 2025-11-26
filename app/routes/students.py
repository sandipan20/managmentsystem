"""
Student management routes for Hostel Manager
"""

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app.routes.auth import login_required
from app.database.models import Student
from app.utils.room_manager import allocate_room_to_student
from app.utils.room_manager import assign_student_to_room, vacate_student
from app.utils.installment_manager import create_installments, get_student_installments
from app.utils.room_manager import get_available_rooms

students_bp = Blueprint('students', __name__, url_prefix='/students')

@students_bp.route('/')
@login_required
def list_students():
    """Display list of all students"""
    students = Student.get_all_students()
    return render_template('students/list.html', students=students)

@students_bp.route('/search')
@login_required
def search():
    """Search students by name, admission number, or Aadhaar"""
    query = request.args.get('q', '').strip()
    
    if not query or len(query) < 2:
        return jsonify({'results': []})
    
    students = Student.search_students(query)
    
    return jsonify({
        'results': students
    })

@students_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_student():
    """Add a new student"""
    if request.method == 'POST':
        try:
            data = {
                'full_name': request.form.get('full_name', '').strip(),
                'date_of_birth': request.form.get('date_of_birth', ''),
                'mobile_number': request.form.get('mobile_number', '').strip(),
                'college_name': request.form.get('college_name', '').strip(),
                'admission_number': request.form.get('admission_number', '').strip(),
                'parent_names': request.form.get('parent_names', '').strip(),
                'aadhaar_number': request.form.get('aadhaar_number', '').strip(),
                'gender': request.form.get('gender', ''),
                'registration_date': request.form.get('registration_date', ''),
                'session_expiration_date': request.form.get('session_expiration_date', ''),
                'full_address': request.form.get('full_address', '').strip(),
                'email': request.form.get('email', '').strip(),
                'emergency_contact': request.form.get('emergency_contact', '').strip(),
                'total_fee': request.form.get('total_fee', 0),
                'installment_count': request.form.get('installment_count', 1)
            }
            
            # Validate required fields
            required_fields = ['full_name', 'date_of_birth', 'mobile_number', 'college_name',
                             'admission_number', 'parent_names', 'aadhaar_number', 'gender',
                             'registration_date', 'session_expiration_date', 'full_address',
                             'email', 'emergency_contact', 'total_fee', 'installment_count']
            
            missing_fields = [f for f in required_fields if not data[f]]
            if missing_fields:
                return render_template('students/add.html',
                                     error=f"Missing required fields: {', '.join(missing_fields)}")
            
            # Add student to database
            success, message = Student.add_student(data)
            
            if success:
                aadhaar = data['aadhaar_number']
                
                # Allocate room
                room_success, room_number, room_msg = allocate_room_to_student(aadhaar)
                
                # Create installments
                inst_success, inst_msg = create_installments(
                    aadhaar,
                    float(data['total_fee']),
                    int(data['installment_count']),
                    data['registration_date']
                )
                
                return render_template('students/add.html',
                                     success='Student added successfully!')
            else:
                return render_template('students/add.html', error=message)
                
        except Exception as e:
            return render_template('students/add.html',
                                 error=f"An error occurred: {str(e)}")
    
    return render_template('students/add.html')

@students_bp.route('/<aadhaar>')
@login_required
def view_student(aadhaar):
    """View detailed information about a specific student"""
    student = Student.get_student_by_aadhaar(aadhaar)
    
    if not student:
        return render_template('error.html',
                             error='Student not found'), 404
    
    # Get installments
    installments = get_student_installments(aadhaar)
    # Get available rooms for assignment dropdown
    available_rooms = get_available_rooms()
    
    return render_template('students/detail.html',
                         student=student,
                         installments=installments,
                         available_rooms=available_rooms)

@students_bp.route('/<aadhaar>/edit', methods=['GET', 'POST'])
@login_required
def edit_student(aadhaar):
    """Edit student information"""
    student = Student.get_student_by_aadhaar(aadhaar)
    
    if not student:
        return render_template('error.html', error='Student not found'), 404
    
    if request.method == 'POST':
        try:
            data = {
                'full_name': request.form.get('full_name', '').strip(),
                'mobile_number': request.form.get('mobile_number', '').strip(),
                'parent_names': request.form.get('parent_names', '').strip(),
                'full_address': request.form.get('full_address', '').strip(),
                'email': request.form.get('email', '').strip(),
                'emergency_contact': request.form.get('emergency_contact', '').strip(),
                'session_expiration_date': request.form.get('session_expiration_date', '')
            }
            
            # Remove empty values
            data = {k: v for k, v in data.items() if v}
            
            if not data:
                return render_template('students/edit.html',
                                     student=student,
                                     error='No fields to update')
            
            success, message = Student.update_student(aadhaar, data)
            
            if success:
                # Refresh student data
                student = Student.get_student_by_aadhaar(aadhaar)
                return render_template('students/edit.html',
                                     student=student,
                                     success='Student updated successfully!')
            else:
                return render_template('students/edit.html',
                                     student=student,
                                     error=message)
                
        except Exception as e:
            return render_template('students/edit.html',
                                 student=student,
                                 error=f"An error occurred: {str(e)}")
    
    return render_template('students/edit.html', student=student)


@students_bp.route('/<aadhaar>/assign', methods=['POST'])
@login_required
def assign_student(aadhaar):
    """Assign a student to a room via student page"""
    room_number = request.form.get('room_number', '').strip()
    if not room_number:
        return jsonify({'success': False, 'message': 'Room number is required'}), 400

    success, message = assign_student_to_room(aadhaar, room_number)
    if success:
        return jsonify({'success': True, 'message': message}), 200
    else:
        return jsonify({'success': False, 'message': message}), 400


@students_bp.route('/<aadhaar>/vacate', methods=['POST'])
@login_required
def vacate_student_from_studentpage(aadhaar):
    success, message, prev_room = vacate_student(aadhaar)
    if success:
        return jsonify({'success': True, 'message': message}), 200
    else:
        return jsonify({'success': False, 'message': message}), 400

@students_bp.route('/<aadhaar>/delete', methods=['POST'])
@login_required
def delete_student(aadhaar):
    """Delete a student record"""
    success, message = Student.delete_student(aadhaar)
    
    if success:
        return jsonify({'success': True, 'message': message}), 200
    else:
        return jsonify({'success': False, 'message': message}), 400
