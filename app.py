import streamlit as st
import joblib
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Admission Forecast System", page_icon="🎓", layout="centered")

# ---------------- PIPELINE LOADING ----------------
@st.cache_resource
def load_pipeline():
    # Loading the "Smart" engine we built
    return joblib.load("final_pipeline.pkl")

pipeline = load_pipeline()

# ---------------- UI ----------------
st.title("🎓 Admission Forecast System")
st.markdown("### AI-powered admission prediction dashboard")
st.markdown("---")

if "history" not in st.session_state:
    st.session_state.history = []

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Student Name")
    jamb = st.slider("JAMB Score", 100, 400, 250)
with col2:
    waec = st.slider("WAEC Score", 0, 100, 50)
    interview = st.slider("Interview Score", 0, 100, 50)

# ---------------- PREDICTION ----------------
if st.button("Predict Admission", type="primary"):
    # The pipeline ONLY expects these 3 specific columns
    input_data = pd.DataFrame({
        "jamb_score": [jamb],
        "waec_points": [waec],
        "interview_score": [interview]
    })

    # The pipeline handles all scaling and math internally
    prediction = pipeline.predict(input_data)
    prob = float(prediction[0])
    prob = max(0, min(1, prob))

    st.session_state.history.append({"name": name or "Anonymous", "prob": prob})

    st.metric("Admission Probability", f"{prob:.2%}")

    if prob >= 0.7:
        st.success("🎉 RESULT: ADMITTED")
        st.balloons()
    elif prob >= 0.4:
        st.warning("⚠ RESULT: BORDERLINE")
    else:
        st.error("❌ RESULT: NOT ADMITTED")

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("Recent Predictions")
    for item in reversed(st.session_state.history[-5:]):
        st.write(f"**{item['name']}** → {item['prob']:.2%}")
        
