-- AI Powered Personalized Learning System
-- Database Schema
-- Author: Harshita Baid
-- MCA Final Year Project
-- Description: Schema for adaptive learning platform

CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE subjects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    subject_id INT REFERENCES subjects(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    topic_id INT REFERENCES topics(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    option_a TEXT,
    option_b TEXT,
    option_c TEXT,
    option_d TEXT,
    correct_option VARCHAR(1),
    difficulty_level VARCHAR(20)
);

CREATE TABLE quiz_attempts (
    id SERIAL PRIMARY KEY,
    student_id INT REFERENCES students(id) ON DELETE CASCADE,
    topic_id INT REFERENCES topics(id),
    score INT,
    total_questions INT,
    time_taken FLOAT,
    attempt_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE responses (
    id SERIAL PRIMARY KEY,
    quiz_attempt_id INT REFERENCES quiz_attempts(id) ON DELETE CASCADE,
    question_id INT REFERENCES questions(id),
    selected_option VARCHAR(1),
    is_correct BOOLEAN
);