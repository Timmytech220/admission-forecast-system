import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
from fpdf import FPDF

# --- 1. PREMIUM WHITE THEME CSS ---
st.markdown("""
    <style>
    /* Main Layout */
    .stApp { background-color: #ffffff; color: #333; }
    /* Sidebar Styling */
    section[data-testid="stSidebar"] { background-color: #f4f7f6; padding-top: 20px; }
    /* Button Styling */
    div.stButton > button { width: 100%; border-radius: 8px; background-color: #4A90E2; color: white; font-weight: bold; }
    /* Headers */
    h1, h2, h3 { color: #2C3E50; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SETUP & MODEL ---
st.set_page_config(page_title="Timmytech Admission Forecast", layout="wide")
pipeline = joblib.load("final_pipeline.pkl")

if "history" not in st.session_state: st.session_state.history = []

# --- 3. ATTRACTIVE SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2942/2942813.png", width=80)
    st.title("Timmytech Console")
    st.markdown("---")
    
    # Navigation with Icons
    page = st.radio("Navigation", 
                    ["📊 Dashboard", "🎯 Admission Forecast", "📋 History Log", "🖨️ Export Reports", "💬 Help & Support"], 
                    index=0)
    
    st.markdown("---")
    st.subheader("System Status")
    st.success("🟢 Online")
    st.caption(f"Forecasts Processed: {len(st.session_state.history)}")
    st.markdown("---")
    st.write("Built by: **Ajayi Oluwatimileyin Daniel**")

# --- 4. PAGE CONTENT ---

if page == "📊 Dashboard":
    st.title("Welcome to Timmytech Admission Forecast System")
    st.markdown("### Empowering academic excellence through data-driven predictions.")
    st.image("https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?q=80&w=1400", use_column_width=True)
    st.info("Navigate using the sidebar to begin your forecasting journey.")

elif page == "🎯 Admission Forecast":
    st.title("🎯 Admission Forecast Portal")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Student Profile Information")
        name = st.text_input("Full Name")
        jamb = st.slider("JAMB Score (100-400)", 100, 400, 250)
        waec = st.slider("WAEC Score (0-100)", 0, 100, 50)
        intv = st.slider("Interview Score (0-100)", 0, 100, 50)
        
        if st.button("🚀 Analyze Now"):
            input_data = pd.DataFrame({"jamb_score": [jamb], "waec_points": [waec], "interview_score": [intv]})
            prob = float(pipeline.predict(input_data)[0])
            status = "QUALIFIED" if prob >= 0.7 else "NOT QUALIFIED"
            st.session_state.history.append({"name": name, "jamb": jamb, "waec": waec, "intv": intv, "prob": prob, "status": status})
            
            with col2:
                st.subheader("Analysis Results")
                st.metric("Admission Probability", f"{prob:.1%}")
                if status == "QUALIFIED": st.success(f"STATUS: {status}")
                else: st.error(f"STATUS: {status}")
                
                fig = px.bar(x=["JAMB", "WAEC", "INT"], y=[jamb/4, waec, intv], 
                             color=[jamb/4, waec, intv], color_continuous_scale="RdYlGn")
                st.plotly_chart(fig, use_container_width=True)

elif page == "📋 History Log":
    st.title("📋 Detailed Prediction History")
    # Separate logic
    q_data = [s for s in st.session_state.history if s['status'] == "QUALIFIED"]
    nq_data = [s for s in st.session_state.history if s['status'] == "NOT QUALIFIED"]
    
    st.subheader("✅ Qualified Candidates")
    if q_data: st.table(pd.DataFrame(q_data))
    else: st.write("No qualified candidates found.")
        
    st.subheader("❌ Not Qualified Candidates")
    if nq_data: st.table(pd.DataFrame(nq_data))
    else: st.write("No disqualified candidates found.")

elif page == "🖨️ Export Reports":
    st.title("🖨️ Individual Report Printing")
    for student in st.session_state.history:
        if st.button(f"Generate PDF for {student['name']}"):
            # Simple PDF logic
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt="Timmytech Official Admission Report", ln=True, align='C')
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Candidate Name: {student['name']}", ln=True)
            pdf.cell(200, 10, txt=f"Final Decision: {student['status']}", ln=True)
            st.download_button(f"Click to Download {student['name']}_Report.pdf", pdf.output(dest='S').encode('latin-1'), f"{student['name']}_report.pdf", "application/pdf")

elif page == "💬 Help & Support":
    st.title("💬 Help Center")
    st.write("I am **Ajayi Oluwatimileyin Daniel**, your lead developer for Timmytech.")
    st.markdown("""
    ### System Explanation
    - **How it works:** Our system maps your entrance exam scores against historical data.
    - **Need help?** If you have specific questions about your scores, feel free to contact the administrator.
    """)
