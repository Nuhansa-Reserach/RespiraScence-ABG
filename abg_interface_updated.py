import streamlit as st
import numpy as np
import pandas as pd
import joblib
from datetime import datetime
import os

# Load the latest SVM model
model = joblib.load("svm_model_v151.pkl")

# Excel file path
excel_file = "abg_results_log.xlsx"

# Set page config
st.set_page_config(page_title="RespiraSence-ABG", page_icon="🩸", layout="centered")

# --- Blood Cell UI Header ---
st.markdown("""
    <div style='background-color:#ffe6e6;padding:20px;border-radius:10px;'>
        <h1 style='color:#800000;text-align:center;'>🩺 RespiraSence-ABG</h1>
        <h4 style='color:#660000;text-align:center;'>AI-Powered Blood Gas Interpretation for Modern Medicine</h4>
    </div>
""", unsafe_allow_html=True)

# --- Basic Login ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if email == "nuhansa@example.com" and password == "1234":
            st.success("Login successful!")
            st.session_state.logged_in = True
        else:
            st.error("Invalid email or password.")
    st.stop()

# Preview/Dashboard Page
def preview_page():
    show_header()
    st.success("Welcome to RespiraSence-ABG!")
    st.markdown("#### ✅ What would you like to do?")
    if st.button("🧪 Start New ABG Test"):
        st.session_state.page = "test"
        st.rerun()
    st.markdown("---")
    st.caption("Tip: Use the button above to begin ABG testing.")

# --- ABG Entry ---
st.subheader("🧪 Enter ABG Parameters")

patient_name = st.text_input("Patient Name", placeholder="e.g., John Doe")

pH = st.number_input("pH (Normal: 7.35 - 7.45)", value=7.40, step=0.01)
pCO2 = st.number_input("pCO₂ (Normal: 35 - 45 mmHg)", value=40.0, step=0.1)
pO2 = st.number_input("pO₂ (Normal: 75 - 100 mmHg)", value=90.0, step=0.1)
HCO3 = st.number_input("HCO₃ (Normal: 22 - 26 mEq/L)", value=24.0, step=0.1)
SaO2 = st.number_input("SaO₂ (Normal: 95 - 100%)", value=98.0, step=0.1)


if st.button("🔍 Analyze ABG Status"):
    abnormal = pH < 7.35 or pH > 7.45 or pCO2 < 35 or pCO2 > 45 or pO2 < 75 or pO2 > 100 or HCO3 < 22 or HCO3 > 26 or SaO2 < 95

    if not patient_name.strip():
        st.warning("⚠️ Please enter the patient name before analyzing.")
    else:
        input_data = np.array([[pH, pCO2, pO2, HCO3, SaO2]])
        prediction = model.predict(input_data)[0]

        status = "Normal" if prediction == 0 else "Abnormal"

        # Show result
        if prediction == 0:
            st.success("✅ Status: Normal")
            st.write("All ABG parameters are within expected physiological ranges.")
        else:
            st.error("⚠️ Status: Abnormal")
            st.markdown("### 🩺 Possible Symptoms:")
            st.markdown("""
            - Shortness of breath  
            - Dizziness or confusion  
            - Rapid breathing  
            - Fatigue or drowsiness  
            - Cyanosis (bluish lips or fingers)
            """)
            st.markdown("### 💡 Suggested Actions:")
            st.markdown("""
            - Repeat ABG test for confirmation  
            - Administer oxygen or ventilation support  
            - Consult a respiratory specialist  
            - Monitor patient for deterioration  
            - Consider ICU referral if symptoms worsen
            """)

        # Save to Excel
        new_row = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Patient Name": patient_name,
            "pH": pH,
            "pCO2": pCO2,
            "pO2": pO2,
            "HCO3": HCO3,
            "SaO2": SaO2,
            "Status": status
        }

        excel_file = "abg_results_log.xlsx"
        if os.path.exists(excel_file):
            df = pd.read_excel(excel_file)
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        else:
            df = pd.DataFrame([new_row])

        df.to_excel(excel_file, index=False)

        st.info(f"📁 Result for **{patient_name}** saved to Excel log.")

# Footer
st.markdown("---")
st.caption("Developed by **Nuhansa Herath** - BEng(Hons) in Biomedical Engineering Final Year Project - London Metropolitan University")
