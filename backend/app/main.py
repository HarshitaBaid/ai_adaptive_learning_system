from fastapi import FastAPI

app = FastAPI(
    title="AI Adaptive Learning System",
    description="Backend API for Personalized Learning Platform",
    version="1.0.0"
)

@app.get("/")
def health_check():
    return {"status": "Backend is running"}