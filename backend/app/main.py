from fastapi import FastAPI

from app.api.projects import router as projects_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine

# Import models so SQLAlchemy registers them with Base
from app.models.project import Project


app = FastAPI(
    title=settings.app_name,
    description="Project Intelligence & Risk Investigation Engine",
    version=settings.app_version,
    debug=settings.debug,
)


# Create database tables
@app.on_event("startup")
def create_database_tables():
    Base.metadata.create_all(bind=engine)


# API Routes
app.include_router(
    projects_router,
    prefix="/api",
)


@app.get("/")
def root():
    return {
        "project": settings.app_name,
        "message": "Project Intelligence & Risk Investigation Engine",
        "status": "online",
        "version": settings.app_version,
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "aurex-backend",
        "environment": settings.environment,
    }