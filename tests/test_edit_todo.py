import pytest
from app import app, db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_edit_todo_valid(client):
    todo_data = {
        "title": "Apply to SLB",
        "description": "Write technique1 and technique 2",
        "status": "Done",
        "due_date": "2024-03-30"
    }
    json_response = client.post('/add_todo', json=todo_data)

    todo_data = {
        "id": '1',
        "title": "Apply to SLB",
        "description": "Write technique1 and technique 2",
        "status": "Done",
        "due_date": "2024-03-30"
    }
    json_response = client.put('/edit_todo', json=todo_data)
    assert json_response.status_code == 200
    assert json_response.json == {'message': 'Todo updated!'}
def test_edit_todo_empty_description_valid(client):
    todo_data = {
        "title": "Apply to SLB",
        "description": "Write technique1 and technique 2",
        "status": "Done",
        "due_date": "2024-03-30"
    }
    json_response = client.post('/add_todo', json=todo_data)
    todo_data = {
        "id": '1',
        "title": "Apply to SLB",
        "description": "",
        "status": "Done",
        "due_date": "2024-03-30"
    }
    json_response = client.put('/edit_todo', json=todo_data)
    assert json_response.status_code == 200
    assert json_response.json == {'message': 'Todo updated!'}


def test_edit_todo_missing_title_invalid(client):
    todo_data = {
        "title": "Apply to SLB",
        "description": "Write technique1 and technique 2",
        "status": "Done",
        "due_date": "2024-03-30"
    }
    json_response = client.post('/add_todo', json=todo_data)
    todo_data = {
        "id": '1',
        "description": "Write technique1 and technique 2",
        "status": "Done",
        "due_date": "2024-03-30"
    }
    json_response = client.put('/edit_todo', json=todo_data)
    assert json_response.status_code == 400
    assert json_response.json == {
        'Invalid JSON Key': "Ensure the following keys exist 'id','title','status','due_date','description'"}


def test_edit_todo_empty_title_invalid(client):
    todo_data = {
        "title": "Apply to SLB",
        "description": "Write technique1 and technique 2",
        "status": "Done",
        "due_date": "2024-03-30"
    }
    json_response = client.post('/add_todo', json=todo_data)
    todo_data = {
        "id": '1',
        "title": "",
        "description": "Write technique1 and technique 2",
        "status": "Done",
        "due_date": "2024-03-30"
    }
    json_response = client.put('/edit_todo', json=todo_data)
    assert json_response.status_code == 400
    assert json_response.json == {'error': 'Title cannot be empty'}


def test_edit_todo_missing_description_invalid(client):
    todo_data = {
        "title": "Apply to SLB",
        "description": "Write technique1 and technique 2",
        "status": "Done",
        "due_date": "2024-03-30"
    }
    json_response = client.post('/add_todo', json=todo_data)
    todo_data = {
        "id": '1',
        "title": "Apply to SLB",
        "status": "Done",
        "due_date": "2024-03-30"
    }
    json_response = client.put('/edit_todo', json=todo_data)
    assert json_response.status_code == 400
    assert json_response.json == {
        'Invalid JSON Key': "Ensure the following keys exist 'id','title','status','due_date','description'"}


def test_edit_todo_invalid_status_invalid(client):
    todo_data = {
        "title": "Apply to SLB",
        "description": "Write technique1 and technique 2",
        "status": "Done",
        "due_date": "2024-03-30"
    }
    json_response = client.post('/add_todo', json=todo_data)
    todo_data = {
        "id": '1',
        'title': 'Test Todo',
        'description': 'Test description',
        'status': 'Invalid',
        'due_date': '2024-03-20'
    }
    response = client.put('/edit_todo', json=todo_data)
    assert response.status_code == 400
    assert response.json == {'error': 'Invalid status, Please only put "Pending","Done","Backlog"'}


def test_edit_todo_empty_status_invalid(client):
    todo_data = {
        "title": "Apply to SLB",
        "description": "Write technique1 and technique 2",
        "status": "Done",
        "due_date": "2024-03-30"
    }
    json_response = client.post('/add_todo', json=todo_data)
    todo_data = {
        "id": '1',
        'title': 'Test Todo',
        'description': 'Test description',
        'status': '',
        'due_date': '2024-03-20'
    }
    response = client.put('/edit_todo', json=todo_data)
    assert response.status_code == 400
    assert response.json == {'error': 'Invalid status, Please only put "Pending","Done","Backlog"'}


def test_edit_todo_empty_date_invalid(client):
    todo_data = {
        "title": "Apply to SLB",
        "description": "Write technique1 and technique 2",
        "status": "Done",
        "due_date": "2024-03-30"
    }
    json_response = client.post('/add_todo', json=todo_data)
    todo_data = {
        "id": '1',
        'title': 'Test Todo',
        'description': 'Test description',
        'status': 'Pending',
        'due_date': ''
    }
    response = client.put('/edit_todo', json=todo_data)
    assert response.status_code == 400
    assert response.json == {'error': 'Due date cannot be empty'}


def test_edit_todo_invalid_date_format(client):
    todo_data = {
        "title": "Apply to SLB",
        "description": "Write technique1 and technique 2",
        "status": "Done",
        "due_date": "2024-03-30"
    }
    json_response = client.post('/add_todo', json=todo_data)
    todo_data = {
        "id": '1',
        'title': 'Test Todo',
        'description': 'Test description',
        'status': 'Pending',
        'due_date': '20-03-2024'  # Wrong date format
    }
    response = client.put('/edit_todo', json=todo_data)
    assert response.status_code == 400
    assert response.json == {'error': 'Invalid date format, Please use YYYY-mm-dd'}
