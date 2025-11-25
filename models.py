from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(30))
    roll_no = db.Column(db.String(50), unique=True, nullable=False)
    total_fee = db.Column(db.Float, default=0.0)
    gender = db.Column(db.String(10))
    year = db.Column(db.String(20))
    parent_name = db.Column(db.String(120))
    parent_phone = db.Column(db.String(30))
    aadhar_number = db.Column(db.String(50))
    college_admission_number = db.Column(db.String(80))
    college_name = db.Column(db.String(180))
    address = db.Column(db.String(255))
    points = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    allocation = db.relationship('Allocation', back_populates='student', uselist=False)
    allocation = db.relationship('Allocation', back_populates='student', uselist=False, cascade='all, delete-orphan')
    payments = db.relationship('Payment', back_populates='student', cascade='all, delete-orphan')
    complaints = db.relationship('Complaint', back_populates='student', cascade='all, delete-orphan')

    # student_badges and installments are defined via backrefs on their models with cascading

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'roll_no': self.roll_no,
            'total_fee': float(self.total_fee or 0.0),
            'gender': self.gender,
            'year': self.year,
            'parent_name': self.parent_name,
            'parent_phone': self.parent_phone,
            'aadhar_number': self.aadhar_number,
            'college_admission_number': self.college_admission_number,
            'college_name': self.college_name,
            'address': self.address,
            'created_at': self.created_at.isoformat(),
            'total_paid': float(self.total_paid or 0.0),
            'remaining_fee': float(self.remaining_fee or 0.0),
        }

    @property
    def total_paid(self):
        # sum of Payment.amount where status == 'paid' plus paid installments
        paid = 0.0
        try:
            for p in getattr(self, 'payments', []) or []:
                if getattr(p, 'status', '') == 'paid' and p.amount:
                    paid += float(p.amount)
        except Exception:
            pass
        try:
            for ins in getattr(self, 'installments', []) or []:
                if getattr(ins, 'status', '') == 'paid' and ins.amount:
                    paid += float(ins.amount)
        except Exception:
            pass
        return float(paid)

    @property
    def remaining_fee(self):
        return float((self.total_fee or 0.0) - (self.total_paid or 0.0))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(30), default='admin')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20), unique=True, nullable=False)
    capacity = db.Column(db.Integer, default=4)
    occupancy = db.Column(db.Integer, default=0)

    allocations = db.relationship('Allocation', back_populates='room')

    def to_dict(self):
        return {
            'id': self.id,
            'number': self.number,
            'capacity': self.capacity,
            'occupancy': self.occupancy,
        }


class Allocation(db.Model):
    __tablename__ = 'allocations'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True)

    student = db.relationship('Student', back_populates='allocation')
    room = db.relationship('Room', back_populates='allocations')


class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(30), default='paid')

    student = db.relationship('Student', back_populates='payments')


class Installment(db.Model):
    __tablename__ = 'installments'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.DateTime, nullable=True)
    paid_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(30), default='due')

    # define backref with cascade so that deleting a Student cleans up installments
    student = db.relationship('Student', backref=db.backref('installments', cascade='all, delete-orphan'))


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_name = db.Column(db.String(120))
    sender_email = db.Column(db.String(120))
    subject = db.Column(db.String(255))
    body = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(40))
    note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Badge(db.Model):
    __tablename__ = 'badges'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255))
    icon = db.Column(db.String(255))


class StudentBadge(db.Model):
    __tablename__ = 'student_badges'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    badge_id = db.Column(db.Integer, db.ForeignKey('badges.id'), nullable=False)
    awarded_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship('Student', backref=db.backref('student_badges', cascade='all, delete-orphan'))
    badge = db.relationship('Badge')


class Complaint(db.Model):
    __tablename__ = 'complaints'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(30), default='open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship('Student', back_populates='complaints')
