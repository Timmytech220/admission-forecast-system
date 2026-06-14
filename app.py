import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- GLOBAL VARS ---
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

# --- AUTHENTICATION GATEKEEPER ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "history" not in st.session_state: st.session_state.history = []

if not st.session_state.logged_in:
    st.title("🔐 Timmytech Secure Access")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if user == "Timmy" and pwd == "1234":
            st.session_state.logged_in = True
            st.rerun()
        else: st.error("Invalid credentials!")
    st.stop() # Stops execution so pages don't load until logged in

# --- DASHBOARD (This only shows if logged_in is True) ---
st.title("Welcome to Timmytech Admission Forecast System")
# Streamlit will now automatically show the pages in the sidebar because they are in the /pages folder!

