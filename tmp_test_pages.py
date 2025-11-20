from app import create_app

app = create_app()
with app.app_context():
    client = app.test_client()
    for path in ['/', '/students', '/students/1', '/login']:
        resp = client.get(path)
        print(path, resp.status_code)
        # print small snippet of content length
        print('len:', len(resp.get_data(as_text=True)))
