from fastapi import FastAPI

app = FastAPI(
    title="Aurex API",
    description="Project Intelligence & Risk Investigation Engine",
    version="0.1.0",
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