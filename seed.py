import os
from faker import Faker
from random import choice, randint
from app import create_app
from models import db, Student, Room, Allocation, Payment, Complaint, User, Message, Contact, Badge, StudentBadge


def seed_db(app):
    fake = Faker()
    with app.app_context():
        # reset db
        db.drop_all()
        db.create_all()

        # create rooms: 25 rooms with capacity 4 -> capacity for 100 students
        rooms = []
        for i in range(1, 26):
            r = Room(number=f'R{i:03}', capacity=4)
            db.session.add(r)
            rooms.append(r)
        db.session.commit()

        # create default admin user (email login)
        admin = User(username='admin', email='admin@culturehostel.local')
        admin.set_password('adminpass')
        db.session.add(admin)
        db.session.commit()

        students = []
        for i in range(1, 101):
            s = Student(
                name=fake.name(),
                email=fake.unique.email(),
                phone=fake.phone_number(),
                roll_no=f'ROLL{i:04}',
                total_fee=randint(2000, 8000),
                gender=choice(['Male', 'Female', 'Other']),
                year=choice(['1st', '2nd', '3rd', '4th'])
            )
            db.session.add(s)
            students.append(s)
        db.session.commit()

        # allocate students evenly
        room_index = 0
        for s in students:
            r = rooms[room_index]
            alloc = Allocation(student_id=s.id, room_id=r.id)
            r.occupancy += 1
            db.session.add(alloc)
            room_index = (room_index + 1) % len(rooms)
        db.session.commit()

        # payments and a few complaints
        for s in students:
            p = Payment(student_id=s.id, amount=randint(500, 1500), status=choice(['paid', 'pending']))
            db.session.add(p)
            if randint(1, 20) == 1:
                c = Complaint(student_id=s.id, text=fake.sentence(), status=choice(['open', 'closed']))
                db.session.add(c)
        db.session.commit()

        # sample messages and contacts
        for i in range(3):
            m = Message(sender_name=fake.name(), sender_email=fake.email(), subject=fake.sentence(nb_words=4), body=fake.paragraph())
            db.session.add(m)
        for i in range(3):
            cnt = Contact(name=fake.name(), email=fake.email(), phone=fake.phone_number(), note='Staff contact')
            db.session.add(cnt)
        db.session.commit()

        # seed badges
        badge_data = [
            ('Early Payer', 'Paid fees before due date', '🏆'),
            ('Helper', 'Reported useful complaint/feedback', '🤝'),
            ('Model Student', 'Consistent on-time payments', '🎖️')
        ]
        badges = []
        for name, desc, icon in badge_data:
            b = Badge(name=name, description=desc, icon=icon)
            db.session.add(b)
            badges.append(b)
        db.session.commit()

        # award some random badges and points to students
        from random import sample
        sampled = sample(students, 10)
        for i, s in enumerate(sampled):
            s.points += (10 + i)
            sb = StudentBadge(student_id=s.id, badge_id=badges[i % len(badges)].id)
            db.session.add(sb)
        db.session.commit()

        print('Seeded DB with', len(students), 'students and', len(rooms), 'rooms')


if __name__ == '__main__':
    os.environ.setdefault('DATABASE_URL', 'sqlite:///hostel.db')
    app = create_app()
    seed_db(app)
