from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database import get_db
from app import schemas
from app.models import Student
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