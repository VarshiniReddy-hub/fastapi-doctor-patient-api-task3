from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Doctor Patient API is running"


def test_login():
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "admin",
            "password": "admin123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_invalid_login():
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "admin",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401


def test_get_doctors():
    response = client.get("/api/v1/doctors/")

    assert response.status_code == 200