import sys, os
# ensure repo root is on sys.path so imports work when running this script directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from models import db, Student

app = create_app()

with app.app_context():
    # ensure DB schema present
    db.create_all()

with app.test_client() as c:
    # create a student via API
    payload = {
        'name': 'ci-test-student',
        'email': 'ci-test@example.com',
        'roll_no': 'CI-ROLL-001',
        'phone': '000',
        'total_fee': '1000'
    }
    resp = c.post('/api/students', json=payload)
    assert resp.status_code == 201, f"create failed: {resp.status_code} {resp.get_data(as_text=True)}"
    created = resp.get_json()
    sid = created.get('id')
    print('created', sid)

    # delete student
    # login first as admin
    login = c.post('/login', data={'email': 'admin@culturehostel.local', 'password': 'adminpass'}, follow_redirects=True)
    assert login.status_code in (200, 302), 'login failed'
    delr = c.post(f'/students/{sid}/delete')
    assert delr.status_code == 200, f"delete failed: {delr.status_code} {delr.get_data(as_text=True)}"
    jr = delr.get_json()
    assert jr.get('success') is True, f"delete not successful: {jr}"
    print('deleted ok')

    # confirm deletion
    with app.app_context():
        s = db.session.get(Student, sid)
        assert s is None, 'student still exists after delete'
    print('confirmed deleted')
