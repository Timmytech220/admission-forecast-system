import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

# 1. SETUP: Wide layout
st.set_page_config(page_title="Admission Analytics Console", page_icon="🎓", layout="wide")

# 2. MODEL LOADING
@st.cache_resource
def load_pipeline():
    return joblib.load("final_pipeline.pkl")

pipeline = load_pipeline()

# 3. INITIALIZATION
if "history" not in st.session_state:
    st.session_state.history = []

# 4. SIDEBAR NAVIGATION
with st.sidebar:
    st.title("🎓 Admission Console")
    # Using index=0 to make "Dashboard" the default view
    page = st.radio("Navigation", ["Dashboard", "Forecast", "History", "Download", "Help/Docs"], index=0)
    
    st.markdown("---")
    st.subheader("System Performance")
    st.caption("Model: Linear Regression")
    st.caption("Status: 🟢 Online")
    st.caption(f"Total Forecasts: {len(st.session_state.history)}")
    st.markdown("---")
    st.write("Developed by: [Your Name]")

# 5. PAGE LOGIC (Standardized for Desktop)

# DASHBOARD PAGE
if page == "Dashboard":
    st.title("📊 Welcome to the Analytics Dashboard")
    st.markdown("This system provides real-time predictive insights for institutional admission planning.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://images.unsplash.com/photo-1523240795612-9a054b0db644?q=80&w=600", caption="Predictive Analytics Engine")
    with col2:
        st.success("System is fully operational.")
        st.write("Use the 'Forecast' tab in the sidebar to begin analyzing student profiles.")

# FORECAST PAGE (Includes all your specific inputs)
elif page == "Forecast":
    st.title("🚀 Admission Forecast Engine")
    col_left, col_right = st.columns([1, 2])
    
    with col_left:
        st.subheader("Student Profile Inputs")
        name = st.text_input("Full Name", placeholder="Enter student name...")
        jamb = st.slider("JAMB Score", 100, 400, 250)
        waec = st.slider("WAEC Score", 0, 100, 50)
        intv = st.slider("Interview Score", 0, 100, 50)
        predict_btn = st.button("🚀 Analyze Now", type="primary", use_container_width=True)
    
    with col_right:
        if predict_btn:
            # Model execution
            input_data = pd.DataFrame({"jamb_score": [jamb], "waec_points": [waec], "interview_score": [intv]})
            prob = float(pipeline.predict(input_data)[0])
            st.session_state.history.append({"name": name or "Anonymous", "prob": prob})
            
            # KPI Layout
            k1, k2 = st.columns(2)
            k1.metric("Admission Probability", f"{prob:.1%}")
            if prob >= 0.7: k2.success("STATUS: QUALIFIED")
            elif prob >= 0.4: k2.warning("STATUS: BORDERLINE")
            else: k2.error("STATUS: NOT QUALIFIED")
            
            # Insights & Chart
            st.subheader("💡 Model Insight")
            st.info("The model indicates high potential." if prob >= 0.7 else "Further preparation recommended.")
            
            fig = px.bar(pd.DataFrame({"Cat": ["JAMB", "WAEC", "INT"], "Val": [jamb/4, waec, intv]}), 
                         x="Cat", y="Val", color="Val", color_continuous_scale="RdYlGn")
            st.plotly_chart(fig, use_container_width=True)

# HISTORY PAGE
elif page == "History":
    st.title("🕒 Prediction Log")
    if st.session_state.history:
        st.table(pd.DataFrame(st.session_state.history))
    else:
        st.info("No prediction history recorded yet.")

# DOWNLOAD PAGE
elif page == "Download":
    st.title("📥 Export Reports")
    st.write("Click below to download your full historical analysis report.")
    if st.session_state.history:
        st.download_button("Download History as CSV", data=pd.DataFrame(st.session_state.history).to_csv(), file_name="history.csv")
    else:
        st.warning("No data available to download.")

# HELP/DOCS PAGE
elif page == "Help/Docs":
    st.title("📚 User Guide & Documentation")
    st.markdown("""
    ### System Architecture
    This system implements a **Linear Regression** model to predict admission probabilities.
    
    * **JAMB Score:** Weighted contribution to the admission outcome.
    * **WAEC Score:** Represents O'Level performance.
    * **Interview Score:** Qualitative assessment metric.
    
    For support, please contact the system administrator.
    """)
    
