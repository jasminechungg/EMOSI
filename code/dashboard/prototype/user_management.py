import streamlit as st
import pandas as pd

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="EmoSI - User Management",
    page_icon="🧠",
    layout="wide"  # Wide layout ensures high readability for administrative data arrays
)

# --- GLOBAL STYLING (Consistent light theme with custom button overrides) ---
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

/* --- REVISED LIGHT BUTTON STYLING --- */
div.stButton > button {
    width: 100% !important;
    height: 52px !important;
    border-radius: 10px !important;
    background-color: #ffffff !important;      /* Clean white background */
    color: #16a34a !important;                 /* Vibrant green text and icons */
    border: 2px solid #16a34a !important;      /* Solid green border outline */
    font-size: 16px !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 12px rgba(22, 163, 74, 0.05); /* Soft premium green shadow */
    transition: all 0.2s ease-in-out;
}

/* Hover state: Inverts smoothly to full green with white text */
div.stButton > button:hover {
    background-color: #16a34a !important;
    color: #ffffff !important;
    border-color: #16a34a !important;
}

/* Active and focus states stay clean and legible */
div.stButton > button:active, div.stButton > button:focus {
    background-color: #15803d !important;
    color: #ffffff !important;
    border-color: #15803d !important;
}

/* Table Card Wrapper Style Adjustments */
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
    
    st.markdown("#### **User Profile**")
    st.markdown("""
    <div style="background-color: #f8fafc; padding: 15px; border-radius: 8px; border: 1px solid #e2e8f0;">
        <p style="margin: 0; font-size: 14px;">👤 <strong>Administrator:</strong> Jasmine</p>
        <p style="margin: 5px 0 0 0; font-size: 14px;">🆔 <strong>Role:</strong> Root Admin</p>
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
st.markdown('<h1 style="font-weight: 900; margin-bottom: 5px;">⚙️ Administrator Control Panel</h1>', unsafe_allow_html=True)
st.markdown('<p style="color: #64748b; font-size: 16px; margin-bottom: 25px;">Manage platform account authentications, privileges, and system-level credential records.</p>', unsafe_allow_html=True)

# --- REGISTRATION & CONTROL CONTROL BLOCK ---
with st.container(border=True):
    st.markdown("### 🔍 Search & Filter Accounts")
    col_search, col_role, col_status = st.columns([2, 1, 1])
    
    with col_search:
        st.text_input("Search accounts by name or email query", placeholder="e.g., Nizamullah")
    with col_role:
        st.selectbox("Access Privilege Tier", ["All Roles", "Administrator", "Clinician"])
    with col_status:
        st.selectbox("Account Status", ["All States", "Active", "Pending", "Deactivated"])

st.write("")

# --- USER INFRASTRUCTURE RECORD GENERATION ---
# Mocking credential registries aligned with your documented academic team context
user_registry = {
    "User ID": ["USR-1002", "USR-1005", "USR-1008", "USR-1011", "USR-1014"],
    "Full Name": ["Jasmine Binti Mohd Shaiful Adli Chung", "Nizamullah Bin Corporate", "Fatih Ahmed", "Fazrul Edlin", "Dr Azman Ab Malik"],
    "Email Address": ["jasmine@um.edu.my", "nizamullah@um.edu.my", "fatih@um.edu.my", "fazrul@um.edu.my", "azman@um.edu.my"],
    "Assigned Role": ["Administrator", "Clinician", "Clinician", "Clinician", "Administrator"],
    "Account Status": ["Active", "Active", "Active", "Active", "Active"],
    "Last Login Date": ["21 May 2026", "20 May 2026", "19 May 2026", "18 May 2026", "15 May 2026"]
}

df_users = pd.DataFrame(user_registry)

with st.container(border=True):
    st.markdown("### 👥 Verified System Account Profiles")
    st.write("Highlight an index field row below to perform configuration adjustment modifications.")
    
    st.dataframe(
        df_users,
        use_container_width=True,
        hide_index=True,
        column_config={
            "User ID": st.column_config.TextColumn("User ID", help="Primary key identifier in user registry data module"),
            "Assigned Role": st.column_config.TextColumn("Role Allocation Status")
        }
    )

st.write("")

# --- ACTION ELEMENTS ROW (Light Premium Outlined Buttons) ---
col_spacer, col_btn_add, col_btn_edit, col_btn_del = st.columns([1, 1, 1, 1])

with col_btn_add:
    st.button("➕ Create New Account", key="admin_add_user", use_container_width=True)

with col_btn_edit:
    st.button("✏️ Modify Permissions", key="admin_edit_user", use_container_width=True)

with col_btn_del:
    st.button("🗑️ Deactivate Selected", key="admin_del_user", use_container_width=True)

# Footer placeholder for report appendix index mapping
st.markdown('<div style="text-align: center; color: #64748b; margin-top: 40px; font-size: 13px;">Figure B.7: Administrator User Management Interface</div>', unsafe_allow_html=True)