import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

# --- 1. PREMIUM WHITE THEME & STYLING ---
st.set_page_config(page_title="Timmytech Admission Forecast", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    section[data-testid="stSidebar"] { background-color: #f8f9fa; }
    div.stButton > button { width: 100%; border-radius: 10px; background-color: #6366f1; color: white; font-weight: bold; height: 3.5em; }
    .css-1544g2n { padding-top: 2rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MODEL LOADING ---
pipeline = joblib.load("final_pipeline.pkl")
if "history" not in st.session_state: st.session_state.history = []

# --- 3. ATTRACTIVE SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135768.png", width=80)
    st.title("Timmytech Console")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Navigation with spacing
    page = st.radio("Navigation", 
                    ["📊 Dashboard", "🎯 Admission Forecast", "📋 History Log", "🖨️ Export Reports", "💬 Help & Support"], 
                    index=0)
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    st.caption("System Status: 🟢 Online")
    st.write("Developed by: **Ajayi Oluwatimileyin Daniel**")

# --- 4. PAGE LOGIC ---

if page == "📊 Dashboard":
    st.title("🚀 Welcome to Timmytech Admission Forecast System")
    st.subheader("Your Future, Predicted with Precision.")
    st.image("https://images.unsplash.com/photo-1552664730-d307ca884978?q=80&w=2000", use_column_width=True)
    st.markdown("### Experience the future of intelligent admission forecasting.")

elif page == "🎯 Admission Forecast":
    st.title("🎯 Admission Forecast Portal")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Student Profile Inputs")
        name = st.text_input("Full Name")
        jamb = st.slider("JAMB Score", 100, 400, 250)
        waec = st.slider("WAEC Score", 0, 100, 50)
        intv = st.slider("Interview Score", 0, 100, 50)
        
        if st.button("🚀 Run Forecast Now"):
            input_data = pd.DataFrame({"jamb_score": [jamb], "waec_points": [waec], "interview_score": [intv]})
            prob = float(pipeline.predict(input_data)[0])
            # Logic Correction: 0.5 (50%) is the new threshold
            status = "QUALIFIED" if prob >= 0.5 else "NOT QUALIFIED"
            st.session_state.history.append({"name": name, "status": status, "prob": prob, "jamb": jamb, "waec": waec, "intv": intv})
            
            with col2:
                st.subheader("Analysis Outcome")
                st.metric("Admission Probability", f"{prob:.1%}")
                if status == "QUALIFIED": st.success(f"FINAL DECISION: {status} ✅")
                else: st.error(f"FINAL DECISION: {status} ❌")
                
                fig = px.bar(x=["JAMB", "WAEC", "INT"], y=[jamb/4, waec, intv], color=["JAMB", "WAEC", "INT"])
                st.plotly_chart(fig, use_container_width=True)

elif page == "📋 History Log":
    st.title("📋 Prediction History")
    st.table(pd.DataFrame(st.session_state.history))

elif page == "🖨️ Export Reports":
    st.title("🖨️ Official Certificates")
    for student in st.session_state.history:
        report = f"""--- TIMMYTECH OFFICIAL ADMISSION CERTIFICATE ---
Candidate Name: {student['name']}
JAMB Score: {student['jamb']}
WAEC Score: {student['waec']}
Interview Score: {student['intv']}
Admission Probability: {student['prob']:.1%}
FINAL DECISION: {student['status']}
--------------------------------------------------"""
        st.download_button(f"Download Certificate: {student['name']}", report, f"{student['name']}_certificate.txt")

elif page == "💬 Help & Support":
    st.title("💬 Help Center")
    st.image("https://cdn-icons-png.flaticon.com/512/1000/1000946.png", width=150)
    st.write("### About Timmytech")
    st.write("Timmytech is a high-performance predictive AI developed by **Ajayi Oluwatimileyin Daniel**. It uses advanced Linear Regression to analyze student metrics and provide unbiased admission outlooks.")
    st.markdown("---")
    st.write("### Contact Support")
    st.write("📞 WhatsApp/Call: **09168090334**")
    st.write("👤 Facebook: **Ajayi oluwatimileyin Daniel**")
    st.write("🎵 TikTok: **Doctor Timmy**")

