from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas import SubjectResponse, TopicResponse, SubjectWithTopics
from app.models import Subject, Topic
from typing import List

app = FastAPI(
    title="AI Adaptive Learning System",
    description="Backend API for Personalized Learning Platform",
    version="1.0.0"
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db  #pauses the function
    finally:
        db.close()


@app.get("/")
def health_check():
    return {"status": "Backend is running"}


@app.get("/subjects", response_model=List[SubjectResponse])
def get_subjects(db: Session = Depends(get_db)):
    subjects = db.query(Subject).all()
    return subjects


@app.get("/subjects/{subject_id}/topics", response_model=List[TopicResponse])
def get_topics_by_subject(subject_id: int, db: Session = Depends(get_db)):
    topics = db.query(Topic).filter(Topic.subject_id == subject_id).all()

    if not topics:
        raise HTTPException(status_code=404, detail="No topics found")

    return topics


@app.get("/subjects/{subject_id}", response_model=SubjectWithTopics)
def get_subject_with_topics(subject_id: int, db: Session = Depends(get_db)):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()

    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    return subject