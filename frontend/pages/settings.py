import streamlit as st
from services.settings_api import update_name, change_password

st.set_page_config(page_title="Settings", layout="centered")


if "settings_css_loaded" not in st.session_state:
    st.session_state["settings_css_loaded"] = True

    st.markdown("""
    <style>

    /* Button Styling */
    div.stButton > button {
        background-color: #4F46E5;
        color: white;
        border-radius: 8px;
        width: 100%;
    }

    /* Card Styling */
    [data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
        background-color: #111827;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #374151;
    }

    </style>
    """, unsafe_allow_html=True)

st.title("⚙️ Settings")

# Check login
if "user" not in st.session_state:
    st.warning("Please login first")
    st.stop()

student_id = st.session_state["user"]["student_id"]

tab1, tab2 = st.tabs(["👤 Profile", "🔒 Change Password"])


# ------------------ PROFILE ------------------
with tab1:
    st.subheader("👤 Profile")

    user = st.session_state["user"]

    # ------------------ DISPLAY INFO ------------------
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1f2937, #111827);
        padding: 15px;
        border-radius: 12px;
        color: white;
        margin-bottom: 20px;
    ">
        <b>Name:</b> {user.get("name", "N/A")} <br>
        <b>Email:</b> {user.get("email", "N/A")}
    </div>
    """, unsafe_allow_html=True)

    # ------------------ UPDATE NAME ------------------
    st.markdown("### ✏️ Update Name")

    new_name = st.text_input("New Name", value=user.get("name", ""))

    if st.button("Update Name"):
        if not new_name.strip():
            st.error("Name cannot be empty")
        else:
            res = update_name(user["student_id"], new_name)

            if "message" in res:
                st.success(res["message"])

                # update session immediately
                st.session_state["user"]["name"] = new_name

                st.rerun()
            else:
                st.error(res.get("error", "Something went wrong"))

    st.markdown("<hr>", unsafe_allow_html=True)

    # ------------------ LOGOUT ------------------
    st.markdown("### 🚪 Logout")

    if st.button("Logout"):
        st.session_state.clear()
        st.success("Logged out successfully")

        st.switch_page("app.py")

# ------------------ PASSWORD ------------------
with tab2:
    st.subheader("Change Password")

    old = st.text_input("Old Password", type="password")
    new = st.text_input("New Password", type="password")

    if st.button("Change Password"):
        if not old or not new:
            st.error("All fields required")

        elif len(new) < 6:
            st.error("Password must be at least 6 characters")

        else:
            res = change_password(student_id, old, new)

            if "message" in res:
                st.success(res["message"])
            else:
                st.error(res.get("detail", "Error changing password"))
