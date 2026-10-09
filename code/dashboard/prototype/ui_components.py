import streamlit as st


def apply_global_style():
    st.markdown("""
    <style>
    .stApp {
        background-color: #f4f7fb;
        color: #000000;
    }

    header, footer {
        visibility: hidden;
    }

    h1, h2, h3, p, label, span {
        color: #000000 !important;
    }

    [data-testid="stMetricValue"] {
        color: #111827 !important;
        font-weight: 800 !important;
    }

    [data-testid="stMetricLabel"] {
        color: #475569 !important;
        font-weight: 600 !important;
    }

    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0;
    }

    [data-testid="stSidebar"] * {
        color: #000000 !important;
    }

    div.stButton > button {
        width: 100% !important;
        height: 45px !important;
        border-radius: 10px !important;
        background-color: #ffffff !important;
        color: #16a34a !important;
        border: 1.5px solid #16a34a !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        margin-bottom: 5px !important;
    }

    div.stButton > button:hover {
        background-color: #16a34a !important;
        color: #ffffff !important;
        border-color: #16a34a !important;
    }

    .profile-box {
        background-color: #f8fafc;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
    }

    .admin-box {
        background-color: #eef2ff;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #c7d2fe;
    }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar(active_page="Dashboard Home"):
    user = st.session_state.get("user", {})
    full_name = user.get("full_name", "Unknown User")
    raw_role = user.get("role", "clinician")
    role = raw_role.title()

    if raw_role == "admin":
        render_admin_sidebar(full_name, role)
    else:
        render_clinician_sidebar(full_name, role)


def render_clinician_sidebar(full_name, role):
    with st.sidebar:
        st.markdown("### 🧠 EmoSI Clinician Portal")
        st.markdown("---")

        st.markdown("#### **Clinician Profile**")
        st.markdown(f"""
        <div class="profile-box">
            <p style="margin: 0; font-size: 14px;">👤 <strong>{full_name}</strong></p>
            <p style="margin: 5px 0 0 0; font-size: 14px;">🆔 <strong>Role:</strong> {role}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### **Clinician Navigation**")

        if st.button("🏠 Dashboard Home", use_container_width=True):
            st.switch_page("pages/Dashboard_home.py")

        if st.button("👥 Patient Management", use_container_width=True):
            st.switch_page("pages/Patient_Management.py")

        if st.button("📅 Appointment Scheduling", use_container_width=True):
            st.switch_page("pages/Appointment_Scheduling.py")

        if st.button("🩺 Session Management", use_container_width=True):
            st.switch_page("pages/Session_Management.py")

        if st.button("📜 Historical Sessions", use_container_width=True):
            st.switch_page("pages/Historical_Sessions.py")

        st.markdown("---")
        st.markdown("#### **System Status**")
        st.success("🟢 **AWS Connection:** Active")
        st.success("🟢 **Data Stream:** Synced")

        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.switch_page("main.py")


def render_admin_sidebar(full_name, role):
    with st.sidebar:
        st.markdown("### ⚙️ EmoSI Admin Portal")
        st.markdown("---")

        st.markdown("#### **Admin Profile**")
        st.markdown(f"""
        <div class="admin-box">
            <p style="margin: 0; font-size: 14px;">👤 <strong>{full_name}</strong></p>
            <p style="margin: 5px 0 0 0; font-size: 14px;">🛡️ <strong>Role:</strong> {role}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### **Admin Navigation**")

        if st.button("📊 Admin Dashboard", use_container_width=True):
            st.switch_page("pages/Admin_Dashboard.py")

        if st.button("⚙️ User Management", use_container_width=True):
            st.switch_page("pages/User_Management.py")

        st.markdown("---")
        st.markdown("#### **Admin Access**")
        st.info("Admin access is limited to account and system overview functions.")

        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.switch_page("main.py")