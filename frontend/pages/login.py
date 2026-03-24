import streamlit as st
from services.auth_api import login_user

st.title("Login")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):
    res = login_user({
        "email": email,
        "password": password
    })

    if res.status_code == 200:
        st.session_state["user"] = res.json()
        st.success("Login successful")
        st.switch_page("pages/dashboard.py")   # navigate
    else:
        st.error("Invalid credentials")