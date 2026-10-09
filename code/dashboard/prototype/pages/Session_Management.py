import streamlit as st
from datetime import datetime

from aws_dynamodb import (
    get_patients,
    create_session,
    get_active_session,
    get_patient_by_id,
    get_sessions_by_patient,
    get_appointments_by_clinician,
)

from ui_components import apply_global_style, render_sidebar

st.set_page_config(page_title="Session Management", page_icon="🩺", layout="wide")

if not st.session_state.get("logged_in", False):
    st.switch_page("main.py")

if st.session_state.user.get("role") != "clinician":
    st.error("Access denied. This page is only available for clinicians.")
    st.stop()

apply_global_style()
render_sidebar("Session Management")

user = st.session_state.user
clinician_id = user["user_id"]


def format_datetime(value):
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S").strftime("%d %b %Y, %H:%M")
    except:
        return value or "N/A"


def get_patient_session_summary(patient_id):
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

        last_session_date = format_datetime(latest_session.get("end_time", ""))
        last_emotion = latest_session.get("dominant_emotion", "N/A").upper()
    else:
        last_session_date = "No completed session"
        last_emotion = "N/A"

    return {
        "total_sessions": total_sessions,
        "last_session_date": last_session_date,
        "last_emotion": last_emotion
    }


def get_upcoming_appointment_for_patient(patient_id):
    appointments = get_appointments_by_clinician(clinician_id)

    patient_appointments = [
        a for a in appointments
        if a.get("patient_id") == patient_id
        and a.get("appointment_status") in ["Scheduled", "In Progress"]
    ]

    if not patient_appointments:
        return None

    patient_appointments = sorted(
        patient_appointments,
        key=lambda a: f"{a.get('appointment_date', '')} {a.get('appointment_time', '')}"
    )

    return patient_appointments[0]


st.title("🩺 Session Management")
st.write("Review patient context and start a live monitoring session.")

st.markdown("---")

active_session = get_active_session()

if active_session:
    patient = get_patient_by_id(active_session.get("patient_id"))
    summary = get_patient_session_summary(active_session.get("patient_id"))
    appointment = get_upcoming_appointment_for_patient(active_session.get("patient_id"))

    st.success("🟢 A monitoring session is currently active.")

    with st.container(border=True):
        st.subheader("Active Session Details")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### Patient")
            st.write(f"**Name:** {patient.get('full_name') if patient else 'Unknown'}")
            if patient:
                st.write(f"**Age:** {patient.get('age')}")
                st.write(f"**Gender:** {patient.get('gender')}")
                st.write(f"**Guardian:** {patient.get('guardian_name')}")

        with col2:
            st.markdown("### Session Context")
            st.write("**Status:** Active Monitoring")
            st.write(f"**Start Time:** {format_datetime(active_session.get('start_time'))}")
            st.write(f"**Device ID:** {active_session.get('device_id')}")

        with col3:
            st.markdown("### Patient History")
            st.metric("Completed Sessions", summary["total_sessions"])
            st.write(f"**Last Session:** {summary['last_session_date']}")
            st.write(f"**Last Emotion:** {summary['last_emotion']}")

        if appointment:
            st.info(
                f"📅 Related Appointment: {appointment.get('appointment_date')} "
                f"at {appointment.get('appointment_time')} | "
                f"Reason: {appointment.get('appointment_reason')}"
            )

    st.info("Open the Main Dashboard to view live readings, emotion prediction, observation notes, and end the session.")

    if st.button("Open Main Dashboard"):
        st.switch_page("pages/Dashboard_home.py")

else:
    patients = get_patients(clinician_id=clinician_id)

    if not patients:
        st.warning("No patients found. Please add a patient first in Patient Management.")
    else:
        patient_options = {
            f"{p.get('full_name')} - Age {p.get('age')}": p
            for p in patients
        }

        with st.container(border=True):
            st.subheader("Start New Monitoring Session")

            selected_patient_label = st.selectbox(
                "Select Patient",
                list(patient_options.keys())
            )

            selected_patient = patient_options[selected_patient_label]
            selected_patient_id = selected_patient.get("patient_id")

            session_summary = get_patient_session_summary(selected_patient_id)
            appointment = get_upcoming_appointment_for_patient(selected_patient_id)

            st.markdown("### Patient Context Before Session")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("#### Patient Details")
                st.write(f"**Name:** {selected_patient.get('full_name')}")
                st.write(f"**Age:** {selected_patient.get('age')}")
                st.write(f"**Gender:** {selected_patient.get('gender')}")
                st.write(f"**Guardian:** {selected_patient.get('guardian_name')}")

            with col2:
                st.markdown("#### Previous Sessions")
                st.metric("Completed Sessions", session_summary["total_sessions"])
                st.write(f"**Last Session:** {session_summary['last_session_date']}")
                st.write(f"**Last Emotion:** {session_summary['last_emotion']}")

            with col3:
                st.markdown("#### Current Status")
                st.success("Ready for New Session")
                if appointment:
                    st.write(f"**Appointment Date:** {appointment.get('appointment_date')}")
                    st.write(f"**Appointment Time:** {appointment.get('appointment_time')}")
                else:
                    st.write("**Appointment:** No upcoming appointment linked")

            if appointment:
                st.info(f"📅 Appointment Reason: {appointment.get('appointment_reason')}")

            if selected_patient.get("notes"):
                st.warning(f"Patient Notes: {selected_patient.get('notes')}")

            session_notes = st.text_area("Initial Session Notes (Optional)")

            if st.button("Start Monitoring Session"):
                session = create_session(
                    clinician_id=clinician_id,
                    patient_id=selected_patient_id,
                    participant_id=selected_patient_id,
                    notes=session_notes
                )

                st.session_state["active_patient"] = selected_patient
                st.session_state["active_session"] = session

                st.success("Session started successfully.")
                st.switch_page("pages/Dashboard_home.py")

st.markdown("---")
st.caption("Figure B.4: Patient Session Management and Pre-Assessment Context Interface")