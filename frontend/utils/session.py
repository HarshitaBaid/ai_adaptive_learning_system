import streamlit as st

def set_user(user):
    st.session_state["user"] = user

def get_user():
    return st.session_state.get("user", None)

def logout():
    st.session_state.pop("user", None)