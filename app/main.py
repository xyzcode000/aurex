from fastapi import FastAPI


from app.db.database import Base, engine
from app.models.project import Project
from app.models.financial_record import FinancialRecord
from app.routers.project import router as project_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Aurex Backend",
    description="Project Intelligence & Risk Investigation Engine",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Aurex Backend is running"
    }


app.include_router(project_router)