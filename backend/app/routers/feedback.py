from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Feedback
from app.schemas import FeedbackCreate

router = APIRouter()

@router.post("/feedback")
def submit_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    
    new_feedback = Feedback(
        attempt_id=feedback.attempt_id,
        question_id=feedback.question_id,
        corrected_answer=feedback.corrected_answer
    )

    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)

    return {"message": "Feedback saved successfully"}