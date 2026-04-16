import streamlit as st
from services.quiz_api import get_result_cached, submit_feedback

st.title("📊 Result")

# ------------------ AUTH ------------------
if "user" not in st.session_state or "student_id" not in st.session_state["user"]:
    st.warning("Please login first")
    st.stop()

# ------------------ SAFETY CHECK ------------------
if "attempt_id" not in st.session_state:
    st.warning("No quiz attempt found")
    st.stop()

# ------------------ FETCH RESULT ------------------
with st.spinner("Fetching results..."):
    result = get_result_cached(st.session_state["attempt_id"])

if not result:
    st.error("Failed to fetch result")
    st.stop()

score = result["score"]
total = result["total"]
percentage = round(result["percentage"], 2)

# ------------------ SUMMARY CONTAINER ------------------
with st.container():
    st.markdown(
        f"""
        <div style="
            padding-top:12px;
            padding-left:15px;
            border-radius:15px;
            background: #1a1a1a;
            border: 2px solid #00f2fe;
            box-shadow: 0 0 15px rgba(0, 242, 254, 0.4), inset 0 0 10px rgba(0, 242, 254, 0.1);
            text-shadow: 0 0 5px rgba(255, 255, 255, 0.2);
            color: #ffffff;
            margin-bottom:15px;
        ">
            <p><b>Score:</b> {score} / {total}</p>
            <p><b>Percentage:</b> {percentage:.2f}%</p>
            <p><b>Wrong Answers:</b> {total - score}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ------------------ TOGGLE DETAILED ANALYSIS ------------------
show_analysis = st.checkbox("Show Detailed Analysis")

# ------------------ DETAILED RESULT ------------------
if show_analysis:

    st.subheader("📋 Detailed Analysis")

    for r in result["responses"]:
        q_id = r["question_id"]
        feedback_key = f"feedback_done_{q_id}"

        option_map = {
            "A": r["option_a"],
            "B": r["option_b"],
            "C": r["option_c"],
            "D": r["option_d"]
        }

        if r["is_correct"]:
            st.success(f"{r['question_text']} ✅ Correct")

        else:
            st.error(
                f"{r['question_text']} ❌\n"
                f"(Your: {r['selected_option']})"
            )

            # ------------------ FEEDBACK ------------------

            if st.session_state.get(feedback_key):
                correct_letter = r["correct_option"]
                correct_text = option_map.get(correct_letter, "")

                st.success(f"Correct Answer: {correct_letter} → {correct_text} ✅")

            else:
                st.write("👉 Try to select the correct answer:")

                options = {
                    "A": r["option_a"],
                    "B": r["option_b"],
                    "C": r["option_c"],
                    "D": r["option_d"]
                }

                corrected = st.radio(
                    "Select correct answer",
                    list(options.keys()),
                    format_func=lambda x: f"{x} → {options[x]}",
                    key=f"feedback_{q_id}",
                    index=None   
                )

                if corrected and st.button("Submit Answer", key=f"btn_{q_id}"):
                    success = submit_feedback(
                        st.session_state["attempt_id"],
                        q_id,
                        corrected
                    )

                    if success:
                        st.cache_data.clear()
                        st.session_state[feedback_key] = True

                        correct_letter = r["correct_option"]
                        correct_text = option_map.get(correct_letter, "")

                        st.success(f"Correct Answer: {correct_letter} → {correct_text} ✅")
                        st.rerun()
                    else:
                        st.error("Failed to submit feedback")

        st.divider()

# ------------------ RESET ------------------
if st.button("Take Another Quiz"):
    for key in ["attempt_id", "topic_id", "start_time"]:
        st.session_state.pop(key, None)

    for key in list(st.session_state.keys()):
        if key.startswith("feedback_done_"):
            del st.session_state[key]

    st.switch_page("pages/start_quiz.py")