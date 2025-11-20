from app import create_app

app = create_app()
with app.app_context():
    client = app.test_client()
    resp = client.get('/api/students/1')
    print(resp.status_code)
    print(resp.get_data(as_text=True))
