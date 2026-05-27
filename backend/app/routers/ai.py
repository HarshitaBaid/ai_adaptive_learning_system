from http.client import HTTPException
import joblib
import pandas as pd
from fastapi import APIRouter, Depends
from collections import defaultdict
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import QuestionResponse, StudentProgressResponse
from app.models import QuizAttempt, Question, Response, Feedback

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


@router.get("/recommend/{student_id}")
def ai_recommend_questions(student_id: int, db: Session = Depends(get_db)):

    # fetch attempts

    attempts = db.query(QuizAttempt).filter(
        QuizAttempt.student_id == student_id
    ).all()

    if not attempts:
        return []


    topic_data = {}

    for a in attempts:
        accuracy = a.score / a.total_questions if a.total_questions else 0

        topic_data.setdefault(a.topic_id, []).append({
            "score": a.score,
            "accuracy": accuracy,
            "time": a.time_taken
        })

    # getting attempted questions

    attempted_question_ids = db.query(Response.question_id).join(
        QuizAttempt,
        QuizAttempt.id == Response.quiz_attempt_id
    ).filter(QuizAttempt.student_id == student_id).all()

    attempted_question_ids = list(set([q[0] for q in attempted_question_ids]))

    # calculate weakness

    topic_scores = []

    for topic_id, records in topic_data.items():

        avg_accuracy = sum(r["accuracy"] for r in records) / len(records)

        topic_scores.append({
            "topic_id": topic_id,
            "accuracy": avg_accuracy
        })

    topic_scores.sort(key=lambda x: x["accuracy"])

    # question recommendation

    recommended_questions = []

    for topic in topic_scores:

        topic_id = topic["topic_id"]
        records = topic_data[topic_id]

        attempts_count = len(records)
        avg_score = sum(r["score"] for r in records) / attempts_count
        valid_times = [r["time"] for r in records if r["time"] is not None]

        avg_time = sum(valid_times) / len(valid_times) if valid_times else 0    

        # applying model

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
        ).limit(2).all()

        if not questions:
            questions = db.query(Question).filter(
                Question.topic_id == topic_id,
                ~Question.id.in_(attempted_question_ids)
            ).limit(2).all()

        if not questions:
            questions = db.query(Question).filter(
                Question.topic_id == topic_id
            ).limit(2).all()

        recommended_questions.extend(questions)

        if len(recommended_questions) >= 5:
            break

    return recommended_questions[:5]


@router.get("/progress/{student_id}")
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

    accuracy = (correct_answers / total_attempts * 100) if total_attempts else 0

    # topic stats

    topic_stats = defaultdict(lambda: {"correct": 0, "total": 0})

    for a in attempts:

        for r in a.responses:
            topic = r.question.topic.name

            topic_stats[topic]["total"] += 1

            if r.is_correct:
                topic_stats[topic]["correct"] += 1

        # FEEDBACK
        feedbacks = db.query(Feedback).filter(
            Feedback.attempt_id == a.id
        ).all()

        for f in feedbacks:
            question = db.query(Question).filter(
                Question.id == f.question_id
            ).first()

            if question:
                topic = question.topic.name

                topic_stats[topic]["total"] += 1


    strong_topics = []
    weak_topics = []

    for topic, stats in topic_stats.items():
        topic_accuracy = stats["correct"] / stats["total"]

        if topic_accuracy >= 0.7:
            strong_topics.append({
                "topic": topic,
                "accuracy": round(topic_accuracy * 100, 2)
            })

        elif topic_accuracy <= 0.4:
            weak_topics.append({
                "topic": topic,
                "accuracy": round(topic_accuracy * 100, 2)
            })

    # returning response

    return {
        "student_id": student_id,
        "total_attempts": total_attempts,
        "correct_answers": correct_answers,
        "accuracy": round(accuracy, 2),
        "strong_topics": strong_topics,
        "weak_topics": weak_topics
    }
    
    
@router.post("/submit-practice")
def submit_practice(data: dict, db: Session = Depends(get_db)):

    student_id = data["student_id"]
    answers = data["answers"]

    #attempt created

    attempt = QuizAttempt(
        student_id=student_id,
        topic_id=None,  # mixed topics
        score=0,
        total_questions=len(answers),
        time_taken=0,
        is_practice=True
    )

    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    score = 0

    for q_id, selected in answers.items():

        question = db.query(Question).filter(
            Question.id == int(q_id)
        ).first()

        is_correct = (selected == question.correct_option)

        if is_correct:
            score += 1

        response = Response(
            quiz_attempt_id=attempt.id,
            question_id=int(q_id),
            selected_option=selected,
            is_correct=is_correct
        )

        db.add(response)

    # updation of score

    attempt.score = score

    db.commit()

    return {
        "score": score,
        "total": len(answers),
        "percentage": (score / len(answers)) * 100
    }
