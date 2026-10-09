import streamlit as st
from aws_dynamodb import register_user, login_user


st.set_page_config(
    page_title="EmoSI Web Platform",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded"
)


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


if "user" not in st.session_state:
    st.session_state.user = None


if "signup_success" not in st.session_state:
    st.session_state.signup_success = False




st.markdown("""
<style>
.stApp {
    background-color: #f4f7fb;
    color: #000000;
}


.block-container {
    max-width: 950px;
    padding-top: 2rem;
}


header, footer {
    visibility: hidden;
}


h1, h2, h3, p, label {
    color: #000000 !important;
}


.title {
    text-align: center;
    font-size: 54px;
    font-weight: 900;
    color: #000000;
}


.subtitle {
    text-align: center;
    font-size: 17px;
    color: #1f2937;
    margin-bottom: 45px;
}


.stRadio label {
    color: #000000 !important;
    font-weight: 700 !important;
}


.stTextInput input,
.stSelectbox div {
    border-radius: 10px;
    background-color: white !important;
    color: #000000 !important;
}


.stButton > button {
    width: 100%;
    height: 58px;
    border-radius: 10px;
    border: none;
    background-color: #16a34a;
    color: white;
    font-size: 19px;
    font-weight: 800;
}


.stButton > button:hover {
    background-color: #15803d;
    color: white;
}


[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: white;
    border-radius: 18px;
    padding: 35px;
    box-shadow: 0 15px 35px rgba(15, 23, 42, 0.08);
}
</style>
""", unsafe_allow_html=True)




if st.session_state.logged_in and st.session_state.user:
    user = st.session_state.user


    if user.get("role") == "admin":
        st.switch_page("pages/Admin_Dashboard.py")
    else:
        st.switch_page("pages/Dashboard_home.py")




st.markdown('<div class="title">🧠 EmoSI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Wearable IoT and Machine Learning-Based Emotional Monitoring Web Platform</div>',
    unsafe_allow_html=True
)


page = st.radio(
    "Select Page",
    ["Login", "Sign Up"],
    index=0,
    horizontal=True,
    label_visibility="collapsed"
)


st.write("")


with st.container(border=True):


    if page == "Login":
        st.header("Login to Your Account")
        st.write("Welcome back! Please enter your details to continue.")


        if st.session_state.signup_success:
            st.success("✅ Account created successfully. Please log in.")
            st.session_state.signup_success = False


        email = st.text_input("Email", placeholder="Enter your email address")
        password = st.text_input("Password", placeholder="Enter your password", type="password")


        if st.button("Login", use_container_width=True):
            if email == "" or password == "":
                st.error("Please enter both email and password.")
            else:
                user, message = login_user(email, password)


                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = user


                    if user.get("role") == "admin":
                        st.switch_page("pages/Admin_Dashboard.py")
                    else:
                        st.switch_page("pages/Dashboard_home.py")
                else:
                    st.error(message)


    else:
        st.header("Create New Account")
        st.write("Register a new account for the Emotional Monitoring System.")


        full_name = st.text_input("Full Name", placeholder="Enter your full name")
        email = st.text_input("Email", placeholder="Enter your email address")
        password = st.text_input("Password", placeholder="Create your password", type="password")
        confirm_password = st.text_input("Confirm Password", placeholder="Re-enter your password", type="password")


        role = st.selectbox(
            "Role",
            ["clinician", "admin"]
        )


        if st.button("Create Account", use_container_width=True):
            if full_name == "" or email == "" or password == "" or confirm_password == "":
                st.error("Please complete all required fields.")
            elif password != confirm_password:
                st.error("Password and confirm password do not match.")
            else:
                user, message = register_user(
                    full_name=full_name,
                    email=email,
                    password=password,
                    role=role
                )


                if user:
                    st.session_state.signup_success = True
                    st.rerun()
                else:
                    st.error(message)

