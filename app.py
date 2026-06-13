import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

# --- 1. CONFIG & CSS ---
st.set_page_config(page_title="Timmytech Admission Forecast", layout="wide")
st.markdown("""
    <style>
    section[data-testid="stSidebar"] { background-color: #1e3a8a !important; color: white !important; }
    section[data-testid="stSidebar"] * { color: white !important; }
    .help-img { border-radius: 50%; width: 180px; height: 180px; border: 5px solid #3b82f6; object-fit: cover; }
    .result-card { border: 1px solid #e0e0e0; padding: 20px; border-radius: 10px; background-color: #f9f9f9; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. AUTHENTICATION & INITIALIZATION ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    c1, mid, c3 = st.columns([1, 2, 1])
    with mid:
        st.markdown("<h2 style='text-align: center;'>🔐 Timmytech Access</h2>", unsafe_allow_html=True)
        user = st.text_input("Username", placeholder="Enter your username")
        pwd = st.text_input("Password", type="password", placeholder="Enter your password")
        if st.button("Login", use_container_width=True):
            if user == "Timmy" and pwd == "1234":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials!")
    st.stop()

# Load model
pipeline = joblib.load("final_pipeline.pkl")

if "history" not in st.session_state: st.session_state.history = []
if "last_result" not in st.session_state: st.session_state.last_result = None

# --- 3. SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2942/2942813.png", width=80) 
    st.markdown("## Timmytech Console")
    page = st.radio("MAIN NAVIGATION", ["Dashboard", "Admission Forecast", "History Log", "Export Reports", "Help & Support"], index=0)
    st.divider()
    st.caption("Status: Online")
    st.write("Developed by: **Ajayi Oluwatimileyin Daniel**")

# --- 4. PAGE LOGIC ---
if page == "Dashboard":
    st.title("Welcome to Timmytech Admission Forecast System")
    st.image("https://images.unsplash.com/photo-1552664730-d307ca884978?q=80&w=2000", use_container_width=True)
    if len(st.session_state.history) > 0:
        df = pd.DataFrame(st.session_state.history)
        st.subheader("System Analytics Overview")
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Forecasts", len(df))
        c2.metric("Success Rate", f"{(len(df[df['status'] == 'QUALIFIED']) / len(df)) * 100:.1f}%")
        c3.metric("Avg Probability", f"{df['prob'].mean() * 100:.1f}%")

elif page == "Admission Forecast":
    st.title("Admission Forecast Portal")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Student Profile Inputs")
        name = st.text_input("Full Name")
        jamb = st.slider("JAMB Score", 100, 400, 250)
        waec = st.slider("WAEC Score", 0, 100, 50)
        intv = st.slider("Interview Score", 0, 100, 50)
        if st.button("Run Forecast Now", type="primary"):
            if not name.strip(): st.error("Please enter a student name.")
            else:
                input_data = pd.DataFrame({"jamb_score": [jamb], "waec_points": [waec], "interview_score": [intv]})
                prob = float(pipeline.predict(input_data)[0])
                status = "QUALIFIED" if prob >= 0.5 else "NOT QUALIFIED"
                st.session_state.last_result = {"name": name, "status": status, "prob": prob, "jamb": jamb, "waec": waec, "intv": intv}
                st.session_state.history.append(st.session_state.last_result)
    
    with col2:
        if st.session_state.last_result:
            res = st.session_state.last_result
            st.success(f"FINAL DECISION: {res['status']}")
            st.info(f"💡 **AI Suggestion:** Your score of {res['prob']:.1%} suggests focusing on { 'Interview' if res['intv'] < 60 else 'academic core subjects' }.")
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.subheader("Visual Analysis")
            df_plot = pd.DataFrame({"Metric": ["JAMB", "WAEC", "INT"], "Score": [res['jamb']/4, res['waec'], res['intv']]})
            fig = px.bar(df_plot, x="Metric", y="Score", color="Score", color_continuous_scale="Blues")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

elif page == "History Log":
    st.title("📋 Prediction History")
    if st.session_state.history: 
        st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True, hide_index=True)
    else: st.write("No records yet.")

elif page == "Export Reports":
    st.title("🖨️ Export Official Reports")
    for i, s in enumerate(st.session_state.history):
        txt = f"TIMMYTECH REPORT\nName: {s['name']}\nDecision: {s['status']}\nProb: {s['prob']:.1%}"
        st.download_button(label=f"Download: {s['name']}", data=txt, file_name=f"{s['name']}_report.txt", key=f"dl_{i}_{s['name']}")

elif page == "Help & Support":
    st.title("💬 Help & Support Center")
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown('<img src="https://i.imgur.com/7M49Vnz.jpeg" class="help-img">', unsafe_allow_html=True)
    with c2:
        st.subheader("Developer Info")
        st.write("Developed by: **Ajayi Oluwatimileyin Daniel**")
        st.write("System designed to provide predictive admission analytics.")
    st.divider()
    st.subheader("Contact & Socials")
    st.write("📞 **WhatsApp/Call:** 09168090334")
    st.write("📱 **Facebook:** facebook.com/Timmytech")
    st.write("🎵 **TikTok:** tiktok.com/@Timmytech")
