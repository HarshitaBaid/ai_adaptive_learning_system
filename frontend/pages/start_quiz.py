import streamlit as st
from services.quiz_api import get_subjects, get_topics_by_subject, start_quiz

st.title("🎯 Start Quiz")

if "user" not in st.session_state or "student_id" not in st.session_state["user"]:
    st.warning("Please login first")
    st.stop()
    

# get subjects

if "subjects" not in st.session_state:
    with st.spinner('Loading subjects...'):
        st.session_state["subjects"] = get_subjects()

subjects = st.session_state["subjects"]

if not subjects:
    st.error("No subjects found")
    st.stop()

subject_names = [s["name"] for s in subjects]

selected_subject = st.selectbox("Select Subject", subject_names)

subject_id = next(s["id"] for s in subjects if s["name"] == selected_subject)

# get topics

if selected_subject:
    if "topics" not in st.session_state or st.session_state.get("subject_id") != subject_id:
        
        with st.spinner('Loading topics...'):
            topics = get_topics_by_subject(subject_id)
        
        st.session_state["topics"] = topics
        st.session_state["subject_id"] = subject_id

    topics = st.session_state["topics"]

    if not topics:
        st.warning("No topics for this subject")
        st.stop()

    topic_names = [t["name"] for t in topics]

    selected_topic = st.selectbox("Select Topic", topic_names)

    topic_id = next(t["id"] for t in topics if t["name"] == selected_topic)

# quiz selection

if st.button("Start Quiz"):
    res = start_quiz(st.session_state["user"]["student_id"], topic_id)

    if res:
        # print(res)
        st.session_state["attempt_id"] = res["id"]
        st.session_state["topic_id"] = topic_id
        st.session_state["time_taken"] = None

        st.switch_page("pages/quiz.py")
