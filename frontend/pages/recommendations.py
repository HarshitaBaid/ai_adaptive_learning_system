import streamlit as st
import time
from services.quiz_api import get_recommendations, submit_practice

st.set_page_config(page_title="Recommendations", layout="wide")

# ------------------ HEADER ------------------

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

# ------------------ CHECK LOGIN ------------------

if "user" not in st.session_state or "student_id" not in st.session_state["user"]:
    st.warning("Please login first")
    st.stop()

student_id = st.session_state["user"]["student_id"]

# ------------------ FETCH QUESTIONS ------------------

questions = get_recommendations(student_id)

if not questions:
    st.info("No recommendations yet. Take more quizzes!")
    st.stop()


# ------------------ START TIMER ------------------

if "start_time" not in st.session_state:
    st.session_state["start_time"] = time.time()
    

# ------------------ QUESTIONS UI ------------------

st.subheader("📚 Recommended Questions")
st.info("⏱️ Time will be recorded automatically")

answers = {}

for i, q in enumerate(questions, start=1):

    with st.container():
        st.markdown(
            f"""
            <div style="padding:15px; border-radius:10px; border:1px solid #ddd;">
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
            key=f"rec_{q['id']}"
        )

        answers[q["id"]] = selected

        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("---")

# ------------------ SUBMIT ------------------

if st.button("🚀 Submit Practice", use_container_width=True):

    # ⏱️ Calculate time taken
    time_taken = int(time.time() - st.session_state["start_time"])

    result = submit_practice(
        student_id,
        answers,
        time_taken   # ✅ NEW
    )

    if result:
        st.success(f"🎯 Score: {result['score']} / {result['total']}")
        st.write(f"📈 {result['percentage']:.2f}%")
        st.write(f"⏱️ Time Taken: {time_taken} seconds")

        # Reset timer for next attempt
        st.session_state.pop("start_time", None)

        st.balloons()
    else:
        st.error("Failed to submit")