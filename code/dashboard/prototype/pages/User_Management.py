import streamlit as st
import pandas as pd

from aws_dynamodb import (
    get_all_users,
    get_patients,
    get_all_sessions,
    update_user_status
)

from ui_components import apply_global_style, render_sidebar

st.set_page_config(page_title="User Management", page_icon="⚙️", layout="wide")

if not st.session_state.get("logged_in", False):
    st.switch_page("main.py")

apply_global_style()
render_sidebar("User Management")

user = st.session_state.user

if user.get("role") != "admin":
    st.error("Access denied. This page is only available for admin users.")
    st.stop()

st.title("⚙️ User Management")
st.write("Manage platform users, clinician accounts, and system overview.")

users = get_all_users()
patients = get_patients()
sessions = get_all_sessions()

total_users = len(users)
total_clinicians = len([u for u in users if u.get("role") == "clinician"])
total_admins = len([u for u in users if u.get("role") == "admin"])
active_users = len([u for u in users if u.get("account_status") == "active"])
terminated_users = len([u for u in users if u.get("account_status") == "terminated"])

st.markdown("---")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Users", total_users)

with col2:
    st.metric("Clinicians", total_clinicians)

with col3:
    st.metric("Admins", total_admins)

with col4:
    st.metric("Active Users", active_users)

with col5:
    st.metric("Terminated", terminated_users)

st.markdown("---")

st.subheader("👥 Registered Users")

if users:
    user_rows = []

    for u in users:
        user_rows.append({
            "User ID": u.get("user_id"),
            "Full Name": u.get("full_name"),
            "Email": u.get("email"),
            "Role": u.get("role"),
            "Status": u.get("account_status"),
            "Created At": u.get("created_at")
        })

    user_df = pd.DataFrame(user_rows)
    st.dataframe(user_df, use_container_width=True)

else:
    st.info("No users found.")

st.markdown("---")

st.subheader("🔐 Account Control")

clinician_users = [
    u for u in users
    if u.get("role") == "clinician"
]

if not clinician_users:
    st.info("No clinician accounts available.")
else:
    clinician_options = {
        f"{u.get('full_name')} - {u.get('email')} ({u.get('account_status')})": u
        for u in clinician_users
    }

    selected_label = st.selectbox(
        "Select Clinician Account",
        list(clinician_options.keys())
    )

    selected_user = clinician_options[selected_label]

    st.write(f"**Name:** {selected_user.get('full_name')}")
    st.write(f"**Email:** {selected_user.get('email')}")
    st.write(f"**Current Status:** {selected_user.get('account_status')}")

    col_a, col_b = st.columns(2)

    with col_a:
        if st.button("Terminate Account"):
            update_user_status(
                selected_user["user_id"],
                "terminated"
            )
            st.success("Clinician account terminated successfully.")
            st.rerun()

    with col_b:
        if st.button("Reactivate Account"):
            update_user_status(
                selected_user["user_id"],
                "active"
            )
            st.success("Clinician account reactivated successfully.")
            st.rerun()

st.markdown("---")

st.subheader("📊 System Overview")

col6, col7 = st.columns(2)

with col6:
    st.metric("Total Patients", len(patients))

with col7:
    st.metric("Total Sessions", len(sessions))

st.markdown(
    "<div style='text-align:center;color:#64748b;margin-top:40px;'>Figure B.6: Admin User Management Interface</div>",
    unsafe_allow_html=True
)