import streamlit as st
import numpy as np
import pandas as pd

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="EmoSI - Emotion Analysis",
    page_icon="🧠",
    layout="wide"
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

/* --- REVISED LIGHT NAVIGATION BUTTON STYLING --- */
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

/* Large Analytics Highlight Box */
.analysis-hero {
    background-color: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(15, 23, 42, 0.04);
    border: 1px solid #e2e8f0;
    border-left: 8px solid #16a34a;
}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION & USER PROFILE ---
with st.sidebar:
    st.markdown("### 🧠 EmoSI Platform")
    st.markdown("---")
    
    st.markdown("#### **User Profile**")
    st.markdown("""
    <div style="background-color: #f8fafc; padding: 15px; border-radius: 8px; border: 1px solid #e2e8f0;">
        <p style="margin: 0; font-size: 14px;">👤 <strong>Clinician:</strong> Jasmine</p>
        <p style="margin: 5px 0 0 0; font-size: 14px;">🆔 <strong>Role:</strong> Primary Assessor</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("#### **Navigation**")
    st.button("🏠 Dashboard Home", use_container_width=True)
    st.button("📈 Real-Time Signals", use_container_width=True)
    st.button("📜 Historical Sessions", use_container_width=True)
    st.button("⚙️ User Management", use_container_width=True)
    
    st.markdown("---")
    st.markdown("#### **System Status**")
    st.success("🟢 **Wearable Sensor:** Active")
    st.success("🟢 **Data Stream:** Synced")

# --- MAIN INTERFACE LAYOUT ---
st.markdown('<h1 style="font-weight: 900; margin-bottom: 5px;">📊 Emotion Prediction & Analysis</h1>', unsafe_allow_html=True)
st.markdown('<p style="color: #64748b; font-size: 16px; margin-bottom: 25px;">Post-session diagnostic overview mapping feature distributions and XGBoost classification profiles.</p>', unsafe_allow_html=True)

# --- SESSION OVERVIEW HEADER ---
with st.container(border=True):
    col_id, col_ts, col_dur = st.columns(3)
    with col_id:
        st.markdown("**Session ID:** `SESS-2026-0520A`", unsafe_allow_html=True)
    with col_ts:
        st.markdown("**Timestamp:** 20 May 2026, 14:30", unsafe_allow_html=True)
    with col_dur:
        st.markdown("**Total Assessment Duration:** 15 Minutes", unsafe_allow_html=True)

st.write("")

# --- ROW 1: PREDICTION HERO & CONFIDENCE SCORES ---
col_hero, col_probs = st.columns([1.2, 1.8])

with col_hero:
    st.markdown("""
    <div class="analysis-hero">
        <span style="font-size: 13px; color: #64748b; font-weight: 600; text-transform: uppercase;">Dominant Classification</span>
        <div style="font-size: 48px; font-weight: 900; color: #111827; margin-top: 5px;">NEUTRAL</div>
        <hr style="margin: 15px 0; border: 0; border-top: 1px solid #e2e8f0;">
        <p style="margin: 0; font-size: 15px; color: #334155;"><strong>Primary Model:</strong> XGBoost Ensemble</p>
        <p style="margin: 5px 0 0 0; font-size: 15px; color: #334155;"><strong>Overall Confidence:</strong> 94.2%</p>
    </div>
    """, unsafe_allow_html=True)

with col_probs:
    with st.container(border=True):
        st.markdown("### 🎯 Model Probability Distribution")
        
        # Mapping model probability distributions for the 5 target categories
        confidence_data = pd.DataFrame({
            'Probability (%)': [94.2, 2.8, 1.5, 1.0, 0.5]
        }, index=['Neutral', 'Happy', 'Nervous', 'Sad', 'Angry'])
        
        st.bar_chart(confidence_data, horizontal=True, height=160)

st.write("")

# --- ROW 2: EMOTION TREND OVER TIME & FEATURE HIGHLIGHTS ---
col_trend, col_features = st.columns([2, 1])

with col_trend:
    with st.container(border=True):
        st.markdown("### 📈 Emotional State Progression")
        st.write("Longitudinal timeline indexing output tracking fluctuations across the assessment interval.")
        
        # Simulating time-series categorical mapping output
        timeline = np.linspace(0, 15, 30)
        trend_map = pd.DataFrame({
            'Classification Value (Index)': [1, 1, 1, 2, 2, 1, 1, 3, 3, 1, 1, 1, 1, 4, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        }, index=timeline)
        st.line_chart(trend_map, height=220)
        st.caption("Value Keys: 0 = Angry, 1 = Neutral, 2 = Happy, 3 = Nervous, 4 = Sad")

with col_features:
    with st.container(border=True):
        st.markdown("### 📋 Statistical Summary")
        st.write("Aggregated biological features extracted for model inputs.")
        
        summary_metrics = {
            "Biometric Feature": ["Mean Heart Rate", "EDA Peak Amplitude", "Skin Temp Average", "Motion Variance"],
            "Value": ["76.4 BPM", "2.48 μS", "32.15 °C", "0.04 m/s²"]
        }
        st.dataframe(pd.DataFrame(summary_metrics), use_container_width=True, hide_index=True)

# Footer placeholder for report appendix index mapping
st.markdown('<div style="text-align: center; color: #64748b; margin-top: 40px; font-size: 13px;">Figure B.6: Emotion Prediction and Analysis Interface</div>', unsafe_allow_html=True)