from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from datetime import datetime
import uuid
from api.models import TaskCreate, TaskUpdate, TaskResponse

app = FastAPI(
    title="Task Management API",
    version="1.0.0"
)

# Add "Flask-like" config
class FlaskConfig:
    def __init__(self):
        self._config = {'TESTING': False}
    
    def __getitem__(self, key):
        return self._config[key]
    
    def __setitem__(self, key, value):
        self._config[key] = value

app.config = FlaskConfig()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"error": "Invalid request data"}
    )

# Add test_client method for testing
class FlaskCompatibleResponse:
    def __init__(self, response):
        self.response = response
        self.status_code = response.status_code
        self.data = response.content
    
    def get_json(self):
        return self.response.json()
    
    def __iter__(self):
        return iter([self.data])

class FlaskCompatibleClient:
    def __init__(self, client):
        self.client = client
        self.config = {"TESTING": True}
    
    def get(self, url, **kwargs):
        resp = self.client.get(url, **kwargs)
        return FlaskCompatibleResponse(resp)
    
    def post(self, url, json=None, content_type=None, **kwargs):
        headers = kwargs.pop('headers', {})
        if content_type:
            headers['Content-Type'] = content_type
        resp = self.client.post(url, json=json, headers=headers, **kwargs)
        return FlaskCompatibleResponse(resp)
    
    def put(self, url, json=None, content_type=None, **kwargs):
        headers = kwargs.pop('headers', {})
        if content_type:
            headers['Content-Type'] = content_type
        resp = self.client.put(url, json=json, headers=headers, **kwargs)
        return FlaskCompatibleResponse(resp)
    
    def delete(self, url, **kwargs):
        resp = self.client.delete(url, **kwargs)
        return FlaskCompatibleResponse(resp)
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        pass

def get_test_client():
    from fastapi.testclient import TestClient
    return FlaskCompatibleClient(TestClient(app))

app.test_client = get_test_client

tasks = {}

# Helper
def create_response(data, status_code=200):
    return JSONResponse(content=data, status_code=status_code)

# Routes

@app.get("/tasks", response_model=list[TaskResponse], status_code=status.HTTP_200_OK)
async def get_tasks():
    """Get all tasks"""
    return create_response(list(tasks.values()))

@app.get("/tasks/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def get_task(task_id: str):
    """Get a specific task by ID"""
    task = tasks.get(task_id)
    if not task:
        return create_response({"error": "Task not found"}, status.HTTP_404_NOT_FOUND)
    return create_response(task)

@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task_data: TaskCreate):
    """Create a new task"""
    task_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    
    task = {
        "id": task_id,
        "title": task_data.title,
        "description": task_data.description or "",
        "completed": False,
        "created_at": now,
        "updated_at": None
    }
    
    tasks[task_id] = task
    return create_response(task, status.HTTP_201_CREATED)

@app.put("/tasks/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def update_task(task_id: str, task_data: TaskUpdate):
    """Update an existing task"""
    task = tasks.get(task_id)
    if not task:
        return create_response({"error": "Task not found"}, status.HTTP_404_NOT_FOUND)
    
    update_data = task_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None:
            task[key] = value
    
    task["updated_at"] = datetime.utcnow().isoformat()
    tasks[task_id] = task
    
    return create_response(task)

@app.delete("/tasks/{task_id}", status_code=status.HTTP_200_OK)
async def delete_task(task_id: str):
    """Delete a task"""
    if task_id not in tasks:
        return create_response({"error": "Task not found"}, status.HTTP_404_NOT_FOUND)
    
    del tasks[task_id]
    return create_response({"message": "Task deleted successfully"})

@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    """Health check endpoint"""
    return create_response({"status": "healthy"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)