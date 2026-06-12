import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

# --- 1. PREMIUM WHITE THEME & BLUE SIDEBAR CSS ---
st.set_page_config(page_title="Timmytech Admission Forecast", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    /* Deep Blue Sidebar */
    section[data-testid="stSidebar"] { background-color: #1e3a8a; color: white; padding-top: 40px; }
    section[data-testid="stSidebar"] * { color: white !important; }
    /* Button Styling */
    div.stButton > button { width: 100%; border-radius: 8px; background-color: #3b82f6; color: white; font-weight: bold; height: 3.5em; }
    /* Maximize Sidebar Spacing */
    .stRadio { padding-top: 30px; padding-bottom: 30px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MODEL & SESSION ---
pipeline = joblib.load("final_pipeline.pkl")
if "history" not in st.session_state: st.session_state.history = []

# --- 3. SPACIOUS NAVIGATION SIDEBAR ---
with st.sidebar:
    # Modern Icon
    st.image("https://cdn-icons-png.flaticon.com/512/2942/2942813.png", width=80) 
    st.markdown("## Timmytech Console")
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    # Navigation with maximum spacing
    page = st.radio("MAIN NAVIGATION", 
                    ["Dashboard", "Admission Forecast", "History Log", "Export Reports", "Help & Support"], 
                    index=0)
    
    st.markdown("<br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
    st.caption("Status: Online")
    st.write("Developed by: **Ajayi Oluwatimileyin Daniel**")

# --- 4. PAGE LOGIC ---

if page == "Dashboard":
    st.title(" Welcome to Timmytech Admission Forecast System")
    st.image("https://images.unsplash.com/photo-1552664730-d307ca884978?q=80&w=2000", use_column_width=True)
    st.markdown("### Intelligent predictive analytics for your academic journey.")

elif page == "Admission Forecast":
    st.title(" Admission Forecast Portal")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Student Profile Inputs")
        name = st.text_input("Full Name")
        jamb = st.slider("JAMB Score", 100, 400, 250)
        waec = st.slider("WAEC Score", 0, 100, 50)
        intv = st.slider("Interview Score", 0, 100, 50)
        
        if st.button(" Run Forecast Now"):
            input_data = pd.DataFrame({"jamb_score": [jamb], "waec_points": [waec], "interview_score": [intv]})
            prob = float(pipeline.predict(input_data)[0])
            status = "QUALIFIED" if prob >= 0.5 else "NOT QUALIFIED"
            st.session_state.history.append({"name": name, "status": status, "prob": prob, "jamb": jamb, "waec": waec, "intv": intv})
            
            with col2:
                st.subheader("Analysis Outcome")
                st.metric("Admission Probability", f"{prob:.1%}")
                if status == "QUALIFIED": st.success(f"FINAL DECISION: {status}")
                else: st.error(f"FINAL DECISION: {status}")
                
                fig = px.bar(x=["JAMB", "WAEC", "INT"], y=[jamb/4, waec, intv])
                st.plotly_chart(fig, use_container_width=True)

elif page == "History Log":
    st.title("📋 Prediction History")
    st.table(pd.DataFrame(st.session_state.history))

elif page == "Export Reports":
    st.title("🖨️ Export Official Reports")
    for student in st.session_state.history:
        report_text = f"TIMMYTECH OFFICIAL ADMISSION REPORT\nName: {student['name']}\nDecision: {student['status']}\nProbability: {student['prob']:.1%}\nJAMB: {student['jamb']}\nWAEC: {student['waec']}\nInterview: {student['intv']}"
        st.download_button(f"Download Report: {student['name']}", report_text, f"{student['name']}_report.txt")

elif page == "Help & Support":
    st.title("💬 Help & Support")
    st.image("https://cdn-icons-png.flaticon.com/512/3062/3062634.png", width=120)
    st.write("Timmytech is a predictive AI system for admission management. Created by **Ajayi Oluwatimileyin Daniel**.")
    st.markdown("---")
    st.write("📞 **WhatsApp/Call:** 09168090334")
    st.write("👤 **Facebook:** Ajayi oluwatimileyin Daniel")
    st.write("🎵 **TikTok:** Doctor Timmy")
