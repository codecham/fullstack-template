"""Alembic entry point: connects to the database and runs the migrations."""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.core.config import get_settings
from app.models import Base  # importing app.models registers every model on Base.metadata

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# The models' tables: `alembic revision --autogenerate` compares them with the database
target_metadata = Base.metadata
# Use the app's database unless a URL was already set (the tests point it to the test database).
# "%" must be doubled because Alembic's config uses ConfigParser interpolation.
if not config.get_main_option("sqlalchemy.url"):
    config.set_main_option("sqlalchemy.url", get_settings().database_url.replace("%", "%%"))


def run_migrations_offline() -> None:
    """Generate SQL without a database connection (`alembic upgrade head --sql`)."""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Apply the migrations to the database."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
