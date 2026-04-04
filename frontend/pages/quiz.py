import streamlit as st
import time
from services.quiz_api import get_questions, submit_quiz

st.title("🧠 Quiz")

# ------------------ AUTH ------------------
if "user" not in st.session_state or "student_id" not in st.session_state["user"]:
    st.warning("Please login first")
    st.stop()

if "topic_id" not in st.session_state:
    st.warning("Please start quiz first")
    st.stop()
    
# if "attempt_id" not in st.session_state:
#     st.warning("No active quiz. Please start again.")
#     st.stop()

# ------------------ TIMER ------------------
if "start_time" not in st.session_state:
    st.session_state["start_time"] = time.time()

# ------------------ LOAD QUESTIONS (OPTIMIZED) ------------------
if "questions" not in st.session_state:
    with st.spinner("Loading questions..."):
        st.session_state["questions"] = get_questions(st.session_state["topic_id"])

questions = st.session_state["questions"]

if not questions:
    st.error("No questions found")
    st.stop()

# ------------------ ANSWERS STORAGE ------------------
if "answers" not in st.session_state:
    st.session_state["answers"] = {}

# ------------------ UI ------------------
st.info("⏱️ Time will be recorded automatically...")
for i, q in enumerate(questions, 1):

    with st.container():
        st.markdown(
            f"""
            <div style="
                padding-left:15px;
                border-radius:12px;
                border:1px solid #e6e6e6;
                margin-bottom:10px;
            ">
            <h4>Q{i}. {q['question_text']}</h4>
            </div>
            """,
            unsafe_allow_html=True
        )

        options = {
            "A": q["option_a"],
            "B": q["option_b"],
            "C": q["option_c"],
            "D": q["option_d"]
        }

        option_values = list(options.values())

        selected = st.radio(
            "Select answer",
            option_values,
            key=f"q_{q['id']}",
            label_visibility="collapsed" 
        )

        # store answer
        for key, value in options.items():
            if value == selected:
                st.session_state["answers"][q["id"]] = key

# ------------------ SUBMIT ------------------
if st.button("Submit Quiz"):
    if len(st.session_state["answers"]) < len(questions):
        st.warning("Please answer all questions")
    
    time_taken = int(time.time() - st.session_state["start_time"])

    success = submit_quiz(
        st.session_state["attempt_id"],
        st.session_state["answers"],
        time_taken
    )

    if success:

        st.session_state.pop("questions", None)
        st.session_state.pop("answers", None)
        st.session_state.pop("topic_id", None)
        # st.session_state.pop("attempt_id", None)
        st.session_state["start_time"] = None
        
        st.switch_page("pages/result.py")

    else:
        st.error("Submission failed")