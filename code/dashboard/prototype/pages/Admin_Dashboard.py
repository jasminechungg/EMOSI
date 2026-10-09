import streamlit as st
import pandas as pd

from aws_dynamodb import (
    get_all_users,
    get_patients,
    get_all_sessions,
    get_appointments_by_clinician
)

from ui_components import apply_global_style, render_sidebar

st.set_page_config(page_title="Admin Dashboard", page_icon="⚙️", layout="wide")

if not st.session_state.get("logged_in", False):
    st.switch_page("main.py")

if st.session_state.user.get("role") != "admin":
    st.error("Access denied. This page is only available for admin users.")
    st.stop()

apply_global_style()
render_sidebar("Admin Dashboard")

st.title("⚙️ Admin Dashboard")
st.write("System overview for EmoSI platform administration.")

users = get_all_users()
patients = get_patients()
sessions = get_all_sessions()

total_users = len(users)
total_clinicians = len([u for u in users if u.get("role") == "clinician"])
total_admins = len([u for u in users if u.get("role") == "admin"])
total_patients = len(patients)
total_sessions = len(sessions)
active_users = len([u for u in users if u.get("account_status") == "active"])
terminated_users = len([u for u in users if u.get("account_status") == "terminated"])

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Users", total_users)

with col2:
    st.metric("Clinicians", total_clinicians)

with col3:
    st.metric("Patients", total_patients)

with col4:
    st.metric("Sessions", total_sessions)

col5, col6, col7 = st.columns(3)

with col5:
    st.metric("Admins", total_admins)

with col6:
    st.metric("Active Accounts", active_users)

with col7:
    st.metric("Terminated Accounts", terminated_users)

st.markdown("---")

st.subheader("🧾 Recent Registered Users")

if users:
    user_df = pd.DataFrame(users)
    show_cols = ["full_name", "email", "role", "account_status", "created_at"]
    existing_cols = [c for c in show_cols if c in user_df.columns]
    st.dataframe(user_df[existing_cols], use_container_width=True)
else:
    st.info("No users found.")

st.markdown("---")

st.subheader("👥 Registered Patients Overview")

if patients:
    patient_df = pd.DataFrame(patients)
    show_cols = ["full_name", "age", "gender", "guardian_name", "created_at"]
    existing_cols = [c for c in show_cols if c in patient_df.columns]
    st.dataframe(patient_df[existing_cols], use_container_width=True)
else:
    st.info("No patients found.")

st.markdown("---")

if st.button("Go to User Management"):
    st.switch_page("pages/User_Management.py")

st.markdown(
    "<div style='text-align:center;color:#64748b;margin-top:40px;'>Figure B.7: Admin Dashboard Interface</div>",
    unsafe_allow_html=True
)