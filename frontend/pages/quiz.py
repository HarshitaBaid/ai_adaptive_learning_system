import streamlit as st
import time
from services.quiz_api import get_questions, submit_quiz

st.title("🧠 Quiz")

# Safety check
if "topic_id" not in st.session_state:
    st.warning("Please start quiz first")
    st.stop()

# Start timer
if "start_time" not in st.session_state or st.session_state["start_time"] is None:
    st.session_state["start_time"] = time.time()

# Get questions
questions = get_questions(st.session_state["topic_id"])

if not questions:
    st.error("No questions found")
    st.stop()

answers = {}

# Show questions
for q in questions:
    st.write(f"**{q['question_text']}**")

    options = {
        "A": q["option_a"],
        "B": q["option_b"],
        "C": q["option_c"],
        "D": q["option_d"]
    }

    selected = st.radio(
        "Select answer",
        list(options.values()),
        key=q["id"]
    )

    # reverse mapping
    for key, value in options.items():
        if value == selected:
            answers[q["id"]] = key
# print(answers)

# Submit
if st.button("Submit Quiz"):
    time_taken = int(time.time() - st.session_state["start_time"])

    success = submit_quiz(
        st.session_state["attempt_id"],
        answers,
        time_taken
    )

    if success:
        st.success("Quiz Submitted! Go to Result Page 👉")
    else:
        st.error("Submission failed")