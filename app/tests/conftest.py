import pytest
from fastapi.testclient import TestClient
import os


from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker

from app.db.database import Base, get_db
from app.main import app


# Original database URL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")


# Create test database URL
original_url = make_url(DATABASE_URL)
test_database_url = original_url.set(database="aurex_test")


# Connect to PostgreSQL default database
admin_url = original_url.set(database="postgres")
admin_engine = create_engine(admin_url)

with admin_engine.connect().execution_options(
    isolation_level="AUTOCOMMIT"
) as connection:
    result = connection.execute(
        text(
            "SELECT 1 FROM pg_database WHERE datname = 'aurex_test'"
        )
    )

    if result.scalar() is None:
        connection.execute(text("CREATE DATABASE aurex_test"))

admin_engine.dispose()


# Test database engine
test_engine = create_engine(
    test_database_url,
    pool_pre_ping=True
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


# Create tables inside test database
Base.metadata.create_all(bind=test_engine)

@pytest.fixture(autouse=True)
def clean_test_database():
    with test_engine.connect() as connection:
        connection.execute(
            text(
                """
                TRUNCATE TABLE
                    milestones,
                    progress_records,
                    financial_records,
                    projects
                RESTART IDENTITY CASCADE
                """
            )
        )
        connection.commit()

@pytest.fixture
def client():
    return TestClient(app)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db