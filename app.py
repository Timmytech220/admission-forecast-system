import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

# --- 1. PREMIUM WHITE THEME CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #333; }
    section[data-testid="stSidebar"] { background-color: #f4f7f6; padding-top: 20px; }
    div.stButton > button { width: 100%; border-radius: 8px; background-color: #4A90E2; color: white; font-weight: bold; }
    h1, h2, h3 { color: #2C3E50; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SETUP & MODEL ---
st.set_page_config(page_title="Timmytech Admission Forecast", layout="wide")
pipeline = joblib.load("final_pipeline.pkl")

if "history" not in st.session_state: st.session_state.history = []

# --- 3. ATTRACTIVE SIDEBAR ---
with st.sidebar:
    st.title("Timmytech Console")
    st.markdown("---")
    page = st.radio("Navigation", 
                    ["📊 Dashboard", "🎯 Admission Forecast", "📋 History Log", "🖨️ Export Reports", "💬 Help & Support"], 
                    index=0)
    st.markdown("---")
    st.caption("Status: 🟢 Online")
    st.write("Developed by: **Ajayi Oluwatimileyin Daniel**")

# --- 4. PAGE CONTENT ---

if page == "📊 Dashboard":
    st.title("Welcome to Timmytech Admission Forecast System")
    st.markdown("### Empowering academic excellence through data-driven predictions.")
    st.info("Navigate using the sidebar to begin your forecasting journey.")

elif page == "🎯 Admission Forecast":
    st.title("🎯 Admission Forecast Portal")
    col1, col2 = st.columns([1, 1])
    with col1:
        name = st.text_input("Full Name")
        jamb = st.slider("JAMB Score", 100, 400, 250)
        waec = st.slider("WAEC Score", 0, 100, 50)
        intv = st.slider("Interview Score", 0, 100, 50)
        if st.button("🚀 Analyze Now"):
            input_data = pd.DataFrame({"jamb_score": [jamb], "waec_points": [waec], "interview_score": [intv]})
            prob = float(pipeline.predict(input_data)[0])
            status = "QUALIFIED" if prob >= 0.7 else "NOT QUALIFIED"
            st.session_state.history.append({"name": name, "status": status, "prob": prob, "jamb": jamb, "waec": waec, "intv": intv})
            with col2:
                st.metric("Probability", f"{prob:.1%}")
                if status == "QUALIFIED": st.success(f"STATUS: {status}")
                else: st.error(f"STATUS: {status}")
                fig = px.bar(x=["JAMB", "WAEC", "INT"], y=[jamb/4, waec, intv], color_continuous_scale="RdYlGn")
                st.plotly_chart(fig, use_container_width=True)

elif page == "📋 History Log":
    st.title("📋 Prediction History")
    st.table(pd.DataFrame(st.session_state.history))

elif page == "🖨️ Export Reports":
    st.title("🖨️ Export Results")
    for student in st.session_state.history:
        report = f"Timmytech Report\nName: {student['name']}\nStatus: {student['status']}\nProbability: {student['prob']:.1%}"
        st.download_button(f"Download Report for {student['name']}", report, f"{student['name']}_report.txt")

elif page == "💬 Help & Support":
    st.title("💬 Help Center")
    st.write("I am Ajayi Oluwatimileyin Daniel. This system predicts admission based on historical trends using Linear Regression.")
    
