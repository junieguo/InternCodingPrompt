import pytest
from fastapi.testclient import TestClient
from app import app

@pytest.fixture(scope="function")
def client():

    with TestClient(app) as test_client:
        # Wrapper for client
        flask_like_client = FlaskLikeClient(test_client)
        yield flask_like_client

class FlaskLikeClient:
    
    def __init__(self, client):
        self.client = client
        self.config = {"TESTING": True}
    
    def get(self, url, **kwargs):
        response = self.client.get(url, **kwargs)
        return FlaskLikeResponse(response)
    
    def post(self, url, json=None, content_type=None, **kwargs):
        headers = kwargs.pop('headers', {})
        if content_type:
            headers['Content-Type'] = content_type
        
        response = self.client.post(url, json=json, headers=headers, **kwargs)
        return FlaskLikeResponse(response)
    
    def put(self, url, json=None, content_type=None, **kwargs):
        headers = kwargs.pop('headers', {})
        if content_type:
            headers['Content-Type'] = content_type
        
        response = self.client.put(url, json=json, headers=headers, **kwargs)
        return FlaskLikeResponse(response)
    
    def delete(self, url, **kwargs):
        response = self.client.delete(url, **kwargs)
        return FlaskLikeResponse(response)

class FlaskLikeResponse:
    
    def __init__(self, response):
        self.response = response
        self.status_code = response.status_code
        self.data = response.content
    
    def get_json(self):
        return self.response.json()
    
    def __iter__(self):
        return iter([self.data])