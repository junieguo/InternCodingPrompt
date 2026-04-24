import pytest
import json
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_get_tasks_empty(client):
    """Test getting all tasks when there are none."""
    response = client.get('/tasks')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == []


def test_create_task(client):
    """Test creating a new task."""
    response = client.post('/tasks',
                          json={'title': 'Test Task', 'description': 'Test Description'},
                          content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'id' in data
    assert data['title'] == 'Test Task'
    assert data['description'] == 'Test Description'
    assert data['completed'] is False
    assert 'created_at' in data


def test_create_task_missing_title(client):
    """Test creating a task without a title."""
    response = client.post('/tasks',
                          json={'description': 'Test Description'},
                          content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


def test_create_task_no_data(client):
    """Test creating a task with no data."""
    response = client.post('/tasks',
                          content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


def test_get_task(client):
    """Test getting a specific task."""
    # First create a task
    create_response = client.post('/tasks',
                                   json={'title': 'Test Task'},
                                   content_type='application/json')
    task_id = json.loads(create_response.data)['id']
    
    # Then get the task
    response = client.get(f'/tasks/{task_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == task_id
    assert data['title'] == 'Test Task'


def test_get_task_not_found(client):
    """Test getting a task that doesn't exist."""
    response = client.get('/tasks/nonexistent-id')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data


def test_update_task(client):
    """Test updating a task."""
    # First create a task
    create_response = client.post('/tasks',
                                   json={'title': 'Test Task'},
                                   content_type='application/json')
    task_id = json.loads(create_response.data)['id']
    
    # Then update the task
    response = client.put(f'/tasks/{task_id}',
                          json={'title': 'Updated Task', 'completed': True},
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Updated Task'
    assert data['completed'] is True
    assert 'updated_at' in data


def test_update_task_not_found(client):
    """Test updating a task that doesn't exist."""
    response = client.put('/tasks/nonexistent-id',
                          json={'title': 'Updated Task'},
                          content_type='application/json')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data


def test_update_task_no_data(client):
    """Test updating a task with no data."""
    # First create a task
    create_response = client.post('/tasks',
                                   json={'title': 'Test Task'},
                                   content_type='application/json')
    task_id = json.loads(create_response.data)['id']
    
    # Then try to update with no data
    response = client.put(f'/tasks/{task_id}',
                          content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


def test_delete_task(client):
    """Test deleting a task."""
    # First create a task
    create_response = client.post('/tasks',
                                   json={'title': 'Test Task'},
                                   content_type='application/json')
    task_id = json.loads(create_response.data)['id']
    
    # Then delete the task
    response = client.delete(f'/tasks/{task_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    
    # Verify the task is deleted
    get_response = client.get(f'/tasks/{task_id}')
    assert get_response.status_code == 404


def test_delete_task_not_found(client):
    """Test deleting a task that doesn't exist."""
    response = client.delete('/tasks/nonexistent-id')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data


def test_health(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'


def test_get_tasks_with_data(client):
    """Test getting all tasks when there are tasks."""
    # Create multiple tasks
    client.post('/tasks', json={'title': 'Task 1'}, content_type='application/json')
    client.post('/tasks', json={'title': 'Task 2'}, content_type='application/json')
    
    response = client.get('/tasks')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) >= 2
