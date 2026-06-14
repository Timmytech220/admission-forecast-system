import streamlit as st

import streamlit as st
from utils import * # Import your functions here
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("app.py")

st.title("💬 Help & Support Center")
st.write("Developed by: **Ajayi Oluwatimileyin Daniel**")
st.write("📞 **WhatsApp:** 09168090334")

