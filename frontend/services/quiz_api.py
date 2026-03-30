import requests
import streamlit as st

BASE_URL = "http://127.0.0.1:8000"

# ------------------ SUBJECTS ------------------

def get_subjects():
    res = requests.get(f"{BASE_URL}/subjects/")
    return res.json() if res.status_code == 200 else []


# ------------------ TOPICS ------------------
@st.cache_data
def get_topics_by_subject(subject_id):
    res = requests.get(f"{BASE_URL}/subjects/{subject_id}/topics")
    return res.json() if res.status_code == 200 else []


# ------------------ QUIZ ------------------

def start_quiz(student_id, topic_id):
    payload = {
        "student_id": student_id,
        "topic_id": topic_id
    }

    res = requests.post(f"{BASE_URL}/quiz/start", json=payload)
    return res.json() if res.status_code == 200 else None


def get_questions(topic_id):
    res = requests.get(f"{BASE_URL}/quiz/{topic_id}")
    return res.json() if res.status_code == 200 else []


def submit_quiz(attempt_id, answers, time_taken):
    payload = {
        "attempt_id": attempt_id,
        "answers": answers,
        "time_taken": time_taken
    }

    res = requests.post(f"{BASE_URL}/quiz/submit", json=payload)
    return res.status_code == 200


def get_result(attempt_id):
    res = requests.get(f"{BASE_URL}/quiz/result/{attempt_id}")
    return res.json() if res.status_code == 200 else None


def submit_feedback(attempt_id, question_id, corrected_answer):
    payload = {
        "attempt_id": attempt_id,
        "question_id": question_id,
        "corrected_answer": corrected_answer
    }

    res = requests.post(f"{BASE_URL}/feedback", json=payload)
    return res.status_code == 200


def get_progress(student_id):
    res = requests.get(f"{BASE_URL}/ai/progress/{student_id}")
    return res.json() if res.status_code == 200 else None


def get_recommendations(student_id):
    res = requests.get(f"{BASE_URL}/ai/recommend/{student_id}")
    return res.json() if res.status_code == 200 else []


def submit_practice(student_id, answers, time_taken):
    payload = {
        "student_id": student_id,
        "answers": answers,
        "time_taken": time_taken
    }

    res = requests.post(f"{BASE_URL}/ai/submit-practice", json=payload)
    return res.json() if res.status_code == 200 else None