import streamlit as st
import sys
import os

# 1. Path Fix: This allows the page to "see" your utils.py file
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 2. Security Gate: If not logged in, force them back to the login page
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("app.py")
    
