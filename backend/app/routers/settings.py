from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from passlib.context import CryptContext

router = APIRouter(
    prefix="/settings",
    tags=["Settings"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ------------------ UPDATE NAME ------------------
@router.put("/update-name/{student_id}")
def update_name(student_id: int, payload: schemas.UpdateName, db: Session = Depends(get_db)):
    
    user = db.query(models.Student).filter(models.Student.id == student_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = payload.name
    db.commit()
    db.refresh(user)

    return {"message": "Name updated successfully"}


# ------------------ CHANGE PASSWORD ------------------
@router.put("/change-password/{student_id}")
def change_password(student_id: int, payload: schemas.ChangePassword, db: Session = Depends(get_db)):

    user = db.query(models.Student).filter(models.Student.id == student_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # check old password
    if not pwd_context.verify(payload.old_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Old password is incorrect")

    # hash new password
    user.password_hash = pwd_context.hash(payload.new_password)

    db.commit()

    return {"message": "Password updated successfully"}