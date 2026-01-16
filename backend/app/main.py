from fastapi import FastAPI

app = FastAPI(
    title="FinScope API",
    description="Personal Finance Analytics Platform",
    version="0.1.0"
)

@app.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "FinScope API"
    }
