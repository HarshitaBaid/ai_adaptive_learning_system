from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
import pandas as pd

db: Session = SessionLocal()

attempts = db.query(models.QuizAttempt).all()

data = []

for a in attempts:

    accuracy = a.score / a.total_questions if a.total_questions else 0

    data.append({
        "student_id": a.student_id,
        "topic_id": a.topic_id,
        "score": a.score,
        "total_questions": a.total_questions,
        "accuracy": accuracy,
        "time_taken": a.time_taken
    })

df = pd.DataFrame(data)

# Aggregate student-topic performance
dataset = df.groupby(["student_id","topic_id"]).agg(
    attempts=("score","count"),
    avg_score=("score","mean"),
    accuracy=("accuracy","mean"),
    avg_time=("time_taken","mean")
).reset_index()

dataset.to_csv("ml_dataset.csv", index=False)

db.close()

print("ML dataset created successfully")