from fastapi import FastAPI

from app.api.projects import router as projects_router
from app.api.auth import router as auth_router

from app.core.config import settings

from app.db.base import Base
from app.db.session import engine

# Import models so SQLAlchemy registers them with Base
from app.models.project import Project
from app.models.user import User


app = FastAPI(
    title=settings.app_name,
    description="Project Intelligence & Risk Investigation Engine",
    version=settings.app_version,
    debug=settings.debug,
)


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

@app.on_event("startup")
def create_database_tables():
    """
    Create database tables when Aurex starts.
    """
    Base.metadata.create_all(bind=engine)


# =========================================================
# API ROUTES
# =========================================================

# Project APIs
app.include_router(
    projects_router,
    prefix="/api",
)

# Authentication APIs
app.include_router(
    auth_router,
    prefix="/api",
)


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():
    return {
        "project": settings.app_name,
        "message": "Project Intelligence & Risk Investigation Engine",
        "status": "online",
        "version": settings.app_version,
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "aurex-backend",
        "environment": settings.environment,
    }