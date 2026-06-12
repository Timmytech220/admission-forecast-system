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
if "last_result" not in st.session_state: st.session_state.last_result = None

# --- 3. SPACIOUS NAVIGATION SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2942/2942813.png", width=80) 
    st.markdown("## Timmytech Console")
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    page = st.radio("MAIN NAVIGATION", 
                    ["Dashboard", "Admission Forecast", "History Log", "Export Reports", "Help & Support"], 
                    index=0)
    
    st.markdown("<br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
    st.caption("Status: Online")
    st.write("Developed by: **Ajayi Oluwatimileyin Daniel**")

# --- 4. PAGE LOGIC ---

if page == "Dashboard":
    st.title("Welcome to Timmytech Admission Forecast System")
    st.image("https://images.unsplash.com/photo-1552664730-d307ca884978?q=80&w=2000", use_column_width=True)
    
    # --- ANALYTICS SUMMARY ---
    if len(st.session_state.history) > 0:
        df_hist = pd.DataFrame(st.session_state.history)
        
        st.subheader("System Analytics Overview")
        col1, col2, col3 = st.columns(3)
        
        # 1. Total Applicants
        col1.metric("Total Applicants", len(df_hist))
        
        # 2. Success Rate
        qualified_count = len(df_hist[df_hist['status'] == "QUALIFIED"])
        success_rate = (qualified_count / len(df_hist)) * 100
        col2.metric("Success Rate", f"{success_rate:.1f}%")
        
        # 3. Average Probability
        avg_prob = df_hist['prob'].mean() * 100
        col3.metric("Avg. Admission Prob.", f"{avg_prob:.1f}%")
        
        st.markdown("---")
    else:
        st.info("Run your first forecast in the 'Admission Forecast' tab to see analytics here!")
        
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
            
            # Store in state
            st.session_state.last_result = {"name": name, "status": status, "prob": prob, "jamb": jamb, "waec": waec, "intv": intv}
            st.session_state.history.append(st.session_state.last_result)
            
    with col2:
        if st.session_state.last_result:
            res = st.session_state.last_result
            st.subheader("Analysis Outcome")
            st.metric("Admission Probability", f"{res['prob']:.1%}")
            if res['status'] == "QUALIFIED": st.success(f"FINAL DECISION: {res['status']}")
            else: st.error(f"FINAL DECISION: {res['status']}")
            
            fig = px.bar(x=["JAMB", "WAEC", "INT"], y=[res['jamb']/4, res['waec'], res['intv']])
            st.plotly_chart(fig, use_container_width=True)

elif page == "History Log":
    st.title("📋 Prediction History")
    if st.session_state.history:
        st.table(pd.DataFrame(st.session_state.history))
    else:
        st.write("No records yet.")

elif page == "Export Reports":
    st.title("🖨️ Export Official Reports")
    if not st.session_state.history:
        st.write("No reports available to export.")
    else:
        for i, student in enumerate(st.session_state.history):
            report_text = f"TIMMYTECH OFFICIAL ADMISSION REPORT\nName: {student['name']}\nDecision: {student['status']}\nProbability: {student['prob']:.1%}\nJAMB: {student['jamb']}\nWAEC: {student['waec']}\nInterview: {student['intv']}"
            st.download_button(
                label=f"Download Report: {student['name']}", 
                data=report_text, 
                file_name=f"{student['name']}_report.txt",
                key=f"dl_{i}"
            )

elif page == "Help & Support":
    st.title("💬 Help & Support")
    st.image("https://cdn-icons-png.flaticon.com/512/3062/3062634.png", width=120)
    st.write("Timmytech is a predictive AI system for admission management. Created by **Ajayi Oluwatimileyin Daniel**.")
    st.markdown("---")
    st.write("📞 **WhatsApp/Call:** 09168090334")
    st.write("👤 **Facebook:** Ajayi oluwatimileyin Daniel")
    st.write("🎵 **TikTok:** Doctor Timmy")
