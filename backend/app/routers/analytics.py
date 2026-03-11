from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import QuizAttempt

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/student/{student_id}")
def student_analytics(student_id: int, db: Session = Depends(get_db)):
    
    attempts = db.query(QuizAttempt).filter(
        QuizAttempt.student_id == student_id
    ).all()
    
    if not attempts:
        return {"message":"No quiz attempts found"}, 404
    
    total_attempts = len(attempts)
    
    total_score = sum(a.score for a in attempts)
    total_questions = sum(a.total_questions for a in attempts)

    avg_accuracy = (total_score / total_questions) * 100 if total_questions else 0

    avg_time = sum(a.time_taken for a in attempts) / total_attempts

    topic_scores = {}

    for a in attempts:

        percentage = (a.score / a.total_questions) * 100 if a.total_questions else 0

        topic_scores.setdefault(a.topic_id, []).append(percentage)
        
    weak_topics = []
    strong_topics = []
    
    for topic_id, scores in topic_scores.items():

        avg = sum(scores) / len(scores)

        if avg < 60:
            weak_topics.append(topic_id)
        else:
            strong_topics.append(topic_id)

    return {
        "student_id": student_id,
        "total_attempts": total_attempts,
        "average_accuracy": round(avg_accuracy, 2),
        "average_time_per_quiz": round(avg_time, 2),
        "weak_topics": weak_topics,
        "strong_topics": strong_topics
    }