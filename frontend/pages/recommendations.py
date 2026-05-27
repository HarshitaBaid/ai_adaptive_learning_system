import streamlit as st
import time
from services.quiz_api import get_recommendations, submit_practice

st.set_page_config(page_title="Recommendations", layout="wide")

#  HEADER
st.markdown(
    """
    <h1 style='text-align: center;'>🎯 Personalized Practice</h1>
    <p style='text-align: center; color: gray;'>
        Practice questions based on your weak topics
    </p>
    <hr>
    """,
    unsafe_allow_html=True
)

# login check
if "user" not in st.session_state or "student_id" not in st.session_state["user"]:
    st.warning("Please login first")
    st.stop()

student_id = st.session_state["user"]["student_id"]

# cache

@st.cache_data(show_spinner=False)
def get_recommendations_cached(student_id):
    return get_recommendations(student_id)

# loading of questions

if "rec_questions" not in st.session_state:
    with st.spinner("Fetching recommendations..."):
        st.session_state["rec_questions"] = get_recommendations_cached(student_id)

questions = st.session_state["rec_questions"]

if not questions:
    st.info("No recommendations yet. Take more quizzes!")
    st.stop()

# timer

if "start_time" not in st.session_state or st.session_state["start_time"] is None:
    st.session_state["start_time"] = time.time()

# store answersw

if "rec_answers" not in st.session_state:
    st.session_state["rec_answers"] = {}


st.subheader("📚 Recommended Questions")
st.info("⏱️ Time will be recorded automatically")

for i, q in enumerate(questions, start=1):

    with st.container():
        st.markdown(
            f"""
            <div style="
                padding:15px;
                border-radius:10px;
                border:1px solid #ddd;
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

        selected = st.radio(
            "Choose your answer:",
            list(options.keys()),
            format_func=lambda x: f"{x} → {options[x]}",
            key=f"rec_{q['id']}",
            index=None   #prevents auto selection
        )

        # store only if selected
        if selected:
            st.session_state["rec_answers"][q["id"]] = selected

        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("---")

# submit

if st.button("🚀 Submit Practice", use_container_width=True):

    if len(st.session_state["rec_answers"]) < len(questions):
        st.warning("Please answer all questions")
        st.stop()

    if "start_time" not in st.session_state or st.session_state["start_time"] is None:
        st.error("Session expired. Please restart.")
        st.stop()

    time_taken = int(time.time() - st.session_state["start_time"])

    with st.spinner("Submitting your answers..."):
        result = submit_practice(
            student_id,
            st.session_state["rec_answers"],
            time_taken
        )

    if result:
        st.success(f"🎯 Score: {result['score']} / {result['total']}")
        st.write(f"📈 {result['percentage']:.2f}%")
        st.write(f"⏱️ Time Taken: {time_taken} seconds")

        # ------------------ RESET ------------------
        st.session_state.pop("start_time", None)
        st.session_state.pop("rec_questions", None)
        st.session_state.pop("rec_answers", None)
        st.cache_data.clear()

        st.balloons()
    else:
        st.error("Failed to submit")
