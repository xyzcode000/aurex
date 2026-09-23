from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.api.projects import router as projects_router
from app.api.auth import router as auth_router

from app.core.config import settings


# =========================================================
# APPLICATION LIFESPAN
# =========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown lifecycle.

    Database schema changes are managed exclusively through
    Alembic migrations.
    """

    yield


app = FastAPI(
    title=settings.app_name,
    description="Project Intelligence & Risk Investigation Engine",
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)


# =========================================================
# GLOBAL ERROR HANDLERS
# =========================================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    """
    Handle invalid request data with a clean API response.

    FastAPI/Pydantic validation errors can contain Python
    exception objects inside the error context. Those objects
    are converted to strings before returning JSON.
    """

    validation_details = []

    for error in exc.errors():
        clean_error = error.copy()

        if "ctx" in clean_error:
            clean_error["ctx"] = {
                key: str(value)
                for key, value in clean_error["ctx"].items()
            }

        validation_details.append(clean_error)

    return JSONResponse(
        status_code=422,
        content={
            "error": "validation_error",
            "message": "The request contains invalid data.",
            "details": validation_details,
        },
    )


@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(
    request: Request,
    exc: SQLAlchemyError,
):
    """
    Handle database errors without exposing internal
    database details to the client.
    """

    return JSONResponse(
        status_code=500,
        content={
            "error": "database_error",
            "message": (
                "A database error occurred while "
                "processing the request."
            ),
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(
    request: Request,
    exc: Exception,
):
    """
    Handle unexpected application errors safely.

    Internal exception details are intentionally not
    returned to the client.
    """

    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "An unexpected application error occurred.",
        },
    )


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