from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from datetime import datetime
import uuid
import json

app = FastAPI()

# Add "Flask-like" config
class FlaskConfig:
    def __init__(self):
        self._config = {'TESTING': False}
    
    def __getitem__(self, key):
        return self._config[key]
    
    def __setitem__(self, key, value):
        self._config[key] = value

app.config = FlaskConfig()

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
def response(data, status=200):
    return JSONResponse(
        content=data,
        status_code=status
    )


# Routes

@app.get("/tasks")
async def get_tasks():
    return response(list(tasks.values()))

@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    task = tasks.get(task_id)

    if not task:
        return response({"error": "Task not found"}, 404)

    return response(task)

@app.post("/tasks")
async def create_task(request: Request):
    try:
        data = await request.json()
    except:
        return response({"error": "Invalid JSON"}, 400)

    if not data or "title" not in data:
        return response({"error": "Title is required"}, 400)

    task_id = str(uuid.uuid4())

    task = {
        "id": task_id,
        "title": data["title"],
        "description": data.get("description", ""),
        "completed": False,
        "created_at": datetime.utcnow().isoformat(),
    }

    tasks[task_id] = task

    return response(task, 201)

@app.put("/tasks/{task_id}")
async def update_task(task_id: str, request: Request):
    task = tasks.get(task_id)

    if not task:
        return response({"error": "Task not found"}, 404)

    try:
        data = await request.json()
    except:
        return response({"error": "Invalid JSON"}, 400)

    if data is None:
        return response({"error": "No data provided"}, 400)

    if "title" in data:
        task["title"] = data["title"]

    if "description" in data:
        task["description"] = data["description"]

    if "completed" in data:
        task["completed"] = data["completed"]

    task["updated_at"] = datetime.utcnow().isoformat()

    tasks[task_id] = task

    return response(task)

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    task = tasks.get(task_id)

    if not task:
        return response({"error": "Task not found"}, 404)

    del tasks[task_id]

    return response({"message": "Task deleted successfully"})

@app.get("/health")
async def health():
    return response({"status": "healthy"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)