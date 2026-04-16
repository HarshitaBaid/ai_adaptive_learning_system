import streamlit as st
import threading
import requests
from config.settings import BASE_URL

def wake_backend():
    try:
        requests.get(f"BASE_URL", timeout=5)
    except:
        pass

threading.Thread(target=wake_backend, daemon=True).start()

st.set_page_config(
    page_title="AI EdTech Platform",
    layout="wide"
)

st.title("🎓 AI-Powered EdTech Platform")

st.write("""
Welcome to our AI-based learning platform.

Features:
- Adaptive Quiz System
- Performance Tracking
- AI-based Recommendations
""")

st.info("Use the sidebar to navigate to Login or Register")