import streamlit as st
from services.quiz_api import get_subjects, get_topics_by_subject, start_quiz

st.title("🎯 Start Quiz")

# ------------------ SUBJECT ------------------

subjects = get_subjects()

if not subjects:
    st.error("No subjects found")
    st.stop()

subject_names = [s["name"] for s in subjects]

selected_subject = st.selectbox("Select Subject", subject_names)

subject_id = next(s["id"] for s in subjects if s["name"] == selected_subject)

# ------------------ TOPICS ------------------

topics = get_topics_by_subject(subject_id)

if not topics:
    st.warning("No topics for this subject")
    st.stop()

topic_names = [t["name"] for t in topics]

selected_topic = st.selectbox("Select Topic", topic_names)

topic_id = next(t["id"] for t in topics if t["name"] == selected_topic)

# ------------------ START QUIZ ------------------

if st.button("Start Quiz"):
    res = start_quiz(st.session_state["user"]["student_id"], topic_id)

    if res:
        # print(res)
        st.session_state["attempt_id"] = res["id"]
        st.session_state["topic_id"] = topic_id
        st.session_state["time_taken"] = None

        st.success("Quiz Started! Go to Quiz Page 👉")