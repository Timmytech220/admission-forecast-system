import streamlit as st
import pandas as pd

import streamlit as st
from utils import * # Import your functions here
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("app.py")


st.title("📋 Prediction History")
if len(st.session_state.history) > 0:
    st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)
else:
    st.info("No records found.")
  
