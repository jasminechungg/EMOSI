import streamlit as st
import pandas as pd

from aws_dynamodb import (
    get_patients,
    create_appointment,
    get_appointments_by_clinician,
    get_patient_by_id,
    create_session,
    update_appointment_status
)

from ui_components import apply_global_style, render_sidebar

st.set_page_config(page_title="Appointment Scheduling", page_icon="📅", layout="wide")

if not st.session_state.get("logged_in", False):
    st.switch_page("main.py")

if st.session_state.user.get("role") != "clinician":
    st.error("Access denied. This page is only available for clinicians.")
    st.stop()

apply_global_style()
render_sidebar("Appointment Scheduling")

user = st.session_state.user
clinician_id = user["user_id"]

st.title("📅 Appointment Scheduling")
st.write("Schedule patient appointments and start monitoring sessions from upcoming appointments.")

st.markdown("---")

patients = get_patients(clinician_id=clinician_id)

with st.container(border=True):
    st.subheader("➕ Schedule New Appointment")

    if not patients:
        st.warning("No patients found. Please add a patient first.")
    else:
        patient_options = {
            f"{p.get('full_name')}": p
            for p in patients
        }

        col1, col2 = st.columns(2)

        with col1:
            selected_patient_name = st.selectbox(
                "Select Patient",
                list(patient_options.keys())
            )
            appointment_date = st.date_input("Appointment Date")

        with col2:
            appointment_time = st.time_input("Appointment Time")
            appointment_reason = st.text_area("Reason for Appointment")

        selected_patient = patient_options[selected_patient_name]

        if st.button("Create Appointment"):
            if appointment_reason.strip() == "":
                st.error("Appointment reason is required.")
            else:
                appointment = create_appointment(
                    patient_id=selected_patient["patient_id"],
                    clinician_id=clinician_id,
                    appointment_date=appointment_date,
                    appointment_time=appointment_time,
                    appointment_reason=appointment_reason.strip()
                )

                st.success("Appointment scheduled successfully.")
                st.rerun()

st.markdown("---")

st.subheader("📋 Appointment List")

appointments = get_appointments_by_clinician(clinician_id)

if not appointments:
    st.info("No appointments found.")
else:
    appointments = sorted(
        appointments,
        key=lambda a: f"{a.get('appointment_date', '')} {a.get('appointment_time', '')}"
    )

    for appt in appointments:
        patient = get_patient_by_id(appt.get("patient_id"))
        patient_name = patient.get("full_name") if patient else "Unknown Patient"

        with st.container(border=True):
            col1, col2, col3 = st.columns([1.5, 1.2, 1])

            with col1:
                st.markdown(f"### {patient_name}")
                st.write(f"**Date:** {appt.get('appointment_date')}")
                st.write(f"**Time:** {appt.get('appointment_time')}")
                st.write(f"**Reason:** {appt.get('appointment_reason')}")

            with col2:
                st.write("**Status**")
                st.markdown(f"### {appt.get('appointment_status')}")

            with col3:
                if appt.get("appointment_status") == "Scheduled":
                    if st.button("Start Session", key=f"start_{appt.get('appointment_id')}"):
                        session = create_session(
                            clinician_id=clinician_id,
                            patient_id=appt.get("patient_id"),
                            participant_id=appt.get("patient_id"),
                            notes=f"Started from appointment: {appt.get('appointment_reason')}"
                        )

                        update_appointment_status(
                            appointment_id=appt.get("appointment_id"),
                            status="In Progress",
                            session_id=session["session_id"]
                        )

                        st.session_state["active_patient"] = patient
                        st.session_state["active_session"] = session

                        st.switch_page("pages/Dashboard_home.py")

                elif appt.get("appointment_status") == "In Progress":
                    st.info("Session in progress")

                elif appt.get("appointment_status") == "Completed":
                    st.success("Completed")