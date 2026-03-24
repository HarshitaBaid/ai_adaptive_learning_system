import streamlit as st
from services.quiz_api import get_result, submit_feedback

st.title("📊 Result")

# Safety check
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

    if r["is_correct"]:
        st.success(f"Q{q_id} ✅ Correct")
    else:
        st.error(
            f"Q{q_id} ❌ Wrong "
            f"(Your: {r['selected_option']} | Correct: {r['correct_option']})"
        )

        # ------------------ FEEDBACK UI ------------------

        st.write("👉 Select correct answer:")

        corrected = st.radio(
            f"Correct answer for Q{q_id}",
            ["A", "B", "C", "D"],
            key=f"feedback_{q_id}"
        )

        if st.button(f"Submit Feedback Q{q_id}", key=f"btn_{q_id}"):
            success = submit_feedback(
                st.session_state["attempt_id"],
                q_id,
                corrected
            )

            if success:
                st.success("Feedback submitted ✅")
            else:
                st.error("Failed to submit feedback")

    st.divider()

# ------------------ RESET ------------------

if st.button("Take Another Quiz"):
    for key in ["attempt_id", "topic_id", "start_time"]:
        st.session_state.pop(key, None)

    st.success("You can start a new quiz now 👉")       