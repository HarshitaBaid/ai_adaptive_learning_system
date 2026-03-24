import streamlit as st
from services.auth_api import register_user

st.title("Register")

name = st.text_input("Name")
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Register"):
    res = register_user({
        "name": name,
        "email": email,
        "password": password
    })

    if res.status_code == 200:
        st.success("Account created")
        st.switch_page("pages/login.py")
    else:
        st.error("Registration failed")