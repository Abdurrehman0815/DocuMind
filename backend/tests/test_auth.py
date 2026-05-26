import time

from fastapi.testclient import TestClient

from app.main import app


def test_auth_flow_signup_login_me() -> None:
    email = f"user_{int(time.time() * 1000)}@example.com"
    password = "SecurePass123"

    with TestClient(app) as client:
        signup_response = client.post(
            "/api/v1/auth/signup", json={"email": email, "password": password}
        )
        assert signup_response.status_code == 201
        assert signup_response.json()["email"] == email

        login_response = client.post(
            "/api/v1/auth/login", json={"email": email, "password": password}
        )
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        me_response = client.get(
            "/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"}
        )
        assert me_response.status_code == 200
        assert me_response.json()["email"] == email


def test_protected_route_requires_token() -> None:
    with TestClient(app) as client:
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401
