
import streamlit as st
import pandas as pd
import plotly.express as px
import joblib


import streamlit as st
from utils import * # Import your functions here
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("app.py")
    
from app import ALL_SUBJECTS, calculate_olevel_points, save_data

# Load your model
pipeline = joblib.load("final_pipeline.pkl")

st.title("Admission Forecast Portal")
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Student Profile Inputs")
    name = st.text_input("Full Name")
    jamb = st.slider("JAMB Score", 100, 400, 250)
    
    st.write("**Select your 5 core/required subjects:**")
    c_eng, c_mat = st.columns(2)
    with c_eng: eng = st.selectbox("English Language", ['None', 'A1', 'B2', 'B3', 'C4', 'C5', 'C6'])
    with c_mat: mat = st.selectbox("Mathematics", ['None', 'A1', 'B2', 'B3', 'C4', 'C5', 'C6'])
    
    c3, c4, c5 = st.columns(3)
    with c3: 
        sub3_name = st.selectbox("Subject 3", ALL_SUBJECTS)
        sub3_grade = st.selectbox("Grade 3", ['None', 'A1', 'B2', 'B3', 'C4', 'C5', 'C6'])
    with c4: 
        sub4_name = st.selectbox("Subject 4", ALL_SUBJECTS)
        sub4_grade = st.selectbox("Grade 4", ['None', 'A1', 'B2', 'B3', 'C4', 'C5', 'C6'])
    with c5: 
        sub5_name = st.selectbox("Subject 5", ALL_SUBJECTS)
        sub5_grade = st.selectbox("Grade 5", ['None', 'A1', 'B2', 'B3', 'C4', 'C5', 'C6'])
    
    olevel = calculate_olevel_points([eng, mat, sub3_grade, sub4_grade, sub5_grade])
    st.write("---")
    st.success(f"Total O-Level Points: {olevel}")
    intv = st.slider("Interview Score", 0, 100, 50)
    
    if st.button("Run Forecast Now", type="primary"):
        if not name.strip(): st.error("Please enter a name.")
        else:
            input_data = pd.DataFrame({"jamb_score": [jamb], "waec_points": [olevel], "interview_score": [intv]})
            prob = float(pipeline.predict(input_data)[0])
            status = f"{'QUALIFIED' if prob >= 0.5 else 'NOT QUALIFIED'} ({prob:.1%})"
            save_data(name, status, f"{prob:.1%}", str(jamb), str(olevel), str(intv))
            st.session_state.last_result = {"name": name, "status": status, "prob": prob, "jamb": jamb, "olevel": olevel, "intv": intv}
            st.session_state.history.append(st.session_state.last_result)
            st.success("Result saved!")

with col2:
    if 'last_result' in st.session_state and st.session_state.last_result:
        res = st.session_state.last_result
        st.success(f"FINAL DECISION: {res['status']}")
        df_plot = pd.DataFrame({"Metric": ["JAMB", "O-Level", "INT"], "Score": [res['jamb']/4, res['olevel'], res['intv']]})
        fig = px.bar(df_plot, x="Metric", y="Score", color="Score", color_continuous_scale="Blues")
        st.plotly_chart(fig, use_container_width=True)
  
