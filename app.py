import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

# --- 1. AUTHENTICATION ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False

    if not st.session_state.password_correct:
        st.markdown("""
            <style>
            .login-card { 
                text-align: center; 
                padding: 40px; 
                border-radius: 20px; 
                background-color: #ffffff; 
                box-shadow: 0px 10px 20px rgba(0,0,0,0.15);
                max-width: 400px; 
                margin: auto;
                border: 1px solid #e1e4e8;
            }
            </style>
            """, unsafe_allow_html=True)
        
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        # Login Page Image (Standing)
        st.image("https://i.imgur.com/KyKv9T9.png", width=180)
        st.title("Timmytech Console")
        st.subheader("Admission Forecast System")
        st.write("Secure Access Portal")
        
        user = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if user == "Timmy" and password == "1234":
                st.session_state.password_correct = True
                st.rerun()
            else:
                st.error("Invalid username or password")
        st.markdown('</div>', unsafe_allow_html=True)
        return False
    return True

# --- 2. PREMIUM THEME & BLUE SIDEBAR CSS ---
st.set_page_config(page_title="Timmytech Admission Forecast")
st.markdown("""
    <style>
    section[data-testid="stSidebar"] { background-color: #1e3a8a !important; color: white !important; padding-top: 40px; }
    section[data-testid="stSidebar"] * { color: white !important; }
    div.stButton > button { width: 100%; border-radius: 8px; background-color: #3b82f6; color: white; font-weight: bold; height: 3.5em; }
    .result-card { border: 1px solid #e0e0e0; padding: 20px; border-radius: 10px; background-color: rgba(249, 249, 249, 0.1); box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. EXECUTION ---
if check_password():
    pipeline = joblib.load("final_pipeline.pkl")
    if "history" not in st.session_state: st.session_state.history = []
    if "last_result" not in st.session_state: st.session_state.last_result = None

    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2942/2942813.png", width=80) 
        st.markdown("## Timmytech Console")
        page = st.radio("MAIN NAVIGATION", ["Dashboard", "Admission Forecast", "History Log", "Export Reports", "Help & Support"], index=0)
        st.markdown("<br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
        st.caption("Status: Online")
        st.write("Developed by: **Ajayi Oluwatimileyin Daniel**")

    # --- 5. PAGE LOGIC ---
    if page == "Dashboard":
        st.title("Welcome to Timmytech Admission Forecast System")
        st.image("https://images.unsplash.com/photo-1552664730-d307ca884978?q=80&w=2000", use_container_width=True)
        if len(st.session_state.history) > 0:
            df = pd.DataFrame(st.session_state.history)
            st.subheader("System Analytics Overview")
            c1, c2, c3 = st.columns(3)
            with c1: st.info(f"Total Applicants: **{len(df)}**")
            with c2: st.success(f"Success Rate: **{(len(df[df['status'] == 'QUALIFIED']) / len(df)) * 100:.1f}%**")
            with c3: st.warning(f"Avg. Probability: **{df['prob'].mean() * 100:.1f}%**")
        else:
            st.info("Run your first forecast in the 'Admission Forecast' tab to see analytics here!")
        st.markdown("### Intelligent predictive analytics for your academic journey.")

    elif page == "Admission Forecast":
        st.title("Admission Forecast Portal")
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("Student Profile Inputs")
            name = st.text_input("Full Name")
            jamb = st.slider("JAMB Score", 100, 400, 250)
            waec = st.slider("WAEC Score", 0, 100, 50)
            intv = st.slider("Interview Score", 0, 100, 50)
            if st.button("Run Forecast Now"):
                if not name.strip(): st.error("Please enter a student name.")
                else:
                    input_data = pd.DataFrame({"jamb_score": [jamb], "waec_points": [waec], "interview_score": [intv]})
                    prob = float(pipeline.predict(input_data)[0])
                    status = "QUALIFIED" if prob >= 0.5 else "NOT QUALIFIED"
                    st.session_state.last_result = {"name": name, "status": status, "prob": prob, "jamb": jamb, "waec": waec, "intv": intv}
                    st.session_state.history.append(st.session_state.last_result)
                if st.session_state.last_result:
                    res = st.session_state.last_result
                    if res['status'] == "QUALIFIED": st.success(f"FINAL DECISION: {res['status']}")
                    else: st.error(f"FINAL DECISION: {res['status']}")
                    st.info(f"💡 **AI Suggestion:** Your score of {res['prob']:.1%} suggests focusing on { 'Interview' if res['intv'] < 60 else 'academic core subjects' } to improve future probability.")
        with col2:
            if st.session_state.last_result:
                res = st.session_state.last_result
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.subheader("Visual Analysis")
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
            st.download_button(label=f"Download: {s['name']}", data=txt, file_name=f"{s['name']}_report.txt", key=f"dl_{i}_{s['name']}")

    elif page == "Help & Support":
        st.title("💬 Help & Support")
        # Help Page Image (With Phone)
        st.image("https://i.imgur.com/7M49Vnz.jpeg", width=250)
        st.write("Developed by **Ajayi Oluwatimileyin Daniel**.")
        st.markdown("---")
        st.write("📞 **WhatsApp/Call:** 09168090334")
        
