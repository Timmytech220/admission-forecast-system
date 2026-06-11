import streamlit as st
import joblib
import pandas as pd
import matplotlib.pyplot as plt

# 1. Page Config
st.set_page_config(page_title="Admission Forecast", page_icon="🎓", layout="centered")

# 2. Optimized Model Loading
@st.cache_resource
def load_my_model():
    # Ensure this path is correct for where your pkl file lives
    return joblib.load('/content/drive/MyDrive/admission_model_v2.pkl')

model = load_my_model()

# --- UI Styling ---
st.title("🎓 Admission Forecast System")
st.markdown("---")

if 'history' not in st.session_state:
    st.session_state.history = []

# --- Input Section ---
st.subheader("📝 Enter Student Details")
col1, col2 = st.columns(2)
with col1:
    student_name = st.text_input("👤 Student Name")
    jamb = st.slider("📝 JAMB Score", 100, 400, 250)
with col2:
    o_level = st.slider("📚 WAEC/O-Level Points", 0, 100, 50)
    post_utme = st.slider("🗣️ Interview/Post-UTME", 0, 100, 50)

year = st.selectbox("📅 Admission Year", [2024, 2025, 2026, 2027])

# --- Forecast Logic ---
if st.button("🚀 Forecast Admission Probability", type="primary"):
    input_df = pd.DataFrame({
        'Year': [year],
        'JAMB_SCORE': [jamb],
        'WAEC_POINTS': [o_level],
        'INTERVIEW_SCORE': [post_utme]
    })
    
    input_df['AGGREGATE_SCORE'] = (input_df['JAMB_SCORE'] * 0.5) + (input_df['WAEC_POINTS'] * 0.3) + (input_df['INTERVIEW_SCORE'] * 0.2)
    input_df['CONSISTENCY_SCORE'] = input_df[['JAMB_SCORE', 'WAEC_POINTS', 'INTERVIEW_SCORE']].std(axis=1)

    prediction = model.predict(input_df[['Year', 'JAMB_SCORE', 'WAEC_POINTS', 'INTERVIEW_SCORE', 'AGGREGATE_SCORE', 'CONSISTENCY_SCORE']])
    prob = max(0.0, min(1.0, prediction[0]))

    st.session_state.history.append({"Name": student_name, "Prob": prob})
    
    st.metric(label="Forecasted Admission Probability", value=f"{prob:.2%}")

    if prob > 0.7: st.balloons(); st.success("### Result: Qualified")
    elif prob > 0.4: st.info("### Result: Borderline")
    else: st.error("### Result: Review Required")

    st.subheader("🔍 Decision Drivers")
    fig, ax = plt.subplots(figsize=(6, 2))
    # Ensure your model has .coef_ attribute; if it's a pipeline, use model.named_steps['model'].coef_
    ax.barh(['Year', 'JAMB', 'WAEC', 'Interview', 'Agg', 'Cons'], model.coef_, color='#003366')
    st.pyplot(fig)

with st.sidebar:
    st.header("🕒 Recent Forecasts")
    for entry in reversed(st.session_state.history[-5:]):
        with st.container(border=True):
            st.write(f"**{entry['Name'] or 'Anonymous'}**")
            st.write(f"Probability: **{entry['Prob']:.1%}**")
