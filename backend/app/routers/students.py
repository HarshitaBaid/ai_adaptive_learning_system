from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database import get_db
from app import schemas
from app.models import Student, QuizAttempt, Question
from app.utils import hash_password, verify_password

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.post("/register", response_model=schemas.StudentResponse)
def register_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):

    email = student.email.lower()
    existing = db.query(Student).filter(Student.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(student.password)

    new_student = Student(
        name=student.name,
        email=email,
        password_hash=hashed
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


@router.post("/login", status_code=200)
def login_student(student: schemas.StudentLogIn, db: Session = Depends(get_db)):

    email = student.email.lower()

    existing = db.query(Student).filter(Student.email == email).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Invalid email or password")

    if not verify_password(student.password, existing.password_hash):
        raise HTTPException(status_code=404, detail="Invalid email or password")

    return {
        "message": "Login successful",
        "student_id": existing.id,
        "name": existing.name
    }
    
    
@router.get("/{student_id}/attempts", response_model=list[schemas.AttemptHistoryResponse])
def student_attempt_history(student_id: int, db: Session = Depends(get_db)):

    attempt_data = db.query(QuizAttempt).filter(QuizAttempt.student_id == student_id).all()

    if not attempt_data:
        raise HTTPException(status_code=404, detail="Student id not found")

    result = []

    for attempt in attempt_data:
        percentage = 0
        if attempt.total_questions:
            percentage = (attempt.score / attempt.total_questions) * 100

        result.append({
            "id": attempt.id,
            "topic_id": attempt.topic_id,
            "score": attempt.score,
            "total_questions": attempt.total_questions,
            "percentage": percentage,
            "attempt_date": attempt.attempt_date,
            "time_taken": attempt.time_taken
        })

    return result


@router.get("/{student_id}/weak-topics")
def weak_topics(student_id: int, db: Session = Depends(get_db)):

    attempts = db.query(QuizAttempt).filter(
        QuizAttempt.student_id == student_id
    ).all()

    topic_scores = {}

    for attempt in attempts:
        percentage = (attempt.score / attempt.total_questions) * 100

        topic_scores.setdefault(attempt.topic_id, []).append(percentage)

    result = []

    for topic_id, scores in topic_scores.items():
        avg = sum(scores) / len(scores)

        status = "Weak" if avg < 60 else "Strong"

        result.append({
            "topic_id": topic_id,
            "average_percentage": avg,
            "status": status
        })

    return result


@router.get("/{student_id}/recommendations", response_model=list[schemas.QuestionResponse])
def recommend_questions(student_id: int, db: Session = Depends(get_db)):

    attempts = db.query(QuizAttempt).filter(
        QuizAttempt.student_id == student_id
    ).all()

    topic_scores = {}

    for attempt in attempts:
        percentage = (attempt.score / attempt.total_questions) * 100
        topic_scores.setdefault(attempt.topic_id, []).append(percentage)

    recommendations = []

    for topic_id, scores in topic_scores.items():

        avg = sum(scores) / len(scores)

        # Only recommend weak topics
        if avg < 60:

            if avg < 40:
                difficulty = "easy"
            else:
                difficulty = "medium"

            questions = db.query(Question).filter(
                Question.topic_id == topic_id,
                Question.difficulty_level == difficulty
            ).limit(5).all()

            recommendations.extend(questions)

    return recommendations[:10]