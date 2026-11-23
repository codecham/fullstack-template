from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext
from sqlalchemy import Engine

from app.models import Base


def test_migrations_match_the_models(db_engine: Engine) -> None:
    """Fails when a model changed but no migration was created (`make migration m="..."`)."""
    with db_engine.connect() as connection:
        context = MigrationContext.configure(connection)

        differences = compare_metadata(context, Base.metadata)

    assert differences == []
