from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.database import get_db
from app.models import Subject, Topic
from app.schemas import SubjectResponse, TopicResponse, SubjectWithTopics

router = APIRouter(
    prefix="/subjects",
    tags=["Subjects"]
)

@router.get("/", response_model=List[SubjectResponse])
def get_subjects(db: Session = Depends(get_db)):
    return db.query(Subject).all()


@router.get("/{subject_id}/topics", response_model=List[TopicResponse])
def get_topics_by_subject(subject_id: int, db: Session = Depends(get_db)):
    topics = db.query(Topic).filter(Topic.subject_id == subject_id).all()

    if not topics:
        raise HTTPException(status_code=404, detail="No topics found")

    return topics


@router.get("/{subject_id}", response_model=SubjectWithTopics)
def get_subject_with_topics(subject_id: int, db: Session = Depends(get_db)):
    subject = db.query(Subject).options(joinedload(Subject.topics)).filter(Subject.id == subject_id).first()

    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    return subject