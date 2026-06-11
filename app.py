import streamlit as st
import joblib
import pandas as pd

# Load the model
@st.cache_resource
def load_model():
    return joblib.load("admission_model.pkl")

model = load_model()

st.title("🎓 Admission Forecast System")

# Inputs - Using the exact names the model expects
jamb = st.slider("JAMB Score", 100, 400, 250)
waec = st.slider("WAEC Points", 0, 100, 50)
interview = st.slider("Interview Score", 0, 100, 50)

if st.button("Forecast"):
    # Create the dataframe with the exact column names used in Colab training
    input_data = pd.DataFrame([[jamb, waec, interview]], 
                              columns=['jamb_score', 'waec_points', 'interview_score'])
    
    # Predict
    prediction = model.predict(input_data)
    
    # Display result
    prob = prediction[0]
    st.write(f"### Forecasted Probability: {prob:.2%}")
    
    if prob > 0.6:
        st.success("Result: Likely to be admitted")
    else:
        st.warning("Result: Low probability of admission")
