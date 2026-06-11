import streamlit as st
import joblib
import pandas as pd
import plotly.express as px

# 1. SETUP: Wide layout for a dashboard feel
st.set_page_config(page_title="Admission Dashboard", layout="wide")

# 2. MODEL
@st.cache_resource
def load_pipeline():
    return joblib.load("final_pipeline.pkl")

pipeline = load_pipeline()

# 3. TITLE
st.title("🎓 Admission Analytics Console")

# 4. DASHBOARD GRID
col_input, col_kpi, col_chart = st.columns([1, 1, 2])

# LEFT: INPUTS
with col_input:
    st.subheader("Student Profile")
    name = st.text_input("Full Name")
    jamb = st.slider("JAMB", 100, 400, 250)
    waec = st.slider("WAEC", 0, 100, 50)
    interview = st.slider("Interview", 0, 100, 50)
    predict_btn = st.button("🚀 Analyze", type="primary")

# MIDDLE: KPI CARDS (Like the Salesforce image)
with col_kpi:
    st.subheader("Key Metrics")
    if predict_btn:
        input_data = pd.DataFrame({"jamb_score": [jamb], "waec_points": [waec], "interview_score": [interview]})
        prob = float(pipeline.predict(input_data)[0])
        
        # Displaying the "Card" style
        st.metric("Admission Probability", f"{prob:.1%}")
        if prob >= 0.7: st.success("STATUS: QUALIFIED")
        elif prob >= 0.4: st.warning("STATUS: BORDERLINE")
        else: st.error("STATUS: NOT QUALIFIED")
    else:
        st.info("Run analysis to see metrics.")

# RIGHT: CHARTS
with col_chart:
    st.subheader("Performance Trends")
    if predict_btn:
        chart_data = pd.DataFrame({"Cat": ["JAMB", "WAEC", "INT"], "Val": [jamb/4, waec, interview]})
        fig = px.bar(chart_data, x="Cat", y="Val", color="Val", color_continuous_scale="RdYlGn")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Visual breakdown will appear here after analysis.")

# 5. SIDEBAR HISTORY
with st.sidebar:
    st.header("🕒 Prediction Log")
    if "history" not in st.session_state: st.session_state.history = []
    for item in reversed(st.session_state.history):
        st.write(f"**{item['name']}**: {item['prob']:.1%}")
