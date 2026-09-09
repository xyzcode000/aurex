from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


# =========================================================
# DATABASE ENGINE CONFIGURATION
# =========================================================

connect_args = {}

if settings.database_url.startswith("sqlite"):
    connect_args = {
        "check_same_thread": False,
    }


engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    pool_pre_ping=True,
)


# =========================================================
# DATABASE SESSION
# =========================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# =========================================================
# DATABASE DEPENDENCY
# =========================================================

def get_db():
    """
    Provides a database session for each API request.

    The session is always closed after the request,
    even if an exception occurs.
    """

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()