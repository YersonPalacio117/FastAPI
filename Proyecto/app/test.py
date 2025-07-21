from fastapi.testclient import TestClient
from app.main import app  # ← Ajusta la ruta

def test_client():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200

