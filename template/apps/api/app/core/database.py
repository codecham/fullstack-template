from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings

# pool_pre_ping: transparently replace connections dropped by the database (e.g. after a restart)
engine = create_engine(get_settings().database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)


def get_db() -> Iterator[Session]:
    """FastAPI dependency: one database session per request, closed afterwards."""
    with SessionLocal() as session:
        yield session
