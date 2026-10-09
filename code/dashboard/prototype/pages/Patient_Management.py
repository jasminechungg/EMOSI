import streamlit as st
import pandas as pd

from aws_dynamodb import (
    create_patient,
    get_patients,
    get_sessions_by_patient,
    get_active_session
)

from ui_components import apply_global_style, render_sidebar

st.set_page_config(page_title="Patient Management", page_icon="👥", layout="wide")

if not st.session_state.get("logged_in", False):
    st.switch_page("main.py")

if st.session_state.user.get("role") != "clinician":
    st.error("Access denied. This page is only available for clinicians.")
    st.stop()

apply_global_style()
render_sidebar("Patient Management")

user = st.session_state.user
clinician_id = user["user_id"]

st.title("👥 Patient Management")
st.write("Register and manage patients assigned to the logged-in clinician.")

if st.session_state.get("patient_created"):
    st.success("✅ Patient added successfully and saved to the patient list.")
    st.session_state["patient_created"] = False

st.markdown("---")

with st.form("add_patient_form", clear_on_submit=True):
    st.subheader("➕ Add New Patient")

    col1, col2 = st.columns(2)

    with col1:
        full_name = st.text_input("Patient Full Name")
        age = st.text_input("Age")
        gender = st.selectbox("Gender", ["", "Male", "Female", "Other"])

    with col2:
        guardian_name = st.text_input("Guardian Name")
        notes = st.text_area("Patient Notes (Optional)")

    submitted = st.form_submit_button("Create Patient")

    if submitted:
        if full_name.strip() == "":
            st.error("Patient full name is required.")
        elif age.strip() == "":
            st.error("Age is required.")
        elif not age.strip().isdigit():
            st.error("Age must be a number.")
        elif gender.strip() == "":
            st.error("Gender is required.")
        elif guardian_name.strip() == "":
            st.error("Guardian name is required.")
        else:
            create_patient(
                full_name=full_name.strip(),
                age=age.strip(),
                gender=gender,
                guardian_name=guardian_name.strip(),
                clinician_id=clinician_id,
                notes=notes.strip()
            )

            st.session_state["patient_created"] = True
            st.rerun()

st.markdown("---")

st.subheader("📋 Patient List with Session Overview")

patients = get_patients(clinician_id=clinician_id)
active_session = get_active_session()

if patients:
    rows = []

    for patient in patients:
        patient_id = patient.get("patient_id")
        sessions = get_sessions_by_patient(patient_id)

        completed_sessions = [
            s for s in sessions
            if s.get("session_status") == "completed"
        ]

        total_sessions = len(completed_sessions)

        if completed_sessions:
            latest_session = sorted(
                completed_sessions,
                key=lambda s: s.get("end_time", ""),
                reverse=True
            )[0]

            last_session_date = latest_session.get("end_time", "N/A")
            last_emotion = latest_session.get("dominant_emotion", "N/A").upper()
        else:
            last_session_date = "No completed session"
            last_emotion = "N/A"

        if active_session and active_session.get("patient_id") == patient_id:
            current_status = "Active Monitoring"
        else:
            current_status = "No Active Session"

        rows.append({
            "Patient Name": patient.get("full_name"),
            "Age": patient.get("age"),
            "Gender": patient.get("gender"),
            "Guardian": patient.get("guardian_name"),
            "Total Sessions": total_sessions,
            "Last Session Date": last_session_date,
            "Last Emotion": last_emotion,
            "Current Status": current_status,
            "Notes": patient.get("notes", "")
        })

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)

    st.markdown("---")
    st.subheader("🧾 Patient Summary Cards")

    for row in rows:
        with st.container(border=True):
            col1, col2, col3, col4 = st.columns([1.5, 1, 1, 1.2])

            with col1:
                st.markdown(f"### {row['Patient Name']}")
                st.write(f"**Age:** {row['Age']}")
                st.write(f"**Gender:** {row['Gender']}")
                st.write(f"**Guardian:** {row['Guardian']}")

            with col2:
                st.metric("Total Sessions", row["Total Sessions"])

            with col3:
                st.write("**Last Emotion**")
                st.markdown(f"### {row['Last Emotion']}")

            with col4:
                st.write("**Current Status**")
                if row["Current Status"] == "Active Monitoring":
                    st.success("🟢 Active Monitoring")
                else:
                    st.info("⚪ No Active Session")

            st.write(f"**Last Session Date:** {row['Last Session Date']}")

            if row["Notes"]:
                st.caption(f"Notes: {row['Notes']}")

else:
    st.info("No patients found. Add a patient to begin session management.")

st.markdown(
    "<div style='text-align:center;color:#64748b;margin-top:40px;'>Figure B.2: Patient Management and Session Overview Interface</div>",
    unsafe_allow_html=True
)