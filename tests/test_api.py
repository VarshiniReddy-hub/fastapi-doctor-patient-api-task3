from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def get_admin_token():
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "admin",
            "password": "admin123"
        }
    )

    assert response.status_code == 200
    return response.json()["access_token"]


def test_root():
    response = client.get("/")
    assert response.status_code == 200


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


def test_get_doctors():
    token = get_admin_token()

    response = client.get(
        "/api/v1/doctors/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200


def test_get_patients():
    token = get_admin_token()

    response = client.get(
        "/api/v1/patients/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200