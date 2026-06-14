import streamlit as st

st.set_page_config(page_title="Timmytech System", layout="wide")

# Professional Blue Styling
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #1e3a8a !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    .login-box { padding: 30px; border-radius: 15px; border: 2px solid #1e3a8a; }
    </style>
    """, unsafe_allow_html=True)

if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "history" not in st.session_state: st.session_state.history = []

if not st.session_state.logged_in:
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.title("🔐 Timmytech Secure Login")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if user == "Timmy" and pwd == "1234":
            st.session_state.logged_in = True
            st.rerun()
        else: st.error("Invalid Login")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

st.title("Welcome to Timmytech Dashboard")
st.success("You are logged in. Use the sidebar to navigate.")
        
