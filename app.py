import streamlit as st
import pandas as pd
import joblib
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- CONFIG & GLOBAL VARS ---
st.set_page_config(page_title="Timmytech Admission Forecast", layout="wide")
ALL_SUBJECTS = ['None', 'Biology', 'Chemistry', 'Physics', 'Accounting', 'Economics', 
                'Government', 'CRS/IRS', 'Literature-in-English', 'Agricultural Science', 
                'Commerce', 'Geography', 'History', 'Further Mathematics', 'Computer Science',
                'Islamic Studies', 'Yoruba', 'Igbo', 'Hausa', 'Civic Education', 
                'Technical Drawing', 'Physical Education', 'Food and Nutrition', 
                'Visual Art', 'Music', 'French']

def calculate_olevel_points(grades):
    grade_map = {'A1': 6, 'B2': 5, 'B3': 4, 'C4': 3, 'C5': 2, 'C6': 1, 'None': 0}
    return sum([grade_map.get(grade, 0) for grade in grades])

def save_data(name, status, prob, jamb, olevel, intv):
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(dict(st.secrets["gcp_service_account"]), scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key("1mmG9VbogSnTLmLwWpOmVa3L1CWCCf5EcZmvJCAGCUp4")
    sheet = spreadsheet.get_worksheet(0) 
    sheet.append_row([name, status, prob, jamb, olevel, intv])

# --- STYLING & AUTH ---
st.markdown("""<style>.login-container { padding: 40px; border-radius: 20px; background: linear-gradient(180deg, #ffffff 0%, #eef2ff 100%); border: 1px solid #1e3a8a; box-shadow: 0px 10px 30px rgba(0,0,0,0.1); }</style>""", unsafe_allow_html=True)

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
    st.stop()

# --- DASHBOARD LOGIC (Remains on main page) ---
st.title("Welcome to Timmytech Admission Forecast System")
st.image("https://images.unsplash.com/photo-1552664730-d307ca884978?q=80&w=2000", use_container_width=True)
if len(st.session_state.history) > 0:
    df = pd.DataFrame(st.session_state.history)
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Forecasts", len(df))
    c2.metric("Success Rate", f"{(len(df[df['status'].str.contains('QUALIFIED')])/len(df))*100:.1f}%")
    c3.metric("Avg Probability", f"{df['prob'].mean()*100:.1f}%")
    
