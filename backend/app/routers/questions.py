from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/questions",
    tags=["Questions"]
)

@router.post("/", response_model=schemas.QuestionResponse)
def create_question(question: schemas.QuestionCreate, db: Session = Depends(get_db)):

    topic = db.query(models.Topic).filter(
        models.Topic.id == question.topic_id
    ).first()

    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    new_question = models.Question(**question.dict())

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return new_question


@router.get("/topic/{topic_id}", response_model=list[schemas.QuestionResponse])
def get_questions_by_topic(topic_id: int, db: Session = Depends(get_db)):

    questions = db.query(models.Question).filter(
        models.Question.topic_id == topic_id
    ).all()

    if not questions:
        raise HTTPException(status_code=404, detail="No questions found")

    return questions


@router.get("/{question_id}", response_model=schemas.QuestionResponse)
def get_question_by_id(question_id: int, db: Session = Depends(get_db)):

    question = db.query(models.Question).filter(
        models.Question.id == question_id
    ).first()

    if not question:
        raise HTTPException(status_code=404, detail="No question found")

    return question


@router.delete("/{question_id}", status_code=204)
def delete_questions_by_id(question_id: int, db: Session = Depends(get_db)):

    question = db.query(models.Question).filter(
        models.Question.id == question_id
    ).first()

    if not question:
        raise HTTPException(status_code=404, detail="No question found")

    try:
        db.delete(question)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
