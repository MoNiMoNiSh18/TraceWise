from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to TraceWise API"


def test_health_endpoint():
    response = client.get("/api/v1/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["application"] == "TraceWise"
    assert data["version"] == "0.1.0"


def test_unknown_endpoint():
    response = client.get("/unknown")

    assert response.status_code == 404