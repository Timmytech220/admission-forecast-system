import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import sys
import os

# Fix path to import from root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import ALL_SUBJECTS, calculate_olevel_points, save_data

if not st.session_state.get("logged_in", False):
    st.switch_page("app.py")

# Load model (ensure final_pipeline.pkl is in root)
pipeline = joblib.load('final_pipeline.pkl')

st.title("Admission Forecast Portal")
col1, col2 = st.columns([1, 1])

with col1:
    name = st.text_input("Full Name")
    jamb = st.slider("JAMB Score", 100, 400, 250)
    
    c_eng, c_mat = st.columns(2)
    with c_eng: eng = st.selectbox("English Language", ['None', 'A1', 'B2', 'B3', 'C4', 'C5', 'C6'])
    with c_mat: mat = st.selectbox("Mathematics", ['None', 'A1', 'B2', 'B3', 'C4', 'C5', 'C6'])
    
    c3, c4, c5 = st.columns(3)
    with c3: sub3_g = st.selectbox("Subject 3 Grade", ['None', 'A1', 'B2', 'B3', 'C4', 'C5', 'C6'])
    with c4: sub4_g = st.selectbox("Subject 4 Grade", ['None', 'A1', 'B2', 'B3', 'C4', 'C5', 'C6'])
    with c5: sub5_g = st.selectbox("Subject 5 Grade", ['None', 'A1', 'B2', 'B3', 'C4', 'C5', 'C6'])

    olevel = calculate_olevel_points([eng, mat, sub3_g, sub4_g, sub5_g])
    intv = st.slider("Interview Score", 0, 100, 50)

    if st.button("Run Forecast Now", type="primary"):
        if not name.strip():
            st.error("Please enter a name.")
        else:
            input_data = pd.DataFrame({'jamb_score': [jamb], 'olevel_points': [olevel], 'interview_score': [intv]})
            prob = float(pipeline.predict(input_data)[0])
            status = 'QUALIFIED' if prob >= 0.5 else 'NOT QUALIFIED'
            st.session_state.last_result = {'name': name, 'status': status, 'prob': prob, 'jamb': jamb, 'olevel': olevel, 'intv': intv}
            save_data(name, status, prob, jamb, olevel, intv)
            st.success("Result Saved!")

with col2:
    if st.session_state.last_result:
        res = st.session_state.last_result
        st.success(f"Final Decision: {res['status']} ({res['prob']*100:.1f}%)")
        df_plot = pd.DataFrame({"Metric": ["JAMB", "O-Level", "Interview"], "Score": [res['jamb']/4, res['olevel']*10, res['intv']]})
        st.plotly_chart(px.bar(df_plot, x="Metric", y="Score", color="Score", color_continuous_scale="Blues"))
                                                       
