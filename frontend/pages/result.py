import streamlit as st
from services.quiz_api import get_result, submit_feedback

st.title("📊 Result")

if "user" not in st.session_state or "student_id" not in st.session_state["user"]:
    st.warning("Please login first")
    st.stop()
    

# ------------------ SAFETY CHECK ------------------

if "attempt_id" not in st.session_state:
    st.warning("No quiz attempt found")
    st.stop()

result = get_result(st.session_state["attempt_id"])

if not result:
    st.error("Failed to fetch result")
    st.stop()

score = result["score"]
total = result["total"]
percentage = round(result["percentage"], 2)

# ------------------ SUMMARY ------------------

st.success(f"🎯 Score: {score} / {total}")
st.write(f"📈 Percentage: {percentage:.2f}%")
st.write(f"❌ Wrong Answers: {total - score}")

# ------------------ DETAILED RESULT ------------------

st.subheader("📋 Detailed Analysis")

for r in result["responses"]:
    q_id = r["question_id"]
    feedback_key = f"feedback_done_{q_id}"

    if r["is_correct"]:
        st.success(f"{r['question_text']} ✅ Correct")

    else:
        st.error(
            f"{r['question_text']} ❌\n"
            f"(Your: {r['selected_option']})"
        )

        # ------------------ CHECK IF ALREADY SUBMITTED ------------------

        if st.session_state.get(feedback_key):
            option_map = {
                "A": r["option_a"],
                "B": r["option_b"],
                "C": r["option_c"],
                "D": r["option_d"]
            }

            correct_letter = r["correct_option"]
            correct_text = option_map.get(correct_letter, "")

            st.success(f"Correct Answer: {correct_letter} → {correct_text} ✅")

        else:
            # ------------------ FEEDBACK UI ------------------

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
                key=f"feedback_{q_id}"
            )

            if st.button("Submit Answer", key=f"btn_{q_id}"):
                success = submit_feedback(
                    st.session_state["attempt_id"],
                    q_id,
                    corrected
                )

                if success:
                    # ✅ mark as submitted
                    st.session_state[feedback_key] = True
                    st.success(f"Correct Answer: {r['correct_option']} ✅")
                    st.rerun()  # refresh UI
                else:
                    st.error("Failed to submit feedback")

    st.divider()

# ------------------ RESET ------------------

if st.button("Take Another Quiz"):
    for key in ["attempt_id", "topic_id", "start_time"]:
        st.session_state.pop(key, None)

    # also clear feedback states
    for key in list(st.session_state.keys()):
        if key.startswith("feedback_done_"):
            del st.session_state[key]

    st.success("You can start a new quiz now 👉")