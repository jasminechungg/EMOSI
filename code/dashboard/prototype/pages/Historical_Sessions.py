import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
from io import BytesIO
from decimal import Decimal

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from xml.sax.saxutils import escape

from aws_dynamodb import (
    get_sessions_by_clinician,
    get_session_by_id,
    get_patient_by_id,
    get_session_summary
)

from ui_components import apply_global_style, render_sidebar


st.set_page_config(
    page_title="Historical Sessions",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)


if not st.session_state.get("logged_in", False):
    st.switch_page("main.py")


if st.session_state.user.get("role") != "clinician":
    st.error("Access denied. This page is only available for clinicians.")
    st.stop()


apply_global_style()
render_sidebar("Historical Sessions")


st.markdown("""
<style>
div.stDownloadButton > button {
    background-color: #f0fdf4 !important;
    color: #166534 !important;
    border: 1.5px solid #16a34a !important;
    border-radius: 10px !important;
    font-weight: 800 !important;
    height: 48px !important;
}

div.stDownloadButton > button:hover {
    background-color: #dcfce7 !important;
    color: #14532d !important;
    border-color: #15803d !important;
}
</style>
""", unsafe_allow_html=True)


user = st.session_state.user
clinician_id = user["user_id"]


def to_float(value):
    try:
        if isinstance(value, Decimal):
            return float(value)
        return float(value)
    except:
        return 0.0


def fmt(value):
    return f"{to_float(value):.2f}"


def fmt_percent(value):
    return f"{to_float(value):.2f}%"


def format_datetime(value):
    try:
        return pd.to_datetime(value).strftime("%d %b %Y, %H:%M")
    except:
        return value or "N/A"


def calculate_duration(start_time, end_time):
    try:
        start_dt = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")
        end_dt = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S")
        return str(end_dt - start_dt)
    except:
        return "N/A"


def build_session_display_data(completed_sessions):
    sorted_sessions = sorted(completed_sessions, key=lambda x: x.get("start_time", ""))
    patient_counter = {}
    rows = []
    options = {}

    for session in sorted_sessions:
        patient_id = session.get("patient_id")
        patient = get_patient_by_id(patient_id)
        patient_name = patient.get("full_name") if patient else "Unknown Patient"

        patient_counter[patient_id] = patient_counter.get(patient_id, 0) + 1
        session_no = patient_counter[patient_id]

        start_time = session.get("start_time", "")
        end_time = session.get("end_time", "")

        display_label = f"{patient_name} - Session {session_no} - {format_datetime(start_time)}"

        rows.append({
            "Patient Name": patient_name,
            "Session": f"Session {session_no}",
            "Date": format_datetime(start_time),
            "Duration": calculate_duration(start_time, end_time),
            "Dominant Emotion": session.get("dominant_emotion", "N/A").upper()
        })

        options[display_label] = {
            "session_id": session.get("session_id"),
            "session_no": session_no,
            "patient_name": patient_name
        }

    return rows, options


def generate_pdf(patient, session, summary, session_label):
    """
    EMOSI PDF report generated from the true selected session details.
    This uses real data from:
    - patient
    - session
    - summary
    """

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=42,
        bottomMargin=42
    )

    width, height = A4
    story = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        "SubtitleStyle",
        parent=styles["BodyText"],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#475569"),
        spaceAfter=12
    )

    section_style = ParagraphStyle(
        "SectionStyle",
        parent=styles["Heading2"],
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#1e3a8a"),
        spaceBefore=12,
        spaceAfter=8
    )

    normal_style = ParagraphStyle(
        "NormalStyle",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#111827")
    )

    small_style = ParagraphStyle(
        "SmallStyle",
        parent=styles["BodyText"],
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#475569")
    )

    white_style = ParagraphStyle(
        "WhiteStyle",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=13,
        textColor=colors.white
    )

    header_white_style = ParagraphStyle(
        "HeaderWhiteStyle",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=12,
        textColor=colors.white,
        alignment=1
    )

    def clean(value):
        return escape(str(value)) if value is not None and value != "" else "N/A"

    def p(text, style=normal_style):
        return Paragraph(clean(text), style)

    def rich(text, style=normal_style):
        return Paragraph(text, style)

    def section(title):
        story.append(Paragraph(title, section_style))

    def safe_upper(value):
        return str(value).upper() if value else "N/A"

    def draw_page_design(canvas_obj, doc_obj):
        canvas_obj.saveState()

        canvas_obj.setFillColor(colors.HexColor("#1e3a8a"))
        canvas_obj.rect(0, height - 20, width, 20, stroke=0, fill=1)

        canvas_obj.setStrokeColor(colors.HexColor("#cbd5e1"))
        canvas_obj.line(36, 34, width - 36, 34)

        canvas_obj.setFont("Helvetica", 8)
        canvas_obj.setFillColor(colors.HexColor("#64748b"))
        canvas_obj.drawString(
            36,
            22,
            "EMOSI - Emotion and Behaviour Monitoring System"
        )
        canvas_obj.drawRightString(
            width - 36,
            22,
            f"Page {doc_obj.page}"
        )

        canvas_obj.restoreState()

    # =========================
    # TRUE SESSION DATA
    # =========================
    patient_name = patient.get("full_name", "Unknown Patient")
    patient_age = patient.get("age", "N/A")
    patient_gender = patient.get("gender", "N/A")
    guardian_name = patient.get("guardian_name", "N/A")

    start_time = format_datetime(session.get("start_time"))
    end_time = format_datetime(session.get("end_time"))
    duration = calculate_duration(session.get("start_time"), session.get("end_time"))

    dominant_emotion = safe_upper(summary.get("dominant_emotion", "N/A"))
    avg_confidence = f"{to_float(summary.get('avg_confidence', 0)) * 100:.2f}%"

    happy_percent = to_float(summary.get("happy_percent", 0))
    nervous_percent = to_float(summary.get("nervous_percent", 0))
    neutral_percent = to_float(summary.get("neutral_percent", 0))
    sad_percent = to_float(summary.get("sad_percent", 0))
    angry_percent = to_float(summary.get("angry_percent", 0))

    avg_eda = fmt(summary.get("avg_eda", 0))
    avg_edl = fmt(summary.get("avg_edl", 0))
    avg_edr = fmt(summary.get("avg_edr", 0))
    avg_temp = fmt(summary.get("avg_temp", 0))
    avg_thermopile = fmt(summary.get("avg_thermopile", 0))
    avg_heart_rate = fmt(summary.get("avg_heart_rate", 0))

    avg_ppg_green = fmt(summary.get("avg_ppg_green", 0))
    avg_ppg_red = fmt(summary.get("avg_ppg_red", 0))
    avg_ppg_infrared = fmt(summary.get("avg_ppg_infrared", 0))

    movement_level = summary.get("movement_level", "N/A")
    rotation_level = summary.get("rotation_level", "N/A")
    orientation_stability = summary.get("orientation_stability", "N/A")

    timeline = summary.get("emotion_timeline", [])
    observations = summary.get("observation_timeline", [])
    conclusion = summary.get("session_conclusion", "No conclusion generated.")
    clinician_notes = summary.get("clinician_notes", "No notes recorded.")

    # =========================
    # HEADER
    # =========================
    header_table = Table(
        [
            [
                rich("<b>EMOSI</b><br/>Emotion and Behaviour Monitoring System", white_style),
                rich("<b>Session Summary Report</b><br/>Generated from Actual Session Data", white_style)
            ]
        ],
        colWidths=[3.4 * inch, 3.4 * inch]
    )

    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#1e3a8a")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#1e3a8a")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))

    story.append(header_table)
    story.append(Spacer(1, 14))

    story.append(Paragraph("EMOSI Session Summary Report", title_style))
    story.append(Paragraph(
        "This report summarizes the selected monitoring session using the recorded patient information, "
        "emotion prediction results, physiological indicators, observation timeline, and clinician notes.",
        subtitle_style
    ))

    # =========================
    # SUMMARY CARDS
    # =========================
    card_data = [
        [
            rich(f"<b>Dominant Emotion</b><br/><font size='16'>{dominant_emotion}</font>", normal_style),
            rich(f"<b>Average Confidence</b><br/><font size='16'>{avg_confidence}</font>", normal_style),
            rich(f"<b>Heart Rate</b><br/><font size='16'>{avg_heart_rate} BPM</font>", normal_style),
            rich(f"<b>Movement</b><br/><font size='16'>{clean(movement_level)}</font>", normal_style),
        ]
    ]

    card_table = Table(card_data, colWidths=[1.7 * inch, 1.7 * inch, 1.7 * inch, 1.7 * inch])
    card_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#fee2e2")),
        ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#dbeafe")),
        ("BACKGROUND", (2, 0), (2, 0), colors.HexColor("#dcfce7")),
        ("BACKGROUND", (3, 0), (3, 0), colors.HexColor("#fef3c7")),
        ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#cbd5e1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))

    story.append(card_table)
    story.append(Spacer(1, 10))

    # =========================
    # PATIENT + SESSION INFO
    # =========================
    section("1. Patient and Session Information")

    session_info = [
        ["Patient Name", patient_name],
        ["Age", patient_age],
        ["Gender", patient_gender],
        ["Guardian", guardian_name],
        ["Session", session_label],
        ["Start Time", start_time],
        ["End Time", end_time],
        ["Duration", duration],
    ]

    session_info_table = Table(
        [[p(a), p(b)] for a, b in session_info],
        colWidths=[2.0 * inch, 4.8 * inch]
    )

    session_info_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f1f5f9")),
        ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#cbd5e1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#e2e8f0")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))

    story.append(session_info_table)

    # =========================
    # EMOTION DISTRIBUTION
    # =========================
    section("2. Emotion Distribution")

    emotion_table_data = [
        [
            rich("<b>Emotion</b>", header_white_style),
            rich("<b>Percentage</b>", header_white_style),
            rich("<b>Interpretation</b>", header_white_style)
        ],
        [p("Happy"), p(f"{happy_percent:.2f}%"), p("Positive or pleasant emotional response")],
        [p("Nervous"), p(f"{nervous_percent:.2f}%"), p("Possible stress, hesitation, or uncertainty")],
        [p("Neutral"), p(f"{neutral_percent:.2f}%"), p("Stable or regulated emotional state")],
        [p("Sad"), p(f"{sad_percent:.2f}%"), p("Low engagement or negative emotional response")],
        [p("Angry"), p(f"{angry_percent:.2f}%"), p("Possible frustration or discomfort")],
    ]

    emotion_table = Table(
        emotion_table_data,
        colWidths=[1.3 * inch, 1.2 * inch, 4.3 * inch]
    )

    emotion_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
        ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#dcfce7")),
        ("BACKGROUND", (0, 2), (-1, 2), colors.HexColor("#ffedd5")),
        ("BACKGROUND", (0, 3), (-1, 3), colors.HexColor("#f8fafc")),
        ("BACKGROUND", (0, 4), (-1, 4), colors.HexColor("#fee2e2")),
        ("BACKGROUND", (0, 5), (-1, 5), colors.HexColor("#fef3c7")),
        ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#cbd5e1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#e2e8f0")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))

    story.append(emotion_table)

    # =========================
    # PHYSIOLOGICAL SUMMARY
    # =========================
    section("3. Physiological and Motion Summary")

    physio_table_data = [
        [
            rich("<b>Indicator</b>", header_white_style),
            rich("<b>Value</b>", header_white_style),
            rich("<b>Description</b>", header_white_style)
        ],
        [p("Average EDA"), p(f"{avg_eda} µS"), p("Average skin conductance level during the session")],
        [p("Average EDL"), p(f"{avg_edl} µS"), p("Tonic component / baseline electrodermal level")],
        [p("Average EDR"), p(f"{avg_edr} µS"), p("Phasic component / short-term electrodermal response")],
        [p("Average Heart Rate"), p(f"{avg_heart_rate} BPM"), p("Estimated heart rate derived from PPG signal")],
        [p("Average Skin Temperature"), p(f"{avg_temp} °C"), p("Average skin temperature reading")],
        [p("Average Thermopile"), p(avg_thermopile), p("Thermal sensor reading")],
        [p("PPG Green"), p(avg_ppg_green), p("Raw optical PPG green channel")],
        [p("PPG Red"), p(avg_ppg_red), p("Raw optical PPG red channel")],
        [p("PPG Infrared"), p(avg_ppg_infrared), p("Raw optical PPG infrared channel")],
        [p("Movement Level"), p(movement_level), p("Overall accelerometer-based movement level")],
        [p("Rotation Level"), p(rotation_level), p("Gyroscope-based body rotation level")],
        [p("Orientation Stability"), p(orientation_stability), p("Magnetometer-based orientation stability")],
    ]

    physio_table = Table(
        physio_table_data,
        colWidths=[1.7 * inch, 1.4 * inch, 3.7 * inch]
    )

    physio_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f766e")),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f0fdfa")),
        ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#99f6e4")),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#ccfbf1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))

    story.append(physio_table)

    # =========================
    # EMOTION TIMELINE
    # =========================
    section("4. Emotion Timeline")

    timeline_table_data = [
        [
            rich("<b>Time</b>", header_white_style),
            rich("<b>Emotion</b>", header_white_style),
            rich("<b>Confidence</b>", header_white_style)
        ]
    ]

    if timeline:
        for item in timeline[:25]:
            timeline_table_data.append([
                p(format_datetime(item.get("timestamp"))),
                p(str(item.get("emotion", "N/A")).title()),
                p(f"{to_float(item.get('confidence', 0)) * 100:.2f}%")
            ])
    else:
        timeline_table_data.append([p("N/A"), p("No timeline records available"), p("N/A")])

    timeline_table = Table(
        timeline_table_data,
        colWidths=[2.5 * inch, 2.0 * inch, 2.3 * inch]
    )

    timeline_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#7c3aed")),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#faf5ff")),
        ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#ddd6fe")),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#ede9fe")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))

    story.append(timeline_table)

    # =========================
    # OBSERVATION TIMELINE
    # =========================
    section("5. Observation Timeline")

    observation_table_data = [
        [
            rich("<b>Time</b>", header_white_style),
            rich("<b>Observation</b>", header_white_style)
        ]
    ]

    if observations:
        for obs in observations[:20]:
            observation_table_data.append([
                p(format_datetime(obs.get("timestamp"))),
                p(obs.get("observation_text", ""))
            ])
    else:
        observation_table_data.append([p("N/A"), p("No observations recorded")])

    observation_table = Table(
        observation_table_data,
        colWidths=[2.2 * inch, 4.6 * inch]
    )

    observation_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#334155")),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f8fafc")),
        ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#cbd5e1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#e2e8f0")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))

    story.append(observation_table)

    # =========================
    # CONCLUSION + NOTES
    # =========================
    section("6. Generated Session Conclusion")

    story.append(Paragraph(clean(conclusion), normal_style))

    story.append(Spacer(1, 8))

    section("7. Clinician Notes")

    story.append(Paragraph(clean(clinician_notes), normal_style))

    story.append(Spacer(1, 14))

    disclaimer_table = Table(
        [[Paragraph(
            "<b>Important Note:</b> This report is generated for monitoring and review purposes only. "
            "It supports clinician judgement but should not be used as a standalone clinical diagnosis.",
            small_style
        )]],
        colWidths=[6.8 * inch]
    )

    disclaimer_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fff7ed")),
        ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#fdba74")),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))

    story.append(disclaimer_table)

    doc.build(
        story,
        onFirstPage=draw_page_design,
        onLaterPages=draw_page_design
    )

    buffer.seek(0)
    return buffer


st.title("📜 Historical Sessions")
st.write("Review completed monitoring sessions and generated patient session summaries.")


sessions = get_sessions_by_clinician(clinician_id)
completed_sessions = [s for s in sessions if s.get("session_status") == "completed"]


if not completed_sessions:
    st.info("No completed sessions found.")
    st.stop()


history_rows, session_options = build_session_display_data(completed_sessions)
df = pd.DataFrame(history_rows)


st.subheader("📋 Session History")
st.dataframe(df, use_container_width=True)


session_labels = list(session_options.keys())
default_index = 0


if st.session_state.get("selected_session_id"):
    for i, label in enumerate(session_labels):
        if session_options[label]["session_id"] == st.session_state["selected_session_id"]:
            default_index = i
            break


selected_label = st.selectbox(
    "Select Patient Session",
    session_labels,
    index=default_index
)


if st.session_state.get("selected_session_id"):
    st.session_state["selected_session_id"] = None


selected_info = session_options[selected_label]
selected_session_id = selected_info["session_id"]
selected_session_no = selected_info["session_no"]


session = get_session_by_id(selected_session_id)
patient = get_patient_by_id(session.get("patient_id"))
summary = get_session_summary(selected_session_id)


st.markdown("---")
st.subheader(f"📌 Session Summary Report: {selected_info['patient_name']} - Session {selected_session_no}")


if not summary:
    st.warning("No generated summary found for this session.")
    st.stop()


col1, col2, col3 = st.columns(3)


with col1:
    st.metric("Dominant Emotion", summary.get("dominant_emotion", "N/A").upper())


with col2:
    st.metric("Average Confidence", f"{to_float(summary.get('avg_confidence')) * 100:.2f}%")


with col3:
    st.metric("Movement Level", summary.get("movement_level", "N/A"))


st.markdown("---")


st.subheader("👤 Patient and Session Details")
col_a, col_b = st.columns(2)


with col_a:
    st.write(f"**Patient Name:** {patient.get('full_name') if patient else 'Unknown'}")
    if patient:
        st.write(f"**Age:** {patient.get('age')}")
        st.write(f"**Gender:** {patient.get('gender')}")
        st.write(f"**Guardian:** {patient.get('guardian_name', 'N/A')}")


with col_b:
    st.write(f"**Session:** Session {selected_session_no}")
    st.write(f"**Start Time:** {format_datetime(session.get('start_time'))}")
    st.write(f"**End Time:** {format_datetime(session.get('end_time'))}")
    st.write(f"**Duration:** {calculate_duration(session.get('start_time'), session.get('end_time'))}")


st.markdown("---")


st.subheader("🎯 Emotion Percentage Summary")


emotion_data = {
    "Happy": to_float(summary.get("happy_percent", 0)),
    "Nervous": to_float(summary.get("nervous_percent", 0)),
    "Neutral": to_float(summary.get("neutral_percent", 0)),
    "Sad": to_float(summary.get("sad_percent", 0)),
    "Angry": to_float(summary.get("angry_percent", 0)),
}


emotion_cols = st.columns(5)
for col, (label, value) in zip(emotion_cols, emotion_data.items()):
    with col:
        st.metric(label, f"{value:.2f}%")


emotion_chart_df = pd.DataFrame({
    "Emotion": list(emotion_data.keys()),
    "Percentage": list(emotion_data.values())
})


emotion_chart = (
    alt.Chart(emotion_chart_df)
    .mark_bar()
    .encode(
        x=alt.X("Emotion:N", title="Emotion"),
        y=alt.Y("Percentage:Q", title="Percentage (%)", scale=alt.Scale(domainMin=0)),
        tooltip=[
            "Emotion:N",
            alt.Tooltip("Percentage:Q", format=".2f")
        ]
    )
    .properties(height=320)
)


st.altair_chart(emotion_chart, use_container_width=True)


st.markdown("---")


st.subheader("🧾 Physiological and Motion Summary")
metric_cols = st.columns(4)


with metric_cols[0]:
    st.metric("Avg EDA", fmt(summary.get("avg_eda", 0)))
    st.metric("Avg EDL", fmt(summary.get("avg_edl", 0)))
    st.metric("Avg EDR", fmt(summary.get("avg_edr", 0)))


with metric_cols[1]:
    st.metric("Avg Skin Temp", f"{fmt(summary.get('avg_temp', 0))} °C")
    st.metric("Avg Thermopile", fmt(summary.get("avg_thermopile", 0)))


with metric_cols[2]:
    st.metric("Avg PPG Green", fmt(summary.get("avg_ppg_green", 0)))
    st.metric("Avg PPG Red", fmt(summary.get("avg_ppg_red", 0)))
    st.metric("Avg PPG Infrared", fmt(summary.get("avg_ppg_infrared", 0)))


with metric_cols[3]:
    st.metric("Movement", summary.get("movement_level", "N/A"))
    st.metric("Rotation", summary.get("rotation_level", "N/A"))
    st.metric("Orientation", summary.get("orientation_stability", "N/A"))


st.markdown("---")


st.subheader("🕒 Emotion Timeline")
timeline = summary.get("emotion_timeline", [])


if timeline:
    timeline_df = pd.DataFrame(timeline)

    if "timestamp" in timeline_df.columns:
        timeline_df["Time"] = timeline_df["timestamp"].apply(format_datetime)
        timeline_df["Short Time"] = timeline_df["timestamp"].apply(lambda x: pd.to_datetime(x).strftime("%H:%M:%S"))

    if "emotion" in timeline_df.columns:
        timeline_df["Emotion"] = timeline_df["emotion"].apply(lambda x: str(x).title())

    if "confidence" in timeline_df.columns:
        timeline_df["Confidence"] = timeline_df["confidence"].apply(lambda x: f"{to_float(x) * 100:.2f}%")
        timeline_df["Confidence Value"] = timeline_df["confidence"].apply(lambda x: round(to_float(x) * 100, 2))

    display_cols = [col for col in ["Time", "Emotion", "Confidence"] if col in timeline_df.columns]
    st.dataframe(timeline_df[display_cols], use_container_width=True)

    if "Short Time" in timeline_df.columns and "Emotion" in timeline_df.columns:
        timeline_chart = (
            alt.Chart(timeline_df)
            .mark_circle(size=120)
            .encode(
                x=alt.X("Short Time:N", title="Time", axis=alt.Axis(labelAngle=-45)),
                y=alt.Y("Emotion:N", title="Emotion"),
                color=alt.Color("Emotion:N", title="Emotion"),
                tooltip=[
                    "Time:N",
                    "Emotion:N",
                    alt.Tooltip("Confidence Value:Q", title="Confidence (%)", format=".2f")
                ]
            )
            .properties(height=280)
        )

        st.altair_chart(timeline_chart, use_container_width=True)

else:
    st.info("No timeline records available.")


st.markdown("---")


st.subheader("📝 Observation Timeline")
observations = summary.get("observation_timeline", [])


if observations:
    obs_df = pd.DataFrame(observations)

    if "timestamp" in obs_df.columns:
        obs_df["Time"] = obs_df["timestamp"].apply(format_datetime)

    if "observation_text" in obs_df.columns:
        obs_df["Observation"] = obs_df["observation_text"]

    st.dataframe(obs_df[["Time", "Observation"]], use_container_width=True)
else:
    st.info("No observation notes recorded.")


st.markdown("---")


st.subheader("🧠 Generated Session Conclusion")
st.info(summary.get("session_conclusion", "No conclusion generated."))


st.markdown("---")


st.subheader("📝 Clinician Notes")
notes = summary.get("clinician_notes", "")
st.info(notes if notes else "No notes recorded.")


st.markdown("---")


pdf_file = generate_pdf(patient or {}, session, summary, f"Session {selected_session_no}")
safe_patient_name = selected_info["patient_name"].replace(" ", "_")


st.download_button(
    label="📄 Download Session Summary PDF",
    data=pdf_file,
    file_name=f"{safe_patient_name}_Session_{selected_session_no}_summary.pdf",
    mime="application/pdf",
    use_container_width=True
)


st.markdown(
    "<div style='text-align:center;color:#64748b;margin-top:40px;'>Figure B.5: Historical Session Summary Report Interface</div>",
    unsafe_allow_html=True
)