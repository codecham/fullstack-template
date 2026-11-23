from fastapi.testclient import TestClient

from tests.fakes import FakeSession


def test_health_returns_ok(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_db_returns_ok_when_database_answers(
    client: TestClient, fake_db: FakeSession
) -> None:
    response = client.get("/health/db")

    assert response.status_code == 200
    assert response.json() == {"database": "ok"}


def test_health_db_returns_503_when_database_is_down(
    client: TestClient, fake_db: FakeSession
) -> None:
    fake_db.fail = True

    response = client.get("/health/db")

    assert response.status_code == 503
    assert response.json() == {"detail": "Database unavailable"}
