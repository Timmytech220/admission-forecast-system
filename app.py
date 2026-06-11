import streamlit as st
import joblib
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="TIMMYTECH ADMISSION FORECAST SYSTEM DASHBOARD", page_icon="🎓", layout="wide")

# ---------------- MODEL ----------------
@st.cache_resource
def load_pipeline():
    return joblib.load("final_pipeline.pkl")

pipeline = load_pipeline()

# ---------------- DASHBOARD HEADER ----------------
st.title("🎓 Admission Forecast Dashboard")
st.markdown("---")

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- LAYOUT: INPUTS ON LEFT ----------------
col_left, col_right = st.columns([1, 2])

with col_left:
    st.subheader("Student Profile")
    name = st.text_input("Full Name")
    jamb = st.slider("JAMB Score", 100, 400, 250)
    waec = st.slider("WAEC Score", 0, 100, 50)
    interview = st.slider("Interview Score", 0, 100, 50)
    predict_btn = st.button("🚀 Run Forecast", type="primary")

# ---------------- LAYOUT: RESULTS ON RIGHT ----------------
with col_right:
    if predict_btn:
        input_data = pd.DataFrame({"jamb_score": [jamb], "waec_points": [waec], "interview_score": [interview]})
        prob = float(pipeline.predict(input_data)[0])
        prob = max(0, min(1, prob))
        
        st.session_state.history.append({"name": name or "Anonymous", "prob": prob})
        
        # Display Metric
        st.metric("Admission Probability", f"{prob:.2%}")
        
        # Status Color-coding
        if prob >= 0.7:
            st.success("STATUS: QUALIFIED")
        elif prob >= 0.4:
            st.warning("STATUS: BORDERLINE")
        else:
            st.error("STATUS: NOT QUALIFIED")
            
        # Chart
        chart_data = pd.DataFrame({"Category": ["JAMB", "WAEC", "Interview"], "Score": [jamb/4, waec, interview]})
        fig = px.bar(chart_data, x="Category", y="Score", color="Score", color_continuous_scale="Viridis")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("👈 Fill in the student details and click Run Forecast to view the dashboard.")

# ---------------- FOOTER ----------------
st.markdown("---")
with st.expander("ℹ️ About this Project"):
    st.write("Professional Admission Forecast System. Powered by Machine Learning.")
    
