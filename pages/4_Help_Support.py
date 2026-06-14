import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("app.py")

st.title("🆘 Help & Support Center")
st.write("Developed by: **Ajay Oluwatimileyin Daniel**")
st.write("📞 **WhatsApp:** 09168090334")
