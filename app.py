import streamlit as st
import joblib
import pandas as pd
import plotly.express as px

# 1. SETUP: Wide layout
st.set_page_config(page_title="Admission forecast system ", page_icon="🎓", layout="wide")

# 2. MODEL LOADING
@st.cache_resource
def load_pipeline():
    return joblib.load("final_pipeline.pkl")

pipeline = load_pipeline()

# 3. SIDEBAR: History
with st.sidebar:
    st.header("🕒 Prediction Log")
    if "history" not in st.session_state: st.session_state.history = []
    for item in reversed(st.session_state.history):
        st.write(f"**{item['name']}**: {item['prob']:.1%}")

# 4. MAIN LAYOUT
st.title("🎓 Admission Analytics Console")
st.markdown("---")

col_left, col_right = st.columns([1, 2])

# LEFT: INPUTS
with col_left:
    st.subheader("Student Profile")
    name = st.text_input("Full Name", placeholder="Enter student name...")
    jamb = st.slider("JAMB Score", 100, 400, 250)
    waec = st.slider("WAEC Score", 0, 100, 50)
    interview = st.slider("Interview Score", 0, 100, 50)
    predict_btn = st.button("🚀 Analyze Now", type="primary", use_container_width=True)

# RIGHT: RESULTS
with col_right:
    if predict_btn:
        input_data = pd.DataFrame({"jamb_score": [jamb], "waec_points": [waec], "interview_score": [interview]})
        prob = float(pipeline.predict(input_data)[0])
        st.session_state.history.append({"name": name or "Anonymous", "prob": prob})
        
        # KPI Cards
        kpi1, kpi2 = st.columns(2)
        kpi1.metric("Admission Probability", f"{prob:.1%}")
        
        if prob >= 0.7: kpi2.success("STATUS: QUALIFIED")
        elif prob >= 0.4: kpi2.warning("STATUS: BORDERLINE")
        else: kpi2.error("STATUS: NOT QUALIFIED")
        
        st.markdown("---")
        
        # SUGGESTION 1: DATA INSIGHTS
        st.subheader("💡 Model Insight")
        if prob >= 0.7:
            st.info("The model indicates a high probability of admission. Your composite score is strong.")
        elif prob >= 0.4:
            st.info("Borderline result. Improving your JAMB/WAEC scores will significantly boost your chances.")
        else:
            st.info("Low probability. We recommend reviewing the admission criteria or improving O'Level performance.")
        
        # SUGGESTION 2: DOWNLOAD REPORT
        report_text = f"Admission Report for {name or 'Anonymous'}\nProbability: {prob:.2%}\nJAMB: {jamb}, WAEC: {waec}, Interview: {interview}"
        st.download_button(label="📥 Download Report", data=report_text, file_name="admission_report.txt", mime="text/plain")
        
        # Performance Chart
        st.subheader("Performance Trends")
        chart_data = pd.DataFrame({"Cat": ["JAMB", "WAEC", "INT"], "Val": [jamb/4, waec, interview]})
        fig = px.bar(chart_data, x="Cat", y="Val", color="Val", color_continuous_scale="RdYlGn")
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("👈 Enter details on the left and click 'Analyze Now' to generate your report.")
