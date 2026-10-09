import streamlit as st
import numpy as np
import pandas as pd

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="EmoSI - Real-Time Signals",
    page_icon="🧠",
    layout="wide"  # Wide layout maximizes graph readability for clinical monitoring
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

/* Section Card Wrapper */
.graph-container {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(15, 23, 42, 0.04);
    border: 1px solid #e2e8f0;
    margin-bottom: 20px;
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
st.markdown('<h1 style="font-weight: 900; margin-bottom: 5px;">📈 Real-Time Physiological Signals</h1>', unsafe_allow_html=True)
st.markdown('<p style="color: #64748b; font-size: 16px; margin-bottom: 25px;">High-resolution visualization window displaying raw multi-modal biometrics captured from the EmotiBit platform.</p>', unsafe_allow_html=True)

# --- MOCK SIGNAL GENERATION (Aligned with your 5-layer IoT hardware parameters) ---
# Simulating continuous structured observations
time_index = np.linspace(0, 10, 50)

# 1. Multi-wavelength PPG Optical Channels
ppg_data = pd.DataFrame({
    'PPG_Green': 75 + np.sin(time_index * 2) * 2 + np.random.randn(50) * 0.3,
    'PPG_Red': 74 + np.sin(time_index * 2 + 0.5) * 1.8 + np.random.randn(50) * 0.3,
    'PPG_Infrared': 76 + np.sin(time_index * 2 - 0.5) * 2.2 + np.random.randn(50) * 0.3
})

# 2. Electrodermal Activity Modalities (Tonic/Phasic components)
eda_data = pd.DataFrame({
    'EDA (Total Conductance)': 2.48 + np.cumsum(np.random.randn(50) * 0.01),
    'EDL (Electrodermal Level)': 2.41 + np.linspace(0, 0.05, 50)
})

# 3. Core Thermal Signals
temp_data = pd.DataFrame({
    'TEMP_1 (Skin Temperature)': 32.1 + np.random.randn(50) * 0.02,
    'THERMOPILE (Ambient/Object)': 31.8 + np.random.randn(50) * 0.04
})

# 4. 9-Axis IMU Motion Data
motion_data = pd.DataFrame({
    'ACC_X': 0.02 + np.random.randn(50) * 0.05,
    'ACC_Y': -0.97 + np.sin(time_index * 0.5) * 0.1 + np.random.randn(50) * 0.05,
    'ACC_Z': 0.15 + np.random.randn(50) * 0.05
})

# --- GRID ARRAY FOR SCREENSHOT GRAPH PANELS ---
col_left, col_right = st.columns(2)

with col_left:
    # Panel A: Photoplethysmography Channels
    with st.container(border=True):
        st.markdown('### ❤️ Photoplethysmography (PPG)', unsafe_allow_html=True)
        st.write("Multi-wavelength optical metrics tracking blood volume pulse variations.")
        st.line_chart(ppg_data, height=220)
        
    # Panel B: Thermal Modalities
    with st.container(border=True):
        st.markdown('### 🌡️ Temperature Channels', unsafe_allow_html=True)
        st.write("Real-time skin conduction temperature matching baseline thermopile levels.")
        st.line_chart(temp_data, height=220)

with col_right:
    # Panel C: Electrodermal Arousal Activity
    with st.container(border=True):
        st.markdown('### ⚡ Electrodermal Activity (EDA)', unsafe_allow_html=True)
        st.write("Autonomic nervous system arousal mapping skin conductance variations.")
        st.line_chart(eda_data, height=220)
        
    # Panel D: Accelerometer Movement Coordinates
    with st.container(border=True):
        st.markdown('### 跑 Inertial Motion (ACC)', unsafe_allow_html=True)
        st.write("Tri-axial tracking coordinates isolating physical artifacts or restless fidgeting behavior.")
        st.line_chart(motion_data, height=220)

# Footer placeholder for report appendix index mapping
st.markdown('<div style="text-align: center; color: #64748b; margin-top: 40px; font-size: 13px;">Figure B.4: Real-Time Physiological Signal Visualization Interface</div>', unsafe_allow_html=True)