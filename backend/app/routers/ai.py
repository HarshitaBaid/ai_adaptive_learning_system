from http.client import HTTPException
import joblib
import pandas as pd
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import QuestionResponse, StudentProgressResponse
from app.models import QuizAttempt, Question, Response

router = APIRouter(prefix="/ai", tags=["AI"])

model = joblib.load("app/ml/weakness_model.pkl")


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

    attempted_question_ids = db.query(Response.question_id).join(
        QuizAttempt,
        QuizAttempt.id == Response.quiz_attempt_id
    ).filter(QuizAttempt.student_id == student_id).all()
    
    attempted_question_ids = list(set([q[0] for q in attempted_question_ids]))
    print(attempted_question_ids)
    
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
            Question.difficulty_level == difficulty,
            ~Question.id.in_(attempted_question_ids)
        ).limit(3).all()
        
        # fallback 1: ignore difficulty
        if not questions:
            questions = db.query(Question).filter(
                Question.topic_id == topic_id,
                ~Question.id.in_(attempted_question_ids)
            ).limit(3).all()

        # fallback 2: allow attempted questions
        if not questions:
            questions = db.query(Question).filter(
                Question.topic_id == topic_id
            ).limit(3).all()

        recommended_questions.extend(questions)

    return recommended_questions


@router.get("/progress/{student_id}", response_model=StudentProgressResponse)
def student_progress(student_id: int, db: Session = Depends(get_db)):

    attempts = db.query(QuizAttempt).filter(
        QuizAttempt.student_id == student_id
    ).all()

    if not attempts:
        raise HTTPException(status_code=404, detail="No attempts found")

    total_attempts = sum(len(a.responses) for a in attempts)

    correct_answers = sum(
        1 for a in attempts for r in a.responses if r.is_correct
    )

    accuracy = (correct_answers / total_attempts) * 100

    topic_stats = {}

    for a in attempts:
        for r in a.responses:

            topic = r.question.topic.name

            if topic not in topic_stats:
                topic_stats[topic] = {"correct":0, "total":0}

            topic_stats[topic]["total"] += 1

            if r.is_correct:
                topic_stats[topic]["correct"] += 1

    strong_topics = []
    weak_topics = []

    for topic, stats in topic_stats.items():
        topic_accuracy = stats["correct"] / stats["total"]

        if topic_accuracy >= 0.7:
            strong_topics.append(topic)
        elif topic_accuracy <= 0.4:
            weak_topics.append(topic)

    return {
        "student_id": student_id,
        "total_attempts": total_attempts,
        "correct_answers": correct_answers,
        "accuracy": round(accuracy,2),
        "strong_topics": strong_topics,
        "weak_topics": weak_topics
    }