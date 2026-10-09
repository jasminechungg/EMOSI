import streamlit as st
import pandas as pd

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="EmoSI - Historical Records",
    page_icon="🧠",
    layout="wide"  # Wide layout allows a clean view of data tables and filters
)

# --- GLOBAL STYLING (Consistent light theme) ---
st.markdown("""
<style>
/* Main App Background */
.stApp {
    background-color: #f4f7fb;
    color: #000000;
}

/* Hide Default Headers/Footers */
header, footer {
    visibility: hidden;
}

h1, h2, h3, p, label {
    color: #000000 !important;
}

/* Light Sidebar Style Override */
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e2e8f0;
}

[data-testid="stSidebar"] h3, 
[data-testid="stSidebar"] h4, 
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
    color: #000000 !important;
}

/* --- REVISED LIGHT NAVIGATION & ACTION BUTTON STYLING --- */
div.stButton > button {
    width: 100% !important;
    height: 45px !important;
    border-radius: 10px !important;
    background-color: #ffffff !important;      /* Clean white background */
    color: #16a34a !important;                 /* Vibrant green text and icons */
    border: 1.5px solid #16a34a !important;    /* Solid green border outline */
    font-size: 15px !important;
    font-weight: 600 !important;
    margin-bottom: 5px !important;
    transition: all 0.2s ease-in-out;
}

/* Hover/Active states matching the consistent aesthetic framework */
div.stButton > button:hover {
    background-color: #16a34a !important;
    color: #ffffff !important;
    border-color: #16a34a !important;
}

div.stButton > button:active, div.stButton > button:focus {
    background-color: #15803d !important;
    color: #ffffff !important;
    border-color: #15803d !important;
}

/* Table Style Adjustments for Clear Scannability */
.stDataFrame table {
    border-radius: 10px;
    overflow: hidden;
}

div[data-testid="stDataFrameResizer"] {
    background-color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION & USER PROFILE ---
with st.sidebar:
    st.markdown("### 🧠 EmoSI Platform")
    st.markdown("---")
    
    # User Profile Section
    st.markdown("#### **User Profile**")
    st.markdown("""
    <div style="background-color: #f8fafc; padding: 15px; border-radius: 8px; border: 1px solid #e2e8f0;">
        <p style="margin: 0; font-size: 14px;">👤 <strong>Clinician:</strong> Jasmine</p>
        <p style="margin: 5px 0 0 0; font-size: 14px;">🆔 <strong>Role:</strong> Primary Assessor</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    # Navigation Buttons
    st.markdown("#### **Navigation**")
    st.button("🏠 Dashboard Home", use_container_width=True)
    st.button("📈 Real-Time Signals", use_container_width=True)
    st.button("📜 Historical Sessions", use_container_width=True)
    st.button("⚙️ User Management", use_container_width=True)
    
    st.markdown("---")
    # Status Widget
    st.markdown("#### **System Status**")
    st.success("🟢 **Wearable Sensor:** Active")
    st.success("🟢 **Data Stream:** Synced")

# --- MAIN INTERFACE LAYOUT ---
st.markdown('<h1 style="font-weight: 900; margin-bottom: 5px;">📜 Historical Monitoring Records</h1>', unsafe_allow_html=True)
st.markdown('<p style="color: #64748b; font-size: 16px; margin-bottom: 25px;">Review past physiological sessions and emotional classification results archived within AWS DynamoDB.</p>', unsafe_allow_html=True)

# --- FILTER CONTROLS SECTION ---
with st.container(border=True):
    st.markdown("### 🔍 Search & Filter Sessions")
    col_search, col_emotion, col_date = st.columns([2, 1, 1])
    
    with col_search:
        st.text_input("Search by Session ID or Participant Profile", placeholder="e.g., Session-04")
    with col_emotion:
        st.selectbox("Filter by Emotion", ["All Emotions", "Happy", "Sad", "Nervous", "Neutral", "Angry"])
    with col_date:
        st.selectbox("Timeframe", ["All Records", "Today", "Past 7 Days", "Past 30 Days"])

st.write("")

# --- HISTORICAL DATA TABLE GENERATION ---
session_data = {
    "Session ID": ["SESS-2026-0520A", "SESS-2026-0518C", "SESS-2026-0515B", "SESS-2026-0512A", "SESS-2026-0510D"],
    "Date & Time": ["20 May 2026, 14:30", "18 May 2026, 10:15", "15 May 2026, 16:45", "12 May 2026, 11:00", "10 May 2026, 09:20"],
    "Duration": ["15 mins", "20 mins", "12 mins", "18 mins", "25 mins"],
    "Avg Heart Rate (BPM)": [76, 88, 82, 74, 95],
    "Avg EDA (µS)": [2.48, 4.12, 1.95, 2.33, 5.84],
    "Avg Temp (°C)": [32.1, 31.9, 32.3, 32.1, 31.6],
    "Dominant Emotion (XGBoost)": ["Neutral", "Nervous", "Sad", "Happy", "Angry"],
    "Model Confidence": ["94.2%", "89.5%", "91.1%", "95.6%", "87.4%"]
}

df = pd.DataFrame(session_data)

with st.container(border=True):
    st.markdown("### 📁 Archived Logs Table")
    st.write("Select a row to pull granular raw data and longitudinal feature summaries from cloud storage.")
    
    # Render interactive clean table dataframe
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Session ID": st.column_config.TextColumn("Session ID", help="Unique data packet key in DynamoDB"),
            "Dominant Emotion (XGBoost)": st.column_config.TextColumn("Classification Result"),
            "Model Confidence": st.column_config.ProgressColumn("Confidence Score", format="%s", min_value=0, max_value=100)
        }
    )

st.write("")

# --- ACTION ELEMENTS ROW ---
col_spacer, col_btn_view, col_btn_export = st.columns([3, 1, 1])
with col_btn_view:
    st.button("🔍 View Selected Session Details", use_container_width=True)
with col_btn_export:
    st.button("📥 Export Session to CSV", use_container_width=True)

# Footer placeholder for report appendix captioning
st.markdown('<div style="text-align: center; color: #64748b; margin-top: 40px; font-size: 13px;">Figure B.5: Historical Monitoring Records Interface</div>', unsafe_allow_html=True)