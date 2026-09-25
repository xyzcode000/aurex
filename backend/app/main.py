from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

app = FastAPI(
    title="Aurex API",
    description="Project Intelligence & Risk Investigation Engine",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def root():
    return {
        "project": "Aurex",
        "message": "Project Intelligence & Risk Investigation Engine",
        "status": "online",
        "version": "0.1.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "aurex-backend",
    }
@app.get("/api/risk/{project_id}")
def get_project_risk(project_id: str):
    return {
        "project_id": project_id,
        "cost_risk": 82,
        "schedule_risk": 74,
        "progress_risk": 91,
        "anomaly_score": 63,
        "overall_risk": 84,
        "risk_level": "MEDIUM" if project_id == "AUREX-002" else "HIGH",
        "evidence": [
            "Project cost is above the planned budget",
            "Schedule is showing delays",
            "Progress is below expected level",
            "Anomaly detected in recent project data",
        ],
    }