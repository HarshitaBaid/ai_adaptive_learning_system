from fastapi import FastAPI
from app.database import engine
from sqlalchemy import text

app = FastAPI(
    title="AI Adaptive Learning System",
    description="Backend API for Personalized Learning Platform",
    version="1.0.0"
)

@app.get("/")
def health_check():
    return {"status": "Backend is running"}

@app.get("/test-db")
def test_db():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return {"database_status": "Connected", "result": result.scalar()}