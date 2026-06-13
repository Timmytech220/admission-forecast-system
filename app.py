import streamlit as st
import pandas as pd
import plotly.express as px
import joblib


import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st


def save_data(name, status, prob, jamb, olevel, intv):
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets']
    # This reads the secret you just saved in the dashboard
    creds = ServiceAccountCredentials.from_json_keyfile_dict(dict(st.secrets["gcp_service_account"]), scope)
    client = gspread.authorize(creds)
    
    # Open the sheet by its name (Make sure it is exactly: Admission_Forecast_Data)
    sheet = client.open("Admission_Forecast_Data").sheet1
    sheet.append_row([name, status, prob, jamb, olevel, intv])


# --- 1. CONFIG & STYLING ---
st.set_page_config(page_title="Timmytech Admission Forecast", layout="wide")
st.markdown("""
    <style>
    section[data-testid="stSidebar"] { background-color: #1e3a8a !important; color: white !important; }
    section[data-testid="stSidebar"] * { color: white !important; }
    
    /* Optimized Login Container */
    .login-container { 
        padding: 40px; 
        border-radius: 20px; 
        background: linear-gradient(180deg, #ffffff 0%, #eef2ff 100%); 
        border: 1px solid #1e3a8a;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.1);
    }
    
    .result-card { border: 1px solid #1e3a8a; padding: 20px; border-radius: 10px; background-color: #ffffff; }
    h1, h2 { color: #1e3a8a !important; }
    .help-img { border-radius: 50%; width: 150px; height: 150px; border: 4px solid #1e3a8a; object-fit: cover; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    c1, mid, c3 = st.columns([1, 1.5, 1])
    with mid:
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>🔐 Timmytech Secure Access</h2>", unsafe_allow_html=True)
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            if user == "Timmy" and pwd == "1234":
                st.session_state.logged_in = True
                st.rerun()
            else: st.error("Invalid credentials!")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 3. MODEL & STATE ---
pipeline = joblib.load("final_pipeline.pkl")
if "history" not in st.session_state: st.session_state.history = []
if "last_result" not in st.session_state: st.session_state.last_result = None

# --- 4. SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2942/2942813.png", width=80) 
    st.markdown("## Timmytech Console")
    page = st.radio("MAIN NAVIGATION", ["Dashboard", "Admission Forecast", "History Log", "Export Reports", "Help & Support"])
    st.divider()
    st.write("Developed by: **Ajayi Oluwatimileyin Daniel**")
# --- 5. PAGE LOGIC ---
if page == "Dashboard":
    st.title("Welcome to Timmytech Admission Forecast System")
    st.image("https://images.unsplash.com/photo-1552664730-d307ca884978?q=80&w=2000", use_container_width=True)
    if len(st.session_state.history) > 0:
        df = pd.DataFrame(st.session_state.history)
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Forecasts", len(df))
        c2.metric("Success Rate", f"{(len(df[df['status'].str.contains('QUALIFIED')])/len(df))*100:.1f}%")
        c3.metric("Avg Probability", f"{df['prob'].mean()*100:.1f}%")

elif page == "Admission Forecast":
    st.title("Admission Forecast Portal")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Student Profile Inputs")
        name = st.text_input("Full Name")
        jamb = st.slider("JAMB Score", 100, 400, 250)
        olevel = st.slider("O-Level Points", 0, 100, 50)
        intv = st.slider("Interview Score", 0, 100, 50)
        
        if st.button("Run Forecast Now", type="primary"):
            if not name.strip(): 
                st.error("⚠️ Please enter a student name.")
            else:
                input_data = pd.DataFrame({"jamb_score": [jamb], "waec_points": [olevel], "interview_score": [intv]})
                prob = float(pipeline.predict(input_data)[0])
                status = f"{'QUALIFIED' if prob >= 0.5 else 'NOT QUALIFIED'} ({prob:.1%})"
                
                # --- Database Save Action ---
                save_data(name, status, f"{prob:.1%}", str(jamb), str(olevel), str(intv))
                
                st.session_state.last_result = {"name": name, "status": status, "prob": prob, "jamb": jamb, "olevel": olevel, "intv": intv}
                st.session_state.history.append(st.session_state.last_result)
                st.success("Result saved to database!")
    
    with col2:
        if st.session_state.last_result:
            res = st.session_state.last_result
            st.success(f"FINAL DECISION: {res['status']}")
            st.info(f"🚀 **Insight Summary:** Your profile metrics suggest focusing on { 'your Interview skills' if res['intv'] < 60 else 'your core academic subjects' }.")
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            df_plot = pd.DataFrame({"Metric": ["JAMB", "O-Level", "INT"], "Score": [res['jamb']/4, res['olevel'], res['intv']]})
            fig = px.bar(df_plot, x="Metric", y="Score", color="Score", color_continuous_scale="Blues")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

elif page == "History Log":
    st.title("📋 Prediction History")
    if st.session_state.history: st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)
    else: st.write("No records yet.")

elif page == "Export Reports":
    st.title("🖨️ Export Official Reports")
    for i, s in enumerate(st.session_state.history):
        txt = f"TIMMYTECH REPORT\nName: {s['name']}\nDecision: {s['status']}"
        st.download_button(f"Download: {s['name']}", txt, file_name=f"{s['name']}_report.txt")

elif page == "Help & Support":
    st.title("💬 Help & Support Center")
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown('<img src="https://i.imgur.com/7M49Vnz.jpeg" class="help-img">', unsafe_allow_html=True)
    with c2:
        st.subheader("Developer Info")
        st.write("Developed by: **Ajayi Oluwatimileyin Daniel**")
        st.write("📞 **WhatsApp/Call:** 09168090334")
        st.write("📱 **Facebook:** [facebook.com/Timmytech](https://facebook.com/Timmytech)")
        st.write("🎵 **TikTok:** [tiktok.com/@Timmytech](https://tiktok.com/@Timmytech)")
        
