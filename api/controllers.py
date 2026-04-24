import uuid
from datetime import datetime
from flask import jsonify

# In-memory storage for tasks
tasks = {}


def get_tasks():
    """Read: Get all tasks"""
    return jsonify(list(tasks.values())), 200


def get_task(task_id):
    """Read: Get a specific task by ID"""
    task = tasks.get(task_id)
    if task:
        return jsonify(task), 200
    return jsonify({"error": "Task not found"}), 404


def create_task(request):
    """Create: Create a new task"""
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
    
    task_id = str(uuid.uuid4())
    task = {
        "id": task_id,
        "title": data['title'],
        "description": data.get('description', ''),
        "completed": False,
        "created_at": datetime.utcnow().isoformat()
    }
    
    tasks[task_id] = task
    return jsonify(task), 201


def update_task(request, task_id):
    """Update: Update an existing task"""
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Update task fields
    if 'title' in data:
        task['title'] = data['title']
    if 'description' in data:
        task['description'] = data['description']
    if 'completed' in data:
        task['completed'] = data['completed']
    
    task['updated_at'] = datetime.utcnow().isoformat()
    tasks[task_id] = task
    
    return jsonify(task), 200


def delete_task(task_id):
    """Delete: Delete a task"""
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    del tasks[task_id]
    return jsonify({"message": "Task deleted successfully"}), 200


def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200
