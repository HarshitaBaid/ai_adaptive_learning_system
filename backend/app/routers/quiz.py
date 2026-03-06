from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/quiz",
    tags=["Quiz"]
)

@router.post("/start", response_model=schemas.QuizAttemptResponse)
def start_quiz(data: schemas.QuizStart, db: Session = Depends(get_db)):

    # Check topic exists
    topic = db.query(models.Topic).filter(
        models.Topic.id == data.id
    ).first()

    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    new_attempt = models.QuizAttempt(
        student_id=data.student_id,
        topic_id=data.id,
        score=0,
        total_questions=0
    )

    db.add(new_attempt)
    db.commit()
    db.refresh(new_attempt)

    return new_attempt