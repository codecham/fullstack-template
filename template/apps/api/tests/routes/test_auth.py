import jwt
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import User

VALID_USER = {"email": "Alice@Mail.com", "password": "correct horse"}


def test_register_creates_user(client: TestClient, db: Session) -> None:
    response = client.post("/auth/register", json=VALID_USER)

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "alice@mail.com"
    assert body["is_active"] is True
    assert "password" not in body
    assert "hashed_password" not in body


def test_register_stores_a_hashed_password(client: TestClient, db: Session) -> None:
    client.post("/auth/register", json=VALID_USER)

    user = db.scalar(select(User).where(User.email == "alice@mail.com"))

    assert user is not None
    assert user.hashed_password != VALID_USER["password"]
    assert user.hashed_password.startswith("$argon2")


def test_register_rejects_duplicate_email(client: TestClient, db: Session) -> None:
    client.post("/auth/register", json=VALID_USER)

    response = client.post(
        "/auth/register",
        json={"email": "ALICE@mail.com", "password": "another password"},
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "Email already registered"}


def test_register_rejects_short_password(client: TestClient, db: Session) -> None:
    response = client.post("/auth/register", json={"email": "bob@mail.com", "password": "short"})

    assert response.status_code == 422


def test_register_rejects_invalid_email(client: TestClient, db: Session) -> None:
    response = client.post(
        "/auth/register", json={"email": "not-an-email", "password": "long enough"}
    )

    assert response.status_code == 422


def register_alice(client: TestClient) -> str:
    """Create Alice's account and return her user id."""
    response = client.post("/auth/register", json=VALID_USER)
    return str(response.json()["id"])


def test_login_returns_a_token_for_the_user(client: TestClient, db: Session) -> None:
    user_id = register_alice(client)

    response = client.post(
        "/auth/login", data={"username": "alice@mail.com", "password": "correct horse"}
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    settings = get_settings()
    payload = jwt.decode(
        body["access_token"],
        settings.jwt_secret_key.get_secret_value(),
        algorithms=[settings.jwt_algorithm],
    )
    assert payload["sub"] == user_id


def test_login_rejects_a_wrong_password(client: TestClient, db: Session) -> None:
    register_alice(client)

    response = client.post(
        "/auth/login", data={"username": "alice@mail.com", "password": "wrong password"}
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect email or password"}


def test_login_rejects_an_unknown_email(client: TestClient, db: Session) -> None:
    response = client.post(
        "/auth/login", data={"username": "nobody@mail.com", "password": "correct horse"}
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect email or password"}
