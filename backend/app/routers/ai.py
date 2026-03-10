import joblib
import pandas as pd
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import QuestionResponse
from app.models import QuizAttempt, Question

router = APIRouter(prefix="/ai", tags=["AI"])

model = joblib.load("ml/weakness_model.pkl")


@router.get("/predict/{student_id}")
def predict_student_performance(student_id: int, db: Session = Depends(get_db)):

    attempts = db.query(QuizAttempt).filter(
        QuizAttempt.student_id == student_id
    ).all()

    topic_data = {}

    for a in attempts:
        acc = a.score / a.total_questions if a.total_questions else 0

        topic_data.setdefault(a.topic_id, []).append({
            "score": a.score,
            "accuracy": acc,
            "time": a.time_taken
        })

    predictions = []

    for topic_id, records in topic_data.items():

        attempts_count = len(records)
        avg_score = sum(r["score"] for r in records) / attempts_count
        avg_time = sum(r["time"] for r in records) / attempts_count

        X = pd.DataFrame([{
            "attempts": attempts_count,
            "avg_score": avg_score,
            "avg_time": avg_time
        }])

        difficulty = model.predict(X)[0]

        predictions.append({
            "topic_id": topic_id,
            "recommended_difficulty": difficulty
        })

    return predictions


@router.get("/recommend/{student_id}", response_model=list[QuestionResponse])
def ai_recommend_questions(student_id: int, db: Session = Depends(get_db)):

    attempts = db.query(QuizAttempt).filter(
        QuizAttempt.student_id == student_id
    ).all()

    topic_data = {}

    for a in attempts:
        accuracy = a.score / a.total_questions if a.total_questions else 0

        topic_data.setdefault(a.topic_id, []).append({
            "score": a.score,
            "accuracy": accuracy,
            "time": a.time_taken
        })

    recommended_questions = []

    for topic_id, records in topic_data.items():

        attempts_count = len(records)
        avg_score = sum(r["score"] for r in records) / attempts_count
        avg_time = sum(r["time"] for r in records) / attempts_count

        X = pd.DataFrame([{
            "attempts": attempts_count,
            "avg_score": avg_score,
            "avg_time": avg_time
        }])

        difficulty = model.predict(X)[0]

        questions = db.query(Question).filter(
            Question.topic_id == topic_id,
            Question.difficulty_level == difficulty
        ).limit(3).all()

        recommended_questions.extend(questions)

    return recommended_questions