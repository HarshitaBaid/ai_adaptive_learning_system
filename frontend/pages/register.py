import streamlit as st
import re
from services.auth_api import register_user

st.title("Register")

name = st.text_input("Name")
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Register"):
    if not name.strip():
        st.warning("Name cannot be empty")

    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        st.warning("Please enter a valid email")

    elif len(password.strip()) < 6:
        st.warning("Password must be at least 6 characters")

    else:
        res = register_user({
            "name": name,
            "email": email,
            "password": password
        })

        if res is None:
            st.error("Unable to connect to server. Please try again later.")
        elif res.status_code == 200:
            st.success("Account created")
            st.switch_page("pages/login.py")
        else:
            st.error("Registration failed")