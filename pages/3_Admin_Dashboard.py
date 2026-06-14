import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("app.py")

st.title("⚙️ Admin Dashboard")
st.write("Bulk upload and system settings will go here.")
