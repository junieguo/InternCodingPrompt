from flask import Blueprint
from api.controllers import get_tasks, get_task, create_task, update_task, delete_task, health

# Create a blueprint for task routes
tasks_bp = Blueprint('tasks', __name__)

# Define routes
tasks_bp.add_url_rule('/tasks', view_func=get_tasks, methods=['GET'])
tasks_bp.add_url_rule('/tasks/<task_id>', view_func=get_task, methods=['GET'])
tasks_bp.add_url_rule('/tasks', view_func=create_task, methods=['POST'])
tasks_bp.add_url_rule('/tasks/<task_id>', view_func=update_task, methods=['PUT'])
tasks_bp.add_url_rule('/tasks/<task_id>', view_func=delete_task, methods=['DELETE'])
tasks_bp.add_url_rule('/health', view_func=health, methods=['GET'])
