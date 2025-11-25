import os
import logging
from flask import Flask, render_template, request, jsonify, redirect, url_for
from models import db, Student, Room, Allocation, Payment, Complaint, User
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
# removed unused check_password_hash import; password checking is handled on User model
import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime
from sqlalchemy import or_


def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    # configure basic logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
    app.logger = logging.getLogger('managmentsystem')
    # ensure instance folder exists and prefer instance DB to avoid duplicate files
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except Exception:
        # if instance_path creation fails, continue; SQLAlchemy will still attempt to create DB
        pass

    instance_db = os.path.join(app.instance_path, 'hostel.db')
    # normalize path for sqlite URL (use forward slashes)
    instance_db_url = f"sqlite:///{instance_db.replace('\\', '/') }"
    database_url = os.environ.get('DATABASE_URL') or instance_db_url
    # if no explicit DATABASE_URL provided and a root `hostel.db` exists, remove it to avoid duplicates
    try:
        if not os.environ.get('DATABASE_URL'):
            root_db = os.path.join(os.getcwd(), 'hostel.db')
            if os.path.exists(root_db) and os.path.abspath(root_db) != os.path.abspath(instance_db):
                try:
                    os.remove(root_db)
                except Exception:
                    # non-fatal: ignore if cannot remove
                    pass
    except Exception:
        pass
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    # allow toggling SQL echo for debugging via env var
    app.config['SQLALCHEMY_ECHO'] = bool(os.environ.get('SQLALCHEMY_ECHO', ''))
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Run a lightweight on-start migration to add `email` column to users if missing
    with app.app_context():
        try:
            # check if 'email' column exists
            res = db.session.execute("PRAGMA table_info('users')").fetchall()
            cols = [r[1] for r in res]
            if 'email' not in cols:
                # Attempt to migrate users table to include `email` column while preserving data.
                try:
                    db.session.execute("BEGIN TRANSACTION;")
                    db.session.execute(
                        "CREATE TABLE users_new (id INTEGER PRIMARY KEY, username TEXT, email TEXT UNIQUE, password_hash TEXT, role TEXT);"
                    )
                    db.session.execute(
                        "INSERT INTO users_new (id, username, email, password_hash, role) SELECT id, username, (username || '@culturehostel.local'), password_hash, role FROM users;"
                    )
                    db.session.execute("DROP TABLE users;")
                    db.session.execute("ALTER TABLE users_new RENAME TO users;")
                    db.session.execute("COMMIT;")
                    db.session.commit()
                except Exception:
                    db.session.rollback()
                    # Fallback: try simple add column without unique constraint
                    try:
                        db.session.execute("ALTER TABLE users ADD COLUMN email VARCHAR(120);")
                        db.session.commit()
                    except Exception:
                        db.session.rollback()
                # populate email from username where possible
                users = db.session.execute("SELECT id, username FROM users").fetchall()
                for uid, uname in users:
                    if uname:
                        email = f"{uname}@culturehostel.local"
                        try:
                            db.session.execute("UPDATE users SET email = :email WHERE id = :id", {'email': email, 'id': uid})
                        except Exception:
                            pass
                db.session.commit()
        except Exception:
            db.session.rollback()

        # Ensure Student table has new columns for registration fields
        try:
            from sqlalchemy import text
            res = db.session.execute(text("PRAGMA table_info('students')")).fetchall()
            cols = [r[1] for r in res]
            add_cols = []
            if 'aadhar_number' not in cols:
                add_cols.append("ALTER TABLE students ADD COLUMN aadhar_number VARCHAR(50);")
            if 'college_admission_number' not in cols:
                add_cols.append("ALTER TABLE students ADD COLUMN college_admission_number VARCHAR(80);")
            if 'college_name' not in cols:
                add_cols.append("ALTER TABLE students ADD COLUMN college_name VARCHAR(180);")
            for sql in add_cols:
                try:
                    db.session.execute(text(sql))
                    db.session.commit()
                except Exception:
                    db.session.rollback()
        except Exception:
            db.session.rollback()

        # Recompute room occupancy from allocations to correct any drift
        try:
            rooms = Room.query.all()
            for r in rooms:
                try:
                    actual = Allocation.query.filter_by(room_id=r.id).count()
                    if (r.occupancy or 0) != actual:
                        r.occupancy = actual
                except Exception:
                    pass
            db.session.commit()
        except Exception:
            db.session.rollback()

    # login manager
    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Require login for all routes except allowed ones
    @app.before_request
    def require_login():
        # allow static files and a set of public endpoints (login/register/index and public APIs)
        allowed = (
            'login', 'static', 'favicon', 'index', 'register_student',
            'students_page', 'student_detail_page', 'api_students', 'api_student_detail', 'api_create_student'
        )
        endpoint = request.endpoint or ''
        if endpoint.startswith('static'):
            return None
        if endpoint in allowed:
            return None
        # If user is not authenticated, redirect to login
        if not current_user.is_authenticated:
            return redirect(url_for('login', next=request.path))

    @app.route('/')
    def index():
        students_count = Student.query.count()
        rooms_count = Room.query.count()
        allocations_count = Allocation.query.count()
        unpaid = Payment.query.filter(Payment.status != 'paid').count()
        # provide recent students list for templates that expect it
        recent_students = Student.query.order_by(Student.id.desc()).limit(6).all()
        return render_template('index.html', students_count=students_count, rooms_count=rooms_count, allocations_count=allocations_count, unpaid=unpaid, recent_students=recent_students)

    @app.route('/dashboard')
    def dashboard():
        # pragmatic alias for index as the authenticated dashboard
        return redirect(url_for('index'))

    @app.route('/students')
    def students_page():
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        # support filters: ?filter=pending to show students with unpaid payments
        flt = request.args.get('filter')
        q = request.args.get('q', '').strip()
        base = Student.query
        if flt == 'pending':
            base = base.join(Payment).filter(Payment.status != 'paid')
        if q:
            # simple search on name, email, phone or roll_no
            qlike = f"%{q}%"
            base = base.filter(or_(Student.name.ilike(qlike), Student.email.ilike(qlike), Student.phone.ilike(qlike), Student.roll_no.ilike(qlike)))
        pagination = base.order_by(Student.id).distinct().paginate(page=page, per_page=per_page)
        # also provide counts for the header/hero
        students_count = Student.query.count()
        rooms_count = Room.query.count()
        allocations_count = Allocation.query.count()
        unpaid = Payment.query.filter(Payment.status != 'paid').count()
        # compute unpaid counts per student for display (small N, acceptable for now)
        unpaid_map = {}
        for s in pagination.items:
            cnt = sum(1 for p in getattr(s, 'payments', []) if getattr(p, 'status', '') != 'paid')
            unpaid_map[s.id] = cnt
        return render_template('students.html', pagination=pagination, students_count=students_count, rooms_count=rooms_count, allocations_count=allocations_count, unpaid=unpaid, unpaid_map=unpaid_map)

    # API: list students (JSON)
    @app.route('/api/students')
    def api_students():
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        pagination = Student.query.order_by(Student.id).paginate(page=page, per_page=per_page)
        data = [s.to_dict() for s in pagination.items]
        return jsonify({
            'items': data,
            'page': pagination.page,
            'pages': pagination.pages,
            'total': pagination.total,
        })

    @app.route('/api/students', methods=['POST'])
    def api_create_student():
        if request.is_json:
            data = request.get_json() or {}
        else:
            data = request.form.to_dict() if request.form else {}
        required = ('name', 'email', 'roll_no')
        for k in required:
            if k not in data:
                return jsonify({'error': f'missing {k}'}), 400

        # create student and accept optional total_fee
        try:
            total_fee = float(data.get('total_fee')) if data.get('total_fee') not in (None, '') else 0.0
        except Exception:
            return jsonify({'error': 'invalid total_fee value'}), 400

        student = Student(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone'),
            roll_no=data['roll_no'],
            gender=data.get('gender'),
            year=data.get('year'),
            total_fee=total_fee,
        )
        db.session.add(student)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'unable to create student', 'detail': str(e)}), 400
        return jsonify(student.to_dict()), 201

    # Public registration endpoint (form or JSON)
    @app.route('/register', methods=['GET', 'POST'])
    def register_student():
        # GET: render registration page for logged-in users
        if request.method == 'GET':
            return render_template('register.html')
        if request.is_json:
            data = request.get_json() or {}
        else:
            data = request.form.to_dict() if request.form else {}

        # validate required fields
        required = ('name', 'email', 'roll_no')
        for k in required:
            if not data.get(k):
                # render the form again with error for HTML form submissions
                if request.method == 'POST' and not request.is_json:
                    return render_template('register.html', error=f'missing {k}'), 400
                return jsonify({'error': f'missing {k}'}), 400

        # parse optional numeric fields safely
        try:
            total_fee = float(data.get('total_fee')) if data.get('total_fee') not in (None, '') else 0.0
        except Exception:
            total_fee = 0.0

        student = Student(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            roll_no=data.get('roll_no'),
            gender=data.get('gender'),
            year=data.get('year'),
            parent_name=data.get('parent_name'),
            parent_phone=data.get('parent_phone'),
            aadhar_number=data.get('aadhar_number'),
            college_admission_number=data.get('college_admission_number'),
            college_name=data.get('college_name'),
            address=data.get('address'),
            total_fee=total_fee,
        )
        db.session.add(student)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            # for form POSTs, re-render with error
            if request.method == 'POST' and not request.is_json:
                return render_template('register.html', error='Unable to register student: ' + str(e)), 400
            return jsonify({'error': 'unable to create student', 'detail': str(e)}), 400

        # on successful HTML form POST, redirect to students list
        if not request.is_json:
            return redirect(url_for('students_page'))
        return jsonify(student.to_dict()), 201

    # Delete a student (admin only)
    @app.route('/students/<int:student_id>/delete', methods=['POST'])
    @login_required
    def delete_student(student_id):
        if getattr(current_user, 'role', '') != 'admin':
            return jsonify({'error':'forbidden'}), 403
        s = Student.query.get_or_404(student_id)
        # delete related records safely and adjust room occupancy
        from models import Allocation, Payment, Complaint, Installment, StudentBadge

        try:
            app.logger.info('Deleting student id=%s requested by user=%s', student_id, getattr(current_user, 'id', None))
            # handle allocations: decrement room occupancy for any active allocation
            allocs = Allocation.query.filter_by(student_id=s.id).all()
            for a in allocs:
                try:
                    if a.room and (a.room.occupancy or 0) > 0:
                        a.room.occupancy = max(0, (a.room.occupancy or 0) - 1)
                except Exception:
                    app.logger.exception('Error adjusting room occupancy for allocation %s', getattr(a, 'id', None))
                db.session.delete(a)

            # remove other dependent rows (use bulk delete for speed)
            Payment.query.filter_by(student_id=s.id).delete(synchronize_session=False)
            Complaint.query.filter_by(student_id=s.id).delete(synchronize_session=False)
            Installment.query.filter_by(student_id=s.id).delete(synchronize_session=False)
            StudentBadge.query.filter_by(student_id=s.id).delete(synchronize_session=False)

            # finally delete the student record
            db.session.delete(s)
            db.session.commit()
            return jsonify({'success': True}), 200
        except Exception as exc:
            app.logger.exception('Failed to delete student id=%s: %s', student_id, exc)
            db.session.rollback()
            return jsonify({'success': False, 'error': 'unable to delete'}), 500

    @app.route('/api/allocate', methods=['POST'])
    def api_allocate():
        data = request.get_json() or {}
        student_id = data.get('student_id')
        room_id = data.get('room_id')
        if not student_id or not room_id:
            return jsonify({'error': 'student_id and room_id required'}), 400

        student = Student.query.get(student_id)
        room = Room.query.get(room_id)
        if not student or not room:
            return jsonify({'error': 'invalid student or room'}), 404

        if room.occupancy >= room.capacity:
            return jsonify({'error': 'room full'}), 400

        # remove previous allocation (and decrement occupancy)
        if student.allocation:
            old = student.allocation
            try:
                old_room = old.room
                if old_room and old_room.occupancy > 0:
                    old_room.occupancy = max(0, old_room.occupancy - 1)
            except Exception:
                pass
            db.session.delete(old)

        alloc = Allocation(student=student, room=room)
        room.occupancy = (room.occupancy or 0) + 1
        db.session.add(alloc)
        db.session.commit()
        return jsonify({'message': 'allocated', 'student': student.to_dict(), 'room': room.to_dict()})

    # Simple API to view a student's detail
    @app.route('/api/students/<int:student_id>')
    def api_student_detail(student_id):
        s = Student.query.get_or_404(student_id)
        d = s.to_dict()
        if s.allocation:
            d['room'] = s.allocation.room.to_dict()
        d['payments'] = [{'amount': p.amount, 'date': p.date.isoformat(), 'status': p.status} for p in s.payments]
        d['complaints'] = [{'text': c.text, 'status': c.status, 'created_at': c.created_at.isoformat()} for c in s.complaints]
        # include installments if present
        try:
            d['installments'] = [
                {
                    'id': ins.id,
                    'amount': ins.amount,
                    'due_date': ins.due_date.isoformat() if ins.due_date else None,
                    'paid_date': ins.paid_date.isoformat() if ins.paid_date else None,
                    'status': ins.status,
                }
                for ins in getattr(s, 'installments', [])
            ]
        except Exception:
            d['installments'] = []

        # include computed fee summaries
        try:
            d['total_paid'] = float(s.total_paid or 0.0)
        except Exception:
            d['total_paid'] = 0.0
        try:
            d['remaining_fee'] = float(s.remaining_fee or 0.0)
        except Exception:
            d['remaining_fee'] = float((s.total_fee or 0.0) - (d.get('total_paid', 0.0)))

        return jsonify(d)

    # protect updates: require login
    @app.route('/api/students/<int:student_id>', methods=['PUT'])
    @login_required
    def api_update_student(student_id):
        s = Student.query.get_or_404(student_id)
        data = request.get_json() or {}
        # allowed fields
        fields = ['name', 'email', 'phone', 'roll_no', 'gender', 'year', 'parent_name', 'parent_phone', 'address']
        for k in fields:
            if k in data:
                setattr(s, k, data[k])
        # allow updating total_fee only by admin users and ensure numeric
        if 'total_fee' in data:
            try:
                if getattr(current_user, 'role', '') != 'admin':
                    return jsonify({'error': 'forbidden'}), 403
                s.total_fee = float(data.get('total_fee') or 0.0)
            except Exception:
                return jsonify({'error': 'invalid total_fee value'}), 400
        db.session.commit()
        return jsonify({'message': 'updated', 'student': s.to_dict()})

    

    # Installment management
    @app.route('/api/students/<int:student_id>/installments', methods=['POST'])
    @login_required
    def api_create_installment(student_id):
        s = Student.query.get_or_404(student_id)
        data = request.get_json() or {}
        amount = data.get('amount')
        if amount is None:
            return jsonify({'error': 'amount required'}), 400
        # parse optional due_date (accepts ISO date or datetime)
        from datetime import datetime, date
        due_date = None
        if data.get('due_date'):
            ds = data.get('due_date')
            try:
                # try full datetime
                due_date = datetime.fromisoformat(ds)
            except Exception:
                try:
                    # try date only
                    d = date.fromisoformat(ds)
                    due_date = datetime(d.year, d.month, d.day)
                except Exception:
                    due_date = None

        from models import Installment
        ins = Installment(student_id=s.id, amount=float(amount), due_date=due_date, status=data.get('status','due'))
        db.session.add(ins)
        db.session.commit()
        return jsonify({'message': 'installment created', 'installment': {'id': ins.id, 'amount': ins.amount, 'status': ins.status}}), 201

    @app.route('/api/installments/<int:ins_id>', methods=['PUT'])
    @login_required
    def api_update_installment(ins_id):
        from models import Installment
        ins = Installment.query.get_or_404(ins_id)
        data = request.get_json() or {}
        if 'amount' in data:
            ins.amount = data['amount']
        if 'status' in data:
            ins.status = data['status']
            if data['status'] == 'paid':
                from datetime import datetime
                ins.paid_date = datetime.utcnow()
        db.session.commit()
        return jsonify({'message': 'updated', 'installment': {'id': ins.id, 'amount': ins.amount, 'status': ins.status}})

    @app.route('/api/installments/<int:ins_id>', methods=['DELETE'])
    @login_required
    def api_delete_installment(ins_id):
        from models import Installment
        ins = Installment.query.get_or_404(ins_id)
        # only admin can delete
        if getattr(current_user, 'role', '') != 'admin':
            return jsonify({'error': 'forbidden'}), 403
        db.session.delete(ins)
        db.session.commit()
        return jsonify({'message': 'deleted'})

    # Student detail page (interactive editor)
    @app.route('/students/<int:student_id>')
    def student_detail_page(student_id):
        s = Student.query.get_or_404(student_id)
        # provide header counts so layout doesn't receive missing vars
        students_count = Student.query.count()
        rooms_count = Room.query.count()
        allocations_count = Allocation.query.count()
        unpaid = Payment.query.filter(Payment.status != 'paid').count()
        return render_template('student_detail.html', student=s, students_count=students_count, rooms_count=rooms_count, allocations_count=allocations_count, unpaid=unpaid)

    # Gamification: award points API
    @app.route('/api/students/<int:student_id>/points', methods=['POST'])
    @login_required
    def api_award_points(student_id):
        # anyone logged-in can award in this demo; in production restrict
        s = Student.query.get_or_404(student_id)
        data = request.get_json() or {}
        try:
            delta = int(data.get('points', 0))
        except Exception:
            return jsonify({'error':'invalid points value'}), 400
        s.points = (s.points or 0) + delta
        db.session.commit()
        return jsonify({'message':'points awarded','points':s.points})

    # Gamification features removed: badge award API, leaderboard and badges pages

    # Admin: show empty rooms
    @app.route('/admin/empty_rooms')
    @login_required
    def admin_empty_rooms():
        if getattr(current_user, 'role', '') != 'admin':
            return redirect(url_for('index'))
        rooms = Room.query.order_by(Room.number).all()
        empty = [r for r in rooms if r.occupancy < r.capacity]
        return render_template('admin_empty_rooms.html', rooms=empty)

    @app.route('/admin/rooms')
    @login_required
    def admin_rooms():
        if getattr(current_user, 'role', '') != 'admin':
            return redirect(url_for('index'))
        rooms = Room.query.order_by(Room.number).all()
        return render_template('admin_rooms.html', rooms=rooms)

    @app.route('/api/rooms/<int:room_id>/students')
    @login_required
    def api_room_students(room_id):
        allocs = Allocation.query.filter_by(room_id=room_id).all()
        items = [a.student.to_dict() for a in allocs]
        return jsonify({'items': items})

    # Email helper
    def send_email(to_email, subject, body):
        smtp_server = os.environ.get('SMTP_SERVER')
        smtp_port = int(os.environ.get('SMTP_PORT', '0') or 0)
        smtp_user = os.environ.get('SMTP_USER')
        smtp_pass = os.environ.get('SMTP_PASSWORD')
        from_email = os.environ.get('FROM_EMAIL') or smtp_user
        if not smtp_server or not smtp_port or not smtp_user or not smtp_pass:
            # SMTP not configured; for safety return False
            return False, 'SMTP not configured'
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email
        msg.set_content(body)
        try:
            # try SSL (465) first
            if smtp_port == 465:
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
                    server.login(smtp_user, smtp_pass)
                    server.send_message(msg)
            else:
                server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
                server.quit()
            return True, 'sent'
        except Exception as e:
            return False, str(e)

    # Admin: send reminders for overdue installments
    @app.route('/admin/send_reminders', methods=['GET','POST'])
    @login_required
    def admin_send_reminders():
        if getattr(current_user, 'role', '') != 'admin':
            return redirect(url_for('index'))
        from models import Installment
        now = datetime.utcnow()
        overdue = Installment.query.filter(Installment.due_date != None, Installment.due_date < now, Installment.status != 'paid').all()
        results = []
        for ins in overdue:
            student = ins.student
            if not student or not student.email:
                results.append((ins.id, 'no email'))
                continue
            subj = f'Reminder: installment due for {student.name}'
            body = f'Dear {student.name},\n\nYour installment of amount {ins.amount} was due on {ins.due_date.date() if ins.due_date else "N/A"}. Please pay as soon as possible.\n\nRegards, Hostel Admin'
            sent, info = send_email(student.email, subj, body)
            results.append((ins.id, sent, info))
        return render_template('admin_send_reminders.html', results=results, count=len(results))

    # Admin: allocated rooms report
    @app.route('/admin/allocated_rooms')
    @login_required
    def admin_allocated_rooms():
        if getattr(current_user, 'role', '') != 'admin':
            return redirect(url_for('index'))
        allocations = Allocation.query.order_by(Allocation.id).all()
        return render_template('admin_allocated_rooms.html', allocations=allocations)

    # Admin: allocate via web form
    @app.route('/admin/allocate_room', methods=['GET', 'POST'])
    @login_required
    def admin_allocate_room():
        if getattr(current_user, 'role', '') != 'admin':
            return redirect(url_for('index'))
        if request.method == 'POST':
            student_id = int(request.form.get('student_id'))
            room_id = int(request.form.get('room_id'))
            # reuse allocation logic
            student = Student.query.get(student_id)
            room = Room.query.get(room_id)
            if not student or not room:
                return render_template('admin_allocate_room.html', error='Invalid student or room', students=Student.query.all(), rooms=Room.query.all())
            if room.occupancy >= room.capacity:
                return render_template('admin_allocate_room.html', error='Room full', students=Student.query.all(), rooms=Room.query.all())
            # remove previous allocation if any and adjust occupancy
            if student.allocation:
                old = student.allocation
                try:
                    old_room = old.room
                    if old_room and old_room.occupancy > 0:
                        old_room.occupancy = max(0, old_room.occupancy - 1)
                except Exception:
                    pass
                db.session.delete(old)

            alloc = Allocation(student=student, room=room)
            room.occupancy = (room.occupancy or 0) + 1
            db.session.add(alloc)
            db.session.commit()
            return redirect(url_for('admin_allocated_rooms'))
        students = Student.query.order_by(Student.id).all()
        rooms = Room.query.order_by(Room.number).all()
        return render_template('admin_allocate_room.html', students=students, rooms=rooms)

    # Admin: vacate student from room
    @app.route('/admin/vacate_room', methods=['POST'])
    @login_required
    def admin_vacate_room():
        if getattr(current_user, 'role', '') != 'admin':
            return jsonify({'error':'forbidden'}), 403
        student_id = int(request.form.get('student_id'))
        student = Student.query.get_or_404(student_id)
        if not student.allocation:
            return jsonify({'error':'no allocation found'}), 400
        alloc = student.allocation
        room = alloc.room
        db.session.delete(alloc)
        room.occupancy = max(0, room.occupancy - 1)
        db.session.commit()
        return redirect(url_for('admin_allocated_rooms'))

    # Admin: messages and contacts
    @app.route('/admin/messages')
    @login_required
    def admin_messages():
        if getattr(current_user, 'role', '') != 'admin':
            return redirect(url_for('index'))
        from models import Message
        msgs = Message.query.order_by(Message.created_at.desc()).all()
        return render_template('admin_messages.html', messages=msgs)

    @app.route('/admin/contacts')
    @login_required
    def admin_contacts():
        if getattr(current_user, 'role', '') != 'admin':
            return redirect(url_for('index'))
        from models import Contact
        contacts = Contact.query.order_by(Contact.created_at.desc()).all()
        return render_template('admin_contacts.html', contacts=contacts)

    @app.route('/admin/profile')
    @login_required
    def admin_profile():
        if getattr(current_user, 'role', '') != 'admin':
            return redirect(url_for('index'))
        return render_template('admin_profile.html', user=current_user)

    # auth routes
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        # if already logged in, go to dashboard
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        error = None
        if request.method == 'POST':
            data = request.form
            email = data.get('email')
            password = data.get('password')
            user = None
            if email:
                try:
                    user = User.query.filter_by(email=email).first()
                except Exception:
                    # column may not exist yet in older DBs; fallback to username lookup
                    user = None
            # fallback to username lookup for backward compatibility
            if not user and data.get('username'):
                user = User.query.filter_by(username=data.get('username')).first()
            if not user and email:
                # also try username == email local-part
                uname = email.split('@')[0]
                user = User.query.filter_by(username=uname).first()

            if user and user.check_password(password):
                login_user(user)
                next_page = request.args.get('next') or url_for('dashboard')
                return redirect(next_page)
            error = 'Invalid email or password'

        return render_template('login.html', error=error)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
