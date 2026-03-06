from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    quiz_attempts = relationship("QuizAttempt", back_populates="student", cascade="all, delete")
    

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    topics = relationship("Topic", back_populates="subject")


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"))

    subject = relationship("Subject", back_populates="topics")
    questions = relationship("Question", back_populates="topic", cascade="all, delete")
    quiz_attempts = relationship("QuizAttempt", back_populates="topic", cascade="all, delete")
    

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)

    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"))

    question_text = Column(Text, nullable=False)

    option_a = Column(Text)
    option_b = Column(Text)
    option_c = Column(Text)
    option_d = Column(Text)

    correct_option = Column(String(1))
    difficulty_level = Column(String(20))

    topic = relationship("Topic", back_populates="questions")
    
    
class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"))
    topic_id = Column(Integer, ForeignKey("topics.id"))

    score = Column(Integer)
    total_questions = Column(Integer)
    time_taken = Column(Float)
    attempt_date = Column(DateTime)

    student = relationship("Student", back_populates="quiz_attempts")
    topic = relationship("Topic", back_populates="quiz_attempts")