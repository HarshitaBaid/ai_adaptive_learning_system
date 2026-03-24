import streamlit as st
import requests

# 🔐 protect page
if "user" not in st.session_state:
    st.warning("Please login first")
    st.switch_page("pages/login.py")

user = st.session_state["user"]

st.title("📊 Dashboard")

st.write(f"Welcome {user['name']} 👋")

# API call
res = requests.get(f"http://localhost:8000/ai/progress/{user['student_id']}")
data = res.json()
# print(data)

# Metrics
col1, col2 = st.columns(2)

with col1:
    st.metric("Accuracy", f"{data['accuracy']}%")

with col2:
    st.metric("Score", f"{data['correct_answers']}/{data['total_attempts']}")

# Weak topics
st.subheader("📉 Weak Topics")

for topic in data["weak_topics"]:
    st.write(f"• {topic}")

# Navigation buttons
if st.button("Start Quiz"):
    st.switch_page("pages/start_quiz.py")

if st.button("View Recommendations"):
    st.write("Coming next...")