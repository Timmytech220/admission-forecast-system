import streamlit as st
import pandas as pd

st.title("📋 Prediction History")
if len(st.session_state.history) > 0:
    st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)
else:
    st.info("No records found.")
  
