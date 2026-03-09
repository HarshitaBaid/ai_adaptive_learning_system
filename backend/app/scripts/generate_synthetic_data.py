from faker import Faker
import random
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models

fake = Faker()

db: Session = SessionLocal()

# create students
for _ in range(100):
    student = models.Student(
        name=fake.name(),
        email=fake.unique.email(),
        password_hash="hashedpassword"
    )
    db.add(student)

db.commit()

students = db.query(models.Student).all()
topics = db.query(models.Topic).all()
questions = db.query(models.Question).all()

for student in students:

    for _ in range(random.randint(20, 40)):

        topic = random.choice(topics)

        topic_questions = [q for q in questions if q.topic_id == topic.id]
        if not topic_questions:
            continue

        selected_questions = random.sample(
            topic_questions,
            min(10, len(topic_questions))
        )

        attempt = models.QuizAttempt(
            student_id=student.id,
            topic_id=topic.id,
            total_questions=len(selected_questions),
            time_taken=random.uniform(30,120)
        )

        db.add(attempt)
        db.flush()

        correct_count = 0

        for q in selected_questions:

            selected_option = random.choice(["A","B","C","D"])
            is_correct = selected_option == q.correct_option

            if is_correct:
                correct_count += 1

            response = models.Response(
                quiz_attempt_id=attempt.id,
                question_id=q.id,
                selected_option=selected_option,
                is_correct=is_correct
            )

            db.add(response)

        attempt.score = correct_count

    db.commit()   # commit after each student
    
db.close()