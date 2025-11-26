"""
Sample data initialization script for Hostel Manager
Run this after creating an admin account to populate the system with sample data
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.database.models import Student
from app.database.connection import get_db_connection, init_db
from app.utils.installment_manager import create_installments
from app.utils.room_manager import create_room, get_all_rooms

def create_sample_students():
    """Create sample student records"""
    sample_students = [
        {
            'full_name': 'Rahul Kumar',
            'date_of_birth': '2004-05-15',
            'mobile_number': '9876543210',
            'college_name': 'Delhi Institute of Technology',
            'admission_number': 'DIT-2023-001',
            'parent_names': 'Mr. Rajesh Kumar and Mrs. Priya Kumar',
            'aadhaar_number': '123456789012',
            'gender': 'Male',
            'registration_date': '2023-09-01',
            'session_expiration_date': '2024-06-30',
            'full_address': '123, Sector 12, New Delhi, Delhi - 110009',
            'email': 'rahul.kumar@college.com',
            'emergency_contact': 'Mrs. Priya Kumar - 9876543210',
            'total_fee': 50000,
            'installment_count': 2
        },
        {
            'full_name': 'Priya Sharma',
            'date_of_birth': '2004-08-22',
            'mobile_number': '8765432109',
            'college_name': 'Delhi Institute of Technology',
            'admission_number': 'DIT-2023-002',
            'parent_names': 'Mr. Vikram Sharma and Mrs. Neha Sharma',
            'aadhaar_number': '234567890123',
            'gender': 'Female',
            'registration_date': '2023-09-01',
            'session_expiration_date': '2024-06-30',
            'full_address': '456, MG Road, New Delhi, Delhi - 110010',
            'email': 'priya.sharma@college.com',
            'emergency_contact': 'Mr. Vikram Sharma - 8765432109',
            'total_fee': 50000,
            'installment_count': 2
        },
        {
            'full_name': 'Amit Singh',
            'date_of_birth': '2003-12-10',
            'mobile_number': '7654321098',
            'college_name': 'Delhi Institute of Technology',
            'admission_number': 'DIT-2023-003',
            'parent_names': 'Mr. Rajendra Singh and Mrs. Sunita Singh',
            'aadhaar_number': '345678901234',
            'gender': 'Male',
            'registration_date': '2023-09-01',
            'session_expiration_date': '2024-06-30',
            'full_address': '789, South Delhi, New Delhi, Delhi - 110011',
            'email': 'amit.singh@college.com',
            'emergency_contact': 'Mr. Rajendra Singh - 7654321098',
            'total_fee': 60000,
            'installment_count': 3
        },
        {
            'full_name': 'Anjali Verma',
            'date_of_birth': '2004-03-05',
            'mobile_number': '6543210987',
            'college_name': 'Delhi Institute of Technology',
            'admission_number': 'DIT-2023-004',
            'parent_names': 'Mr. Ashok Verma and Mrs. Kavya Verma',
            'aadhaar_number': '456789012345',
            'gender': 'Female',
            'registration_date': '2023-09-01',
            'session_expiration_date': '2024-06-30',
            'full_address': '321, West Delhi, New Delhi, Delhi - 110012',
            'email': 'anjali.verma@college.com',
            'emergency_contact': 'Mrs. Kavya Verma - 6543210987',
            'total_fee': 50000,
            'installment_count': 2
        },
        {
            'full_name': 'Ravi Patel',
            'date_of_birth': '2004-07-18',
            'mobile_number': '5432109876',
            'college_name': 'Delhi Institute of Technology',
            'admission_number': 'DIT-2023-005',
            'parent_names': 'Mr. Mukesh Patel and Mrs. Divya Patel',
            'aadhaar_number': '567890123456',
            'gender': 'Male',
            'registration_date': '2023-09-01',
            'session_expiration_date': '2024-06-30',
            'full_address': '654, East Delhi, New Delhi, Delhi - 110013',
            'email': 'ravi.patel@college.com',
            'emergency_contact': 'Mr. Mukesh Patel - 5432109876',
            'total_fee': 50000,
            'installment_count': 2
        }
    ]
    
    print("\n📝 Adding sample students...")
    for i, student in enumerate(sample_students, 1):
        success, message = Student.add_student(student)
        if success:
            # Create installments for the student
            aadhaar = student['aadhaar_number']
            create_installments(
                aadhaar,
                student['total_fee'],
                student['installment_count'],
                student['registration_date']
            )
            print(f"   ✓ Student {i}: {student['full_name']} added successfully")
        else:
            print(f"   ✗ Student {i}: {message}")

def main():
    """Main function"""
    print("=" * 60)
    print("🏨 Hostel Manager - Sample Data Initialization")
    print("=" * 60)
    
    # Initialize database
    print("\n✓ Initializing database...")
    init_db()
    
    # Check if rooms exist
    rooms = get_all_rooms()
    if not rooms:
        print("✓ Creating sample rooms...")
        for i in range(1, 6):
            create_room(f"Room-{i}")
    
    # Add sample students
    create_sample_students()
    
    print("\n" + "=" * 60)
    print("✅ Sample data initialization complete!")
    print("=" * 60)
    print("\nYou can now:")
    print("  1. Login to the application")
    print("  2. View students in the Students section")
    print("  3. Check room allocations")
    print("  4. View installment details")
    print("\n")

if __name__ == '__main__':
    main()
