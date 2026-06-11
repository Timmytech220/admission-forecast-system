import streamlit as st
import joblib
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Admission Forecast System",
    page_icon="🎓",
    layout="centered"
)

# ---------------- MODEL LOADING ----------------
@st.cache_resource
def load_model():
    return joblib.load("admission_model.pkl")  # ✅ FIXED (NO v2)

model = load_model()

# ---------------- UI ----------------
st.title("🎓 Admission Forecast System")
st.markdown("### AI-powered admission prediction dashboard")
st.markdown("---")

# session history
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- INPUTS ----------------
st.subheader("Student Information")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Student Name")
    jamb = st.slider("JAMB Score", 100, 400, 250)

with col2:
    waec = st.slider("WAEC Score", 0, 100, 50)
    interview = st.slider("Interview Score", 0, 100, 50)

year = st.selectbox("Admission Year", [2024, 2025, 2026, 2027])

# ---------------- PREDICTION ----------------
if st.button("Predict Admission", type="primary"):

    data = pd.DataFrame({
        "Year": [year],
        "JAMB_SCORE": [jamb],
        "WAEC_POINTS": [waec],
        "INTERVIEW_SCORE": [interview]
    })

    # feature engineering (safe)
    data["AGGREGATE_SCORE"] = (
        data["JAMB_SCORE"] * 0.5 +
        data["WAEC_POINTS"] * 0.3 +
        data["INTERVIEW_SCORE"] * 0.2
    )

    data["CONSISTENCY_SCORE"] = data[
        ["JAMB_SCORE", "WAEC_POINTS", "INTERVIEW_SCORE"]
    ].std(axis=1)

    prediction = model.predict(data)

    prob = float(prediction[0])
    prob = max(0, min(1, prob))

    st.session_state.history.append({
        "name": name if name else "Anonymous",
        "prob": prob
    })

    st.metric("Admission Probability", f"{prob:.2%}")

    if prob >= 0.7:
        st.success("🎉 RESULT: ADMITTED")
        st.balloons()
    elif prob >= 0.4:
        st.warning("⚠ RESULT: BORDERLINE")
    else:
        st.error("❌ RESULT: NOT ADMITTED")

    # ---------------- CHART ----------------
    st.subheader("Feature Influence")

    features = ["Year", "JAMB", "WAEC", "Interview", "Agg", "Consistency"]

    # safe fallback if model has no coef_
    if hasattr(model, "coef_"):
        values = model.coef_
    else:
        values = [1, 1, 1, 1, 1, 1]

    chart = pd.DataFrame({
        "Feature": features,
        "Importance": values[:6]
    })

    fig = px.bar(chart, x="Feature", y="Importance", title="Model Influence")
    st.plotly_chart(fig)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("Recent Predictions")

    for item in reversed(st.session_state.history[-5:]):
        st.write(f"**{item['name']}** → {item['prob']:.2%}")
