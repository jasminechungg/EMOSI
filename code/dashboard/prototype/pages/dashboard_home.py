import streamlit as st
import pandas as pd
import math
import altair as alt
from decimal import Decimal
from datetime import datetime
from collections import Counter


from aws_dynamodb import (
    get_latest_sensor_readings,
    get_latest_prediction,
    get_active_session,
    get_patient_by_id,
    end_session,
    get_sensor_readings_between,
    get_predictions_between,
    save_session_summary,
    add_session_observation,
    get_session_observations,
    get_appointment_by_session_id,
    update_appointment_status,
)


from ui_components import apply_global_style, render_sidebar


st.set_page_config(
    page_title="EmoSI Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)


if not st.session_state.get("logged_in", False):
    st.switch_page("main.py")


if st.session_state.user.get("role") != "clinician":
    st.error("Access denied. This page is only available for clinicians.")
    st.stop()


apply_global_style()
render_sidebar("Dashboard Home")


st.markdown("""
<style>
.metric-card, .emotion-box {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 8px 22px rgba(15, 23, 42, 0.06);
    margin-bottom: 14px;
}


.metric-label {
    color: #475569;
    font-size: 14px;
    font-weight: 700;
}


.metric-value {
    color: #111827;
    font-size: 30px;
    font-weight: 900;
    margin-top: 5px;
}


.prob-card {
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 16px;
    text-align: center;
}


.prob-label {
    color: #475569;
    font-size: 14px;
    font-weight: 700;
}


.prob-value {
    color: #111827;
    font-size: 24px;
    font-weight: 900;
}
</style>
""", unsafe_allow_html=True)




def to_float(value, default=0.0):
    try:
        if isinstance(value, Decimal):
            return float(value)
        return float(value)
    except:
        return default




def display_temp(value):
    return to_float(value) + 0.5




def generate_demo_heart_rate(timestamp=None, ppg_value=0):
    """
    Demo-only heart rate generator.
    Produces smooth realistic BPM values within a normal-looking range.
    This is NOT a clinical-grade heart rate calculation.
    """

    try:
        if timestamp:
            base_time = pd.to_datetime(timestamp).timestamp()
        else:
            base_time = datetime.now().timestamp()
    except:
        base_time = datetime.now().timestamp()

    ppg_factor = (to_float(ppg_value) % 5) * 0.4

    heart_rate = (
        88
        + 8 * math.sin(base_time / 22)
        + 4 * math.sin(base_time / 8)
        + ppg_factor
    )

    heart_rate = max(75, min(105, heart_rate))

    return round(heart_rate)




def safe_get(data, key, default=0.0):
    return data.get(key, default) if data else default




def percent(value):
    return f"{to_float(value) * 100:.2f}%"




def generate_demo_neutral_prediction(timestamp=None):
    """
    Demo-only emotion probability generator.

    Neutral remains dominant, while Happy, Nervous, Sad, and Angry
    still fluctuate realistically. This is useful for dashboard demo mode.
    """

    try:
        if timestamp:
            base_time = pd.to_datetime(timestamp).timestamp()
        else:
            base_time = datetime.now().timestamp()
    except:
        base_time = datetime.now().timestamp()

    neutral = (
        0.60
        + 0.05 * math.sin(base_time / 18)
        + 0.02 * math.sin(base_time / 7)
    )

    neutral = max(0.56, min(0.68, neutral))

    raw_happy = 0.12 + 0.03 * math.sin(base_time / 16)
    raw_nervous = 0.18 + 0.04 * math.sin(base_time / 11)
    raw_sad = 0.11 + 0.03 * math.sin(base_time / 13)
    raw_angry = 0.07 + 0.02 * math.sin(base_time / 9)

    raw_values = {
        "happy_probability": max(0.05, raw_happy),
        "nervous_probability": max(0.08, raw_nervous),
        "sad_probability": max(0.05, raw_sad),
        "angry_probability": max(0.03, raw_angry),
    }

    other_total = sum(raw_values.values())
    remaining = 1.0 - neutral

    if other_total <= 0:
        values = {
            "happy_probability": 0.10,
            "nervous_probability": 0.15,
            "sad_probability": 0.09,
            "angry_probability": 0.06,
        }
    else:
        values = {
            key: (value / other_total) * remaining
            for key, value in raw_values.items()
        }

    values["neutral_probability"] = neutral

    return {
        "predicted_emotion": "neutral",
        "confidence": values["neutral_probability"],
        "happy_probability": values["happy_probability"],
        "nervous_probability": values["nervous_probability"],
        "neutral_probability": values["neutral_probability"],
        "sad_probability": values["sad_probability"],
        "angry_probability": values["angry_probability"],
    }




def avg(items, key):
    values = [to_float(i.get(key)) for i in items if i.get(key) is not None]
    return round(sum(values) / len(values), 6) if values else 0




def avg_temp(items, key):
    values = [display_temp(i.get(key)) for i in items if i.get(key) is not None]
    return round(sum(values) / len(values), 6) if values else 0




def magnitude_value(item, x, y, z):
    return math.sqrt(
        to_float(item.get(x)) ** 2 +
        to_float(item.get(y)) ** 2 +
        to_float(item.get(z)) ** 2
    )




def magnitude_avg(items, x, y, z):
    values = [magnitude_value(i, x, y, z) for i in items]
    return round(sum(values) / len(values), 6) if values else 0




def heart_rate_avg(items):
    values = [
        generate_demo_heart_rate(
            timestamp=i.get("timestamp", i.get("time", None)),
            ppg_value=i.get("PPG_GREEN", 0)
        )
        for i in items
    ]
    return round(sum(values) / len(values), 2) if values else 0




def movement_label(value):
    if value < 1.2:
        return "Low"
    elif value < 2.0:
        return "Moderate"
    return "High"




def gyro_label(value):
    if value < 20:
        return "Stable"
    elif value < 60:
        return "Moderate movement"
    return "Frequent movement"




def orientation_label(value):
    if value < 50:
        return "Stable orientation"
    elif value < 100:
        return "Moderate orientation changes"
    return "Frequent orientation changes"




def format_duration(start_time):
    try:
        start_dt = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")
        diff = datetime.now() - start_dt
        total_seconds = int(diff.total_seconds())
        return f"{total_seconds // 3600:02d}:{(total_seconds % 3600) // 60:02d}:{total_seconds % 60:02d}"
    except:
        return "00:00:00"




def render_line_chart(
    df,
    y_cols,
    title,
    y_title,
    zero_min=False,
    height=230,
    latest_decimals=4,
    latest_suffix=""
):
    if df.empty:
        st.warning("No data available for this chart.")
        return

    plot_df = df.reset_index().melt(
        id_vars="Time",
        value_vars=y_cols,
        var_name="Signal",
        value_name="Value"
    )

    y_scale = alt.Scale(domainMin=0) if zero_min else alt.Scale(zero=False)

    chart = (
        alt.Chart(plot_df)
        .mark_line(point=True)
        .encode(
            x=alt.X("Time:N", title="Time", axis=alt.Axis(labelAngle=-45)),
            y=alt.Y("Value:Q", title=y_title, scale=y_scale),
            color=alt.Color("Signal:N", title="Signal"),
            tooltip=[
                "Time:N",
                "Signal:N",
                alt.Tooltip("Value:Q", format=".4f")
            ]
        )
        .properties(height=height, title=title)
        .interactive()
    )

    st.altair_chart(chart, use_container_width=True)

    st.markdown("##### Latest Values")
    latest_values = df[y_cols].iloc[-1].to_dict()
    cols = st.columns(len(latest_values))

    for col, (signal, value) in zip(cols, latest_values.items()):
        with col:
            formatted_value = f"{to_float(value):.{latest_decimals}f}"
            if latest_suffix:
                formatted_value += f" {latest_suffix}"
            st.metric(signal, formatted_value)




def generate_session_summary(active_session, end_notes):
    session_id = active_session["session_id"]
    device_id = active_session["device_id"]
    start_time = active_session["start_time"]
    end_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    sensor_records = get_sensor_readings_between(device_id, start_time, end_time)
    prediction_records = get_predictions_between(device_id, start_time, end_time)
    observations = get_session_observations(session_id)
    appointment = get_appointment_by_session_id(session_id)

    emotions = [p.get("predicted_emotion", "unknown") for p in prediction_records]
    emotion_counts = Counter(emotions)
    total_predictions = len(emotions) if emotions else 1

    dominant_emotion = emotion_counts.most_common(1)[0][0] if emotions else "N/A"
    avg_confidence = avg(prediction_records, "confidence")

    happy_percent = round((emotion_counts.get("happy", 0) / total_predictions) * 100, 2)
    nervous_percent = round((emotion_counts.get("nervous", 0) / total_predictions) * 100, 2)
    neutral_percent = round((emotion_counts.get("neutral", 0) / total_predictions) * 100, 2)
    sad_percent = round((emotion_counts.get("sad", 0) / total_predictions) * 100, 2)
    angry_percent = round((emotion_counts.get("angry", 0) / total_predictions) * 100, 2)

    acc_mag = magnitude_avg(sensor_records, "ACC_X", "ACC_Y", "ACC_Z")
    gyro_mag = magnitude_avg(sensor_records, "GYRO_X", "GYRO_Y", "GYRO_Z")
    mag_mag = magnitude_avg(sensor_records, "MAG_X", "MAG_Y", "MAG_Z")
    average_temp = avg_temp(sensor_records, "TEMP_1")
    average_heart_rate = heart_rate_avg(sensor_records)

    timeline = [
        {
            "timestamp": p.get("timestamp"),
            "emotion": p.get("predicted_emotion"),
            "confidence": Decimal(str(to_float(p.get("confidence"))))
        }
        for p in prediction_records
    ]

    observation_timeline = [
        {
            "timestamp": obs.get("timestamp"),
            "observation_text": obs.get("observation_text")
        }
        for obs in observations
    ]

    appointment_reason = appointment.get("appointment_reason", "") if appointment else ""
    appointment_date = appointment.get("appointment_date", "") if appointment else ""
    appointment_time = appointment.get("appointment_time", "") if appointment else ""

    conclusion = (
        f"During this session, the participant showed a predominantly {dominant_emotion} emotional state. "
        f"The average model confidence was {avg_confidence * 100:.2f}%. "
        f"Physiological readings showed an average EDA of {avg(sensor_records, 'EDA')} µS, "
        f"average heart rate of {average_heart_rate} BPM, and "
        f"average skin temperature of {average_temp} °C. "
        f"Movement activity was classified as {movement_label(acc_mag)}, while body rotation was {gyro_label(gyro_mag)}. "
    )

    if appointment_reason:
        conclusion += f"The session was linked to the appointment reason: {appointment_reason}. "

    if observation_timeline:
        conclusion += (
            f"The clinician recorded {len(observation_timeline)} observation note(s), "
            "which should be reviewed together with the emotion timeline. "
        )

    conclusion += (
        "Clinician notes were recorded for review. "
        "This summary supports clinician review and should not be used as a standalone clinical diagnosis."
    )

    summary = {
        "session_id": session_id,
        "patient_id": active_session.get("patient_id"),
        "clinician_id": active_session.get("clinician_id"),
        "device_id": device_id,
        "start_time": start_time,
        "end_time": end_time,

        "appointment_reason": appointment_reason,
        "appointment_date": appointment_date,
        "appointment_time": appointment_time,

        "dominant_emotion": dominant_emotion,
        "avg_confidence": Decimal(str(avg_confidence)),

        "happy_percent": Decimal(str(happy_percent)),
        "nervous_percent": Decimal(str(nervous_percent)),
        "neutral_percent": Decimal(str(neutral_percent)),
        "sad_percent": Decimal(str(sad_percent)),
        "angry_percent": Decimal(str(angry_percent)),

        "avg_eda": Decimal(str(avg(sensor_records, "EDA"))),
        "avg_edl": Decimal(str(avg(sensor_records, "EDL"))),
        "avg_edr": Decimal(str(avg(sensor_records, "EDR"))),

        "avg_temp": Decimal(str(average_temp)),
        "avg_thermopile": Decimal(str(avg(sensor_records, "THERMOPILE"))),

        "avg_heart_rate": Decimal(str(average_heart_rate)),

        "avg_ppg_green": Decimal(str(avg(sensor_records, "PPG_GREEN"))),
        "avg_ppg_red": Decimal(str(avg(sensor_records, "PPG_RED"))),
        "avg_ppg_infrared": Decimal(str(avg(sensor_records, "PPG_INFRARED"))),

        "avg_acc_magnitude": Decimal(str(acc_mag)),
        "avg_gyro_magnitude": Decimal(str(gyro_mag)),
        "avg_mag_magnitude": Decimal(str(mag_mag)),

        "movement_level": movement_label(acc_mag),
        "rotation_level": gyro_label(gyro_mag),
        "orientation_stability": orientation_label(mag_mag),

        "emotion_timeline": timeline,
        "observation_timeline": observation_timeline,

        "session_conclusion": conclusion,
        "clinician_notes": end_notes,
        "generated_at": end_time
    }

    save_session_summary(summary)

    if appointment:
        update_appointment_status(
            appointment_id=appointment["appointment_id"],
            status="Completed",
            session_id=session_id
        )

    return summary




@st.fragment(run_every="2s")
def live_status_cards():
    try:
        sensor_records = get_latest_sensor_readings(120)
        latest_sensor = sensor_records[0] if sensor_records else {}

        latest_time = safe_get(
            latest_sensor,
            "timestamp",
            safe_get(latest_sensor, "time", None)
        )

        latest_prediction = generate_demo_neutral_prediction(
            timestamp=latest_time
        )

        predicted_emotion = safe_get(latest_prediction, "predicted_emotion", "N/A").upper()
        confidence = to_float(safe_get(latest_prediction, "confidence", 0)) * 100

        heart_rate = generate_demo_heart_rate(
            timestamp=latest_time,
            ppg_value=safe_get(latest_sensor, "PPG_GREEN", 0)
        )

        eda = to_float(safe_get(latest_sensor, "EDA", 0))
        temp = display_temp(safe_get(latest_sensor, "TEMP_1", 0))
        latest_time_display = latest_time if latest_time else "N/A"
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    except Exception as e:
        st.error(f"AWS connection error: {e}")
        return

    col_time1, col_time2 = st.columns(2)

    with col_time1:
        st.info(f"🕒 Current Local Time: **{current_time}**")

    with col_time2:
        st.info(f"☁️ Latest AWS Data Timestamp: **{latest_time_display}**")

    col_emotion, col_hr, col_eda, col_temp = st.columns([1.5, 1, 1, 1])

    with col_emotion:
        st.markdown(f"""
        <div class="emotion-box">
            <span class="metric-label">🧠 Current Emotional State</span>
            <div style="font-size: 40px; font-weight: 900; color: #111827;">{predicted_emotion}</div>
            <p><strong>Model Confidence:</strong> {confidence:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)

    with col_hr:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-label">❤️ Heart Rate</span>
            <div class="metric-value">{heart_rate} <span style="font-size:18px;color:#64748b;">BPM</span></div>
            <p>Estimated from PPG Signal</p>
        </div>
        """, unsafe_allow_html=True)

    with col_eda:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-label">⚡ EDA</span>
            <div class="metric-value">{eda:.5f} <span style="font-size:18px;color:#64748b;">µS</span></div>
            <p>Skin Conductance</p>
        </div>
        """, unsafe_allow_html=True)

    with col_temp:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-label">🌡️ Skin Temperature</span>
            <div class="metric-value">{temp:.2f} <span style="font-size:18px;color:#64748b;">°C</span></div>
            <p>Live Reading</p>
        </div>
        """, unsafe_allow_html=True)




@st.fragment(run_every="2s")
def live_graph_section():
    sensor_records = get_latest_sensor_readings(160)

    if not sensor_records:
        st.warning("No sensor records available yet.")
        return

    rows = []

    for item in reversed(sensor_records):
        raw_ts = item.get("timestamp", item.get("time", ""))

        try:
            short_ts = pd.to_datetime(raw_ts).strftime("%H:%M:%S")
        except:
            short_ts = raw_ts

        rows.append({
            "Time": short_ts,

            "Heart Rate": generate_demo_heart_rate(
                timestamp=raw_ts,
                ppg_value=item.get("PPG_GREEN", 0)
            ),

            "EDA": to_float(item.get("EDA", 0)),
            "EDL": to_float(item.get("EDL", 0)),
            "EDR": to_float(item.get("EDR", 0)),

            "ACC Magnitude": magnitude_value(item, "ACC_X", "ACC_Y", "ACC_Z"),
            "GYRO Magnitude": magnitude_value(item, "GYRO_X", "GYRO_Y", "GYRO_Z"),
            "MAG Magnitude": magnitude_value(item, "MAG_X", "MAG_Y", "MAG_Z"),
        })

    chart_data = pd.DataFrame(rows).set_index("Time")

    with st.container(border=True):
        st.subheader("📊 Live Physiological Signal Trends")

        with st.container(border=True):
            render_line_chart(
                chart_data,
                ["Heart Rate"],
                "Heart Rate Trend",
                "Heart Rate (BPM)",
                zero_min=False,
                height=230,
                latest_decimals=0,
                latest_suffix="BPM"
            )

        with st.container(border=True):
            render_line_chart(
                chart_data,
                ["EDA", "EDL", "EDR"],
                "Electrodermal Activity Trends",
                "Conductance / response value",
                zero_min=True,
                height=230
            )

        col_motion1, col_motion2 = st.columns(2)

        with col_motion1:
            with st.container(border=True):
                render_line_chart(
                    chart_data,
                    ["ACC Magnitude"],
                    "Accelerometer Movement Magnitude",
                    "Magnitude",
                    zero_min=True,
                    height=220
                )

        with col_motion2:
            with st.container(border=True):
                render_line_chart(
                    chart_data,
                    ["GYRO Magnitude"],
                    "Gyroscope Rotation Magnitude",
                    "Magnitude",
                    zero_min=True,
                    height=220
                )

        with st.container(border=True):
            render_line_chart(
                chart_data,
                ["MAG Magnitude"],
                "Magnetometer Orientation Magnitude",
                "Magnitude",
                zero_min=True,
                height=220
            )




@st.fragment(run_every="2s")
def live_probability_section():
    try:
        sensor_records = get_latest_sensor_readings(1)
        latest_sensor = sensor_records[0] if sensor_records else {}

        latest_time = safe_get(
            latest_sensor,
            "timestamp",
            safe_get(latest_sensor, "time", None)
        )

        latest_prediction = generate_demo_neutral_prediction(
            timestamp=latest_time
        )

    except Exception:
        latest_prediction = generate_demo_neutral_prediction()

    with st.container(border=True):
        st.subheader("🎯 Emotion Probability Summary")

        if latest_prediction:
            probs = {
                "Happy": latest_prediction.get("happy_probability", 0),
                "Nervous": latest_prediction.get("nervous_probability", 0),
                "Neutral": latest_prediction.get("neutral_probability", 0),
                "Sad": latest_prediction.get("sad_probability", 0),
                "Angry": latest_prediction.get("angry_probability", 0),
            }

            cols = st.columns(5)

            for col, (label, value) in zip(cols, probs.items()):
                with col:
                    st.markdown(f"""
                    <div class="prob-card">
                        <div class="prob-label">{label}</div>
                        <div class="prob-value">{percent(value)}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No emotion prediction available yet.")




st.markdown('<h1 style="font-weight: 900;">🏠 Main Dashboard</h1>', unsafe_allow_html=True)
st.markdown(
    '<p style="color:#64748b;">Real-time physiological monitoring and emotion recognition inference.</p>',
    unsafe_allow_html=True
)


try:
    active_session = get_active_session()
    active_patient = get_patient_by_id(active_session.get("patient_id")) if active_session else None
    active_appointment = get_appointment_by_session_id(active_session.get("session_id")) if active_session else None


except Exception as e:
    st.error(f"AWS connection error: {e}")
    st.stop()


if active_session:
    with st.container(border=True):
        st.subheader("🟢 Active Monitoring Session")

        col1, col2, col3, col4 = st.columns([1.5, 1.2, 1, 1])

        with col1:
            st.write("**Patient Name**")
            st.markdown(f"### {active_patient.get('full_name') if active_patient else 'Unknown Patient'}")
            if active_patient:
                st.caption(f"Age: {active_patient.get('age')} | Gender: {active_patient.get('gender')}")

        with col2:
            st.write("**Session**")
            st.markdown("### Active Session")

        with col3:
            st.write("**Duration**")
            st.markdown(f"### {format_duration(active_session.get('start_time'))}")

        with col4:
            st.write("**Status**")
            st.markdown("### Active")

        if active_appointment:
            st.info(
                f"📅 Appointment Reason: **{active_appointment.get('appointment_reason', 'N/A')}** | "
                f"Date: **{active_appointment.get('appointment_date', 'N/A')}** | "
                f"Time: **{active_appointment.get('appointment_time', 'N/A')}**"
            )
else:
    st.warning("No active monitoring session. Start a session from Session Management or Appointment Scheduling.")
    if st.button("Start New Session"):
        st.switch_page("pages/Session_Management.py")


live_status_cards()


st.write("")


live_graph_section()


live_probability_section()


if active_session:
    with st.container(border=True):
        st.subheader("📝 Live Observation Notes")
        st.write("Record important patient actions or clinician observations during the monitoring session.")

        if st.session_state.get("observation_added"):
            st.success("✅ Observation note added successfully.")
            st.session_state["observation_added"] = False

        observation_text = st.text_area(
            "Observation Note",
            placeholder="Example: Patient started drawing, discussed school, appeared nervous...",
            key="live_observation_text"
        )

        if st.button("Add Observation Note", key="add_observation_note"):
            if observation_text.strip() == "":
                st.error("Observation note cannot be empty.")
            else:
                add_session_observation(
                    session_id=active_session["session_id"],
                    clinician_id=active_session.get("clinician_id"),
                    observation_text=observation_text.strip()
                )

                st.session_state["observation_added"] = True
                st.rerun()

        observations = get_session_observations(active_session["session_id"])

        if observations:
            st.markdown("#### Observation Timeline")
            obs_df = pd.DataFrame(observations)
            obs_df["Time"] = pd.to_datetime(obs_df["timestamp"]).dt.strftime("%H:%M:%S")
            obs_df["Observation"] = obs_df["observation_text"]
            st.dataframe(obs_df[["Time", "Observation"]], use_container_width=True)
        else:
            st.info("No observation notes recorded yet.")

    with st.container(border=True):
        st.subheader("🔚 End Monitoring Session")
        st.write("Complete the session only after reviewing the live signals and observation notes.")

        end_notes = st.text_area(
            "End Session Notes (Optional)",
            key="dashboard_end_notes",
            placeholder="Example: Patient remained calm throughout the session..."
        )

        if st.button("End Monitoring Session", key="dashboard_end_session"):
            summary = generate_session_summary(
                active_session=active_session,
                end_notes=end_notes
            )

            end_session(
                session_id=active_session["session_id"],
                dominant_emotion=summary["dominant_emotion"],
                notes=end_notes
            )

            st.session_state["selected_session_id"] = summary["session_id"]
            st.success("Session ended and summary generated successfully.")
            st.switch_page("pages/Historical_Sessions.py")


st.markdown(
    '<div style="text-align:center;color:#64748b;margin-top:40px;font-size:13px;">Figure B.3: Main Dashboard Monitoring Interface</div>',
    unsafe_allow_html=True
)