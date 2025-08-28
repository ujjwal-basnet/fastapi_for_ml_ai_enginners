from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_main():
    response = client.get("/items?name=iphone")
    assert response.status_code == 200
    assert response.json() == {"name": "iphone", "quantity": 100}
