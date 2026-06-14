import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- CONFIG & STYLING ---
st.set_page_config(page_title="Timmytech Admission Forecast", layout="wide")
st.markdown("""
    <style>
    section[data-testid="stSidebar"] { background-color: #1e3a8a !important; color: white !important; }
    section[data-testid="stSidebar"] * { color: white !important; }
    .login-container { 
        padding: 40px; 
        border-radius: 20px; 
        background: linear-gradient(180deg, #ffffff 0%, #eef2ff 100%); 
        border: 1px solid #1e3a8a;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.1);
    }
    h1, h2 { color: #1e3a8a !important; }
    </style>
    """, unsafe_allow_html=True)

# --- AUTHENTICATION ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "history" not in st.session_state: st.session_state.history = []

if not st.session_state.logged_in:
    c1, mid, c3 = st.columns([1, 1.5, 1])
    with mid:
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>🔐 Timmytech Secure Access</h2>", unsafe_allow_html=True)
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            if user == "Timmy" and pwd == "1234":
                st.session_state.logged_in = True
                st.rerun()
            else: st.error("Invalid credentials!")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop() # Stops execution so pages only load for logged-in users

# --- DASHBOARD ---
st.title("Welcome to Timmytech Admission Forecast System")
st.image("https://images.unsplash.com/photo-1552664730-d307ca884978?q=80&w=2000", use_container_width=True)

if len(st.session_state.history) > 0:
    df = pd.DataFrame(st.session_state.history)
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Forecasts", len(df))
    # Add back your metrics here...
  
