import streamlit as st
import matplotlib.pyplot as plt
from services.quiz_api import get_progress
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard", layout="wide")

# Custom CSS 
if "css_loaded" not in st.session_state:
    st.session_state["css_loaded"] = True
    st.markdown("""
    <style>

    /* Background */
    .stApp {
        background: linear-gradient(135deg, #0E1117, #111827);
    }

    /* Glass Card */
    .card {
        background: linear-gradient(145deg, #ffffff, #ffffff);
        padding: 1px;
        border-radius: 1px;
        box-shadow: 0px 6px 20px rgba(0,0,0,0.5);
        margin-bottom: 20px;
        margin-top: 10px;
    }

    /* KPI Card */
    .kpi-card {
        background: linear-gradient(135deg, #6a11cb, #2575fc);
        padding: 20px;
        border-radius: 18px;
        color: white;
    }

    /* Titles */
    .card-title {
        font-size: 14px;
        opacity: 0.8;
    }

    .card-value {
        font-size: 30px;
        font-weight: bold;
    }

    /* Section headers */
    .section-title {
        color: white;
        margin-bottom: 10px;
    }

    </style>
    """, unsafe_allow_html=True)


# HEADER 
st.markdown(
    "<h1 style='text-align:center; color:white;'>📊 Student Dashboard</h1>",
    unsafe_allow_html=True
)

# FETCH DATA 
if "user" not in st.session_state or "student_id" not in st.session_state["user"]:
    st.warning("Please login first")
    st.stop()

if "dashboard_data" not in st.session_state:
    with st.spinner("Loading dashboard..."):
        st.session_state["dashboard_data"] = get_progress(
            st.session_state["user"]["student_id"]
        )

data = st.session_state["dashboard_data"]

if not data:
    st.info("No activity yet. Start a quiz to see your dashboard insights!")
    st.stop()

# KPI CARDS 
st.markdown("<h3 class='section-title'>📈 Overview</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

def kpi(title, value, gradient):
    st.markdown(f"""
    <div style="
        background: {gradient};
        padding: 20px;
        border-radius: 18px;
        color: white;
        box-shadow: 0px 6px 20px rgba(0,0,0,0.5);
    ">
        <div style="font-size:14px; opacity:0.8;">{title}</div>
        <div style="font-size:30px; font-weight:bold;">{value}</div>
    </div>
    """, unsafe_allow_html=True)

with col1:
    kpi("🎯 Accuracy", f"{data['accuracy']}%", "linear-gradient(135deg, #00C9FF, #92FE9D)")

with col2:
    kpi("✅ Correct Answers", data["correct_answers"], "linear-gradient(135deg, #f7971e, #ffd200)")

with col3:
    kpi("📝 Total Questions Attempts", data["total_attempts"], "linear-gradient(135deg, #8E2DE2, #4A00E0)")

# charts   
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<h4 style='color:white;'>📊 Performance</h4>", unsafe_allow_html=True)

    correct = data.get("correct_answers", 0)
    total = data.get("total_attempts", 0)
    wrong = max(total - correct, 0)

    fig = go.Figure(data=[go.Pie(
        labels=["Correct", "Wrong"],
        values=[correct, wrong],
        hole=0.65,  
        marker=dict(
            colors=["#00C49F", "#FF4B4B"]
        ),
        textinfo="percent",
        textfont=dict(color="white", size=14),
        hovertemplate="<b>%{label}</b><br>Count: %{value}<extra></extra>"
    )])

    fig.update_layout(
        showlegend=True,
        legend=dict(
            font=dict(color="white", size=12),
            orientation="v",
            x=1,
            y=0.5
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=20, b=20, l=20, r=20),
        annotations=[
            dict(
                text=f"<b>{data['accuracy']}%</b><br><span style='font-size:12px'>Accuracy</span>",
                x=0.5,
                y=0.5,
                font=dict(size=18, color="white"),
                showarrow=False
            )
        ]
    )

    with st.container():
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)
    
    
# INSIGHTS 
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<h4 style='color:white;'>💡 Insights</h4>", unsafe_allow_html=True)

    if data["weak_topics"]:
        weakest = min(data["weak_topics"], key=lambda x: x["accuracy"])

        st.markdown(f"""
        <div style="
            background: linear-gradient(90deg, #3a2b00, #5a4500);
            padding: 12px;
            border-radius: 10px;
            color: #FFD700;
            margin-bottom: 10px;">
        🚀 Focus on <b>{weakest['topic']}</b>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <p style='color:#bbb; font-size:16px;'>
        Improving this topic can significantly boost your accuracy.
        Practice consistently to strengthen weak areas.
        </p>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="
            background: linear-gradient(90deg, #003b2f, #005f4a);
            padding: 12px;
            border-radius: 10px;
            color: #00FFB2;
            margin-bottom: 10px;">
        🎉 Excellent performance!
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='color:#ccc; font-size:14px; line-height:1.8'>
    📊 Questions Attempts: <b>{data['total_attempts']}</b><br>
    ✅ Correct: <b>{data['correct_answers']}</b><br>
    🎯 Accuracy: <b>{data['accuracy']}%</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# WEAK & STRONG
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<h4 style='color:white;'>⚠️ Weak Topics</h4>", unsafe_allow_html=True)

    if not data["weak_topics"]:
        st.success("No weak topics 🎉")
    else:
        for t in data["weak_topics"]:
            st.markdown(f"🔴 **{t['topic']}**")
            st.progress(1 - (t["accuracy"] / 100))
            st.caption(f"{t['accuracy']}% accuracy")

    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<h4 style='color:white;'>💪 Strong Topics</h4>", unsafe_allow_html=True)

    if not data["strong_topics"]:
        st.info("No strong topics yet")
    else:
        for t in data["strong_topics"]:
            st.markdown(f"🟢 **{t['topic']}**")
            st.progress(t["accuracy"] / 100)
            st.caption(f"{t['accuracy']}% accuracy")

    st.markdown('</div>', unsafe_allow_html=True)

# BUTTON
st.markdown("<br>", unsafe_allow_html=True)

if st.button("🚀 Practice Weak Topics"):
    st.switch_page("pages/recommendations.py")
    st.rerun()
