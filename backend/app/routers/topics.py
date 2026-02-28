from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/topics",
    tags=["Topics"]
)

@router.post("/", response_model=schemas.TopicResponse)
def create_topic(topic: schemas.TopicCreate, db: Session = Depends(get_db)):

    # Check if subject exists
    subject = db.query(models.Subject).filter(
        models.Subject.id == topic.subject_id
    ).first()

    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    # Create topic
    new_topic = models.Topic(
        name=topic.name,
        subject_id=topic.subject_id
    )

    try:
        db.add(new_topic)  #prepare object
        db.commit()        # save to db
        db.refresh(new_topic)  #reload from db

        return new_topic
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))