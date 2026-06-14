import streamlit as st
import streamlit as st
from utils import * # Import your functions here
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("app.py")

st.title("⚙️ Admin Dashboard")
st.write("Bulk upload and system settings will go here.")

