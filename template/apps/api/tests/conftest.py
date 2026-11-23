"""Shared test setup: pytest loads this file automatically before the tests.

The tests use a real PostgreSQL database named "<POSTGRES_DB>_test", recreated at the
start of every run and migrated with Alembic. Each test runs inside a transaction
that is rolled back afterwards, so tests never see each other's data.
"""

from collections.abc import Iterator
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.main import app
from tests.fakes import FakeSession

settings = get_settings()
TEST_DB_NAME = f"{settings.postgres_db}_test"
TEST_DATABASE_URL = settings.model_copy(update={"postgres_db": TEST_DB_NAME}).database_url
# The "postgres" database always exists: we connect to it to (re)create the test database
ADMIN_DATABASE_URL = settings.model_copy(update={"postgres_db": "postgres"}).database_url
ALEMBIC_INI = Path(__file__).resolve().parents[1] / "alembic.ini"


def recreate_test_database() -> None:
    admin_engine = create_engine(ADMIN_DATABASE_URL, isolation_level="AUTOCOMMIT")
    try:
        with admin_engine.connect() as connection:
            connection.execute(text(f'DROP DATABASE IF EXISTS "{TEST_DB_NAME}" WITH (FORCE)'))
            connection.execute(text(f'CREATE DATABASE "{TEST_DB_NAME}"'))
    except OperationalError as error:
        pytest.exit(
            f"Cannot reach PostgreSQL at {settings.postgres_host}:{settings.postgres_port}. "
            "Start it with `make db` (or run the tests with `make test`).\n"
            f"Error: {error.orig}",
            returncode=1,
        )
    finally:
        admin_engine.dispose()


@pytest.fixture(scope="session")
def db_engine() -> Iterator[Engine]:
    """A fresh, fully migrated test database, created once for the whole test run."""
    recreate_test_database()
    alembic_config = Config(ALEMBIC_INI)
    alembic_config.set_main_option("sqlalchemy.url", TEST_DATABASE_URL.replace("%", "%%"))
    command.upgrade(alembic_config, "head")

    engine = create_engine(TEST_DATABASE_URL)
    yield engine
    engine.dispose()


@pytest.fixture
def db_session(db_engine: Engine) -> Iterator[Session]:
    """A database session whose changes are rolled back after each test."""
    connection = db_engine.connect()
    transaction = connection.begin()
    # "create_savepoint": session.commit() in our code only commits a savepoint,
    # so the outer transaction can still undo everything at the end of the test
    session = Session(bind=connection, join_transaction_mode="create_savepoint")
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client() -> Iterator[TestClient]:
    """An HTTP client that calls the app directly, without a real server."""
    with TestClient(app) as test_client:
        yield test_client
    # Undo any dependency override so it cannot leak into the next test
    app.dependency_overrides.clear()


@pytest.fixture
def db(db_session: Session) -> Session:
    """Make the routes use the test database session for this test."""
    app.dependency_overrides[get_db] = lambda: db_session
    return db_session


@pytest.fixture
def fake_db() -> FakeSession:
    """Replace the real database session with a fake one (e.g. to simulate an outage)."""
    session = FakeSession()
    app.dependency_overrides[get_db] = lambda: session
    return session
