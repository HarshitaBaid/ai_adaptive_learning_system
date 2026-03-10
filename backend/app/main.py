from fastapi import FastAPI
from app.routers import topics, subjects, questions, quiz, students, ai

app = FastAPI(
    title="AI Adaptive Learning System",
    description="Backend API for Personalized Learning Platform",
    version="1.0.0"
)

@app.get("/")
def health_check():
    return {"status": "Backend is running"}

# Include routers
app.include_router(subjects.router)
app.include_router(topics.router)
app.include_router(questions.router)
app.include_router(quiz.router)
app.include_router(students.router)
app.include_router(ai.router)