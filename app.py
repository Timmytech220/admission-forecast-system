import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

# --- 1. PREMIUM WHITE THEME & BLUE SIDEBAR CSS ---
st.set_page_config(page_title="Timmytech Admission Forecast", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    section[data-testid="stSidebar"] { background-color: #1e3a8a; color: white; padding-top: 40px; }
    section[data-testid="stSidebar"] * { color: white !important; }
    div.stButton > button { width: 100%; border-radius: 8px; background-color: #3b82f6; color: white; font-weight: bold; height: 3.5em; }
    .result-card { border: 1px solid #e0e0e0; padding: 20px; border-radius: 10px; background-color: #f9f9f9; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
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
    page = st.radio("MAIN NAVIGATION", ["Dashboard", "Admission Forecast", "History Log", "Export Reports", "Help & Support"], index=0)
    st.markdown("<br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
    st.caption("Status: Online")
    st.write("Developed by: **Ajayi Oluwatimileyin Daniel**")

# --- 4. PAGE LOGIC ---

if page == "Dashboard":
    st.title("Welcome to Timmytech Admission Forecast System")
    if len(st.session_state.history) > 0:
        df = pd.DataFrame(st.session_state.history)
        st.subheader("System Analytics Overview")
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Applicants", len(df))
        c2.metric("Success Rate", f"{(len(df[df['status'] == 'QUALIFIED']) / len(df)) * 100:.1f}%")
        c3.metric("Avg. Probability", f"{df['prob'].mean() * 100:.1f}%")
    else:
        st.info("Run your first forecast in the 'Admission Forecast' tab to see analytics here!")

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
            if not name.strip():
                st.error("Please enter a student name.")
            else:
                input_data = pd.DataFrame({"jamb_score": [jamb], "waec_points": [waec], "interview_score": [intv]})
                prob = float(pipeline.predict(input_data)[0])
                status = "QUALIFIED" if prob >= 0.5 else "NOT QUALIFIED"
                st.session_state.last_result = {"name": name, "status": status, "prob": prob, "jamb": jamb, "waec": waec, "intv": intv}
                st.session_state.history.append(st.session_state.last_result)
            
    with col2:
        if st.session_state.last_result:
            res = st.session_state.last_result
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.subheader("Analysis Outcome")
            st.metric("Admission Probability", f"{res['prob']:.1%}")
            if res['status'] == "QUALIFIED": st.success(f"FINAL DECISION: {res['status']}")
            else: st.error(f"FINAL DECISION: {res['status']}")
            
            df_plot = pd.DataFrame({"Metric": ["JAMB", "WAEC", "INT"], "Score": [res['jamb']/4, res['waec'], res['intv']]})
            fig = px.bar(df_plot, x="Metric", y="Score", color="Score", color_continuous_scale="Blues")
            fig.add_hline(y=50, line_dash="dash", line_color="red", annotation_text="Threshold")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

elif page == "History Log":
    st.title("📋 Prediction History")
    if st.session_state.history: st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)
    else: st.write("No records yet.")

elif page == "Export Reports":
    st.title("🖨️ Export Official Reports")
    for i, s in enumerate(st.session_state.history):
        txt = f"TIMMYTECH REPORT\nName: {s['name']}\nDecision: {s['status']}\nProb: {s['prob']:.1%}"
        st.download_button(f"Download: {s['name']}", txt, f"{s['name']}_report.txt", key=f"dl_{i}")

elif page == "Help & Support":
    st.title("💬 Help & Support")
    st.write("Timmytech System. Created by **Ajayi Oluwatimileyin Daniel**.")
