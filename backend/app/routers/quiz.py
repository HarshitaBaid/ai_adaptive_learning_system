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
        models.Topic.id == data.topic_id
    ).first()
    print("hdsgvhd")
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    new_attempt = models.QuizAttempt(
        student_id=data.student_id,
        topic_id=data.topic_id,
        score=0,
        total_questions=0
    )

    db.add(new_attempt)
    db.commit()
    db.refresh(new_attempt)

    return new_attempt


@router.get("/{topic_id}", response_model=list[schemas.QuestionResponse])
def get_quiz_questions(topic_id: int, db: Session = Depends(get_db)):

    questions = db.query(models.Question).filter(
        models.Question.topic_id == topic_id
    ).all()

    if not questions:
        raise HTTPException(status_code=404, detail="No questions found for this topic")

    return questions


@router.post("/submit")
def submit_quiz(data: schemas.QuizSubmit, db: Session = Depends(get_db)):

    attempt = db.query(models.QuizAttempt).filter(
        models.QuizAttempt.id == data.attempt_id
    ).first()

    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")

    score = 0
    total = 0
    
    for question_id, selected_option in data.answers.items():

        question = db.query(models.Question).filter(
            models.Question.id == question_id,
            models.Question.topic_id == attempt.topic_id
        ).first()

        if not question:
            continue

        total += 1
        is_correct = False

        if question.correct_option == selected_option:
            score += 1
            is_correct = True
        
        response = models.Response(
            quiz_attempt_id=attempt.id,
            question_id=question_id,
            selected_option=selected_option,
            is_correct=is_correct
        )

        db.add(response)

    attempt.time_taken = data.time_taken
    attempt.score = score
    attempt.total_questions = total

    db.commit()

    percentage = (score / total * 100) if total > 0 else 0
    
    return {
        "score": score,
        "total": total,
        "percentage": percentage
    }