from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

from app.core.config import settings
from app.db.base import Base

# Import all SQLAlchemy models so they are registered
# with Base.metadata for Alembic.
from app.models.project import Project
from app.models.project_snapshot import ProjectSnapshot
from app.models.user import User


# Alembic Config object
config = context.config

# Use Aurex's existing database configuration.
# We deliberately use the same DATABASE_URL as the application.
config.set_main_option(
    "sqlalchemy.url",
    settings.database_url.replace("%", "%%"),
)

# Configure Python logging from alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# SQLAlchemy metadata used for autogenerate.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations without creating a database connection."""
    url = settings.database_url

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named",
        },
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations using a live database connection."""
    connect_args = {}

    if settings.database_url.startswith("sqlite"):
        connect_args = {
            "check_same_thread": False,
        }

    connectable = create_engine(
        settings.database_url,
        connect_args=connect_args,
        pool_pre_ping=True,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()

    connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()