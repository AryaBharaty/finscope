from fastapi import FastAPI
from backend.app.api import metrics
from backend.app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FinScope API")

app.include_router(metrics.router)

@app.get("/")
def root():
    return {"status": "ok", "service": "FinScope API"}
