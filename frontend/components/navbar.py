import streamlit as st
from utils.session import logout

def show_navbar():
    col1, col2 = st.columns([8, 2])

    with col1:
        st.title("🎓 AI EdTech Platform")

    with col2:
        if st.button("Logout"):
            logout()
            st.rerun()