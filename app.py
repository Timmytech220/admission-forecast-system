import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import os
import uuid
from datetime import datetime
from PIL import Image, ImageDraw



# 1. Update the function to handle missing user_iddef load_user_from_sheet(user_id=None):
    try:
        conn = st.connection("gsheets", type="gsheets")
        df = conn.read(worksheet="Sheet1")
        if user_id:
            df = df[df['id'] == user_id]
        return df.to_dict('records')
    except Exception as e:
        return []

# 2. Call it properly

if 'history' not in st.session_state:
    # If you have a logged-in user, pass their ID; otherwise pass None
    st.session_state.history = load_user_from_sheet() 
    
    


def create_shareable_card(name, status, jamb, olevel, intv, total_score):
    # Setup
    report_id = f"TT-{uuid.uuid4().hex[:8].upper()}"
    issue_date = datetime.now().strftime("%d-%m-%Y")
    
    # Professional Palette: Off-white background, Navy Blue text/borders, Gold accents
    bg_color = (248, 249, 250)
    navy_color = (0, 32, 96)
    gold_color = (191, 144, 0)
    
    img = Image.new('RGB', (800, 1000), color=bg_color)
    d = ImageDraw.Draw(img)
    
    # Load fonts
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 40)
        font_header = ImageFont.truetype("arialbd.ttf", 28)
        font_text = ImageFont.truetype("arial.ttf", 22)
        font_bold = ImageFont.truetype("arialbd.ttf", 24)
    except:
        font_title = font_header = font_text = font_bold = ImageFont.load_default()

    # 1. Decorative Border
    d.rectangle([20, 20, 780, 980], outline=navy_color, width=8)
    
    # 2. Logo
    try:
        logo = Image.open("logo.png").convert("RGBA").resize((120, 120))
        img.paste(logo, (340, 60), logo)
    except:
        pass

    # 3. Headings (Centered)
    d.text((400, 200), "TIMMYTECH UNIVERSITY OF CODING", font=font_title, fill=navy_color, anchor="mm")
    d.text((400, 250), "OFFICIAL ADMISSION FORECAST VERIFICATION REPORT", font=font_header, fill=gold_color, anchor="mm")
    d.line([100, 280, 700, 280], fill=navy_color, width=2)

    # 4. Metadata
    d.text((100, 320), f"Name: {name}", font=font_text, fill=(0, 0, 0))
    d.text((500, 320), f"Report No.: {report_id}", font=font_text, fill=(0, 0, 0))
    d.text((100, 360), f"Date of Report: {issue_date}", font=font_text, fill=(0, 0, 0))

    # 5. Performance Table
    d.text((100, 420), "SCORES OF EXAMINATION LISTED BELOW:", font=font_bold, fill=navy_color)
    d.rectangle([100, 450, 700, 490], outline=navy_color, fill=(230, 235, 245))
    d.text((120, 460), "SUBJECT", font=font_bold, fill=navy_color)
    d.text((450, 460), "SCORE", font=font_bold, fill=navy_color)
    d.text((600, 460), "FULL", font=font_bold, fill=navy_color)
    
    y = 510
    items = [("JAMB (UTME)", str(jamb), "400"), ("O-LEVEL", str(olevel), "30"), ("INTERVIEW", str(intv), "100")]
    for sub, score, full in items:
        d.text((120, y), sub, font=font_text, fill=(0, 0, 0))
        d.text((450, y), score, font=font_text, fill=(0, 0, 0))
        d.text((600, y), full, font=font_text, fill=(0, 0, 0))
        y += 50

    # 6. Admission Status (Bold)
    d.rectangle([100, y + 50, 700, y + 120], outline=navy_color, width=2)
    d.text((400, y + 85), f"ADMISSION STATUS: {status.upper()}", font=font_title, fill=navy_color, anchor="mm")
    
    # 7. Disclaimer
    d.text((400, 950), "Verification report can be verified online at: https://timmytech.com", font=font_text, fill=(100, 100, 100), anchor="mm")
    
    card_path = "official_admission_report.png"
    img.save(card_path)
    return card_path
    
    
# --- 1. THE PERSISTENCE HOOK (Must be at the top) ---
query_params = st.query_params

# This function fetches data from Google Sheets based on the user_id in the URL

# --- 2. REST OF YOUR CODE (CSS, Translations, UI, etc.) ---

st.markdown("""
    <style>
    /* Global Styles */
    .stApp { background-color: #f8f9fa; }
    
    /* Button Styling (Premium Blue) */
    div.stButton > button { 
        background-color: #1e3a8a; 
        color: white; 
        border-radius: 8px; 
        font-weight: bold; 
    }
    
    /* Premium Report Card Style */
    .report-card { 
        background: white; 
        padding: 15px; 
        border-radius: 10px; 
        border: 1px solid #e2e8f0; 
        margin-bottom: 15px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] { 
        background-color: #0e1117; 
        color: white; 
    }
    </style>
""", unsafe_allow_html=True)


# --- LANGUAGES ---

translations = {
    "English": {"nav_title": "MAIN NAVIGATION", "title": "Admission Forecast Portal", "btn": "Run Forecast Now", "success": "FINAL DECISION", "roadmap": "💡 Improvement Roadmap"},
    "Hausa": {"nav_title": "BABBAN JERE", "title": "Tashar Hasashen Shiga Makaranta", "btn": "Fara Hasashen Yanzu", "success": "SAKO NA KARSHE", "roadmap": "💡 Hanyar Ingantawa"},
    "French": {"nav_title": "NAVIGATION PRINCIPALE", "title": "Portail de prévision d'admission", "btn": "Lancer la prévision", "success": "DÉCISION FINALE", "roadmap": "💡 Feuille de route"},
    "Yoruba": {"nav_title": "AWON ILE-ISE", "title": "Ile-ise Isiro Gbigba-si-Ile-Iwe", "btn": "Bere Isiro Isiro", "success": "IPARI ERO", "roadmap": "💡 Ona lati se atunse"},
    "Igbo": {"nav_title": "NKE N'IHU", "title": "Portal Amụma Nnabata", "btn": "Malite Amụma Ugbu a", "success": "MKPEBI IKPEAZỤ", "roadmap": "💡 Ụzọ mmezi"}
}


ALL_SUBJECTS = [
    'None', 'Biology', 'Chemistry', 'Physics', 'Accounting', 'Economics', 
    'Government', 'CRS/IRS', 'Literature-in-English', 'Agricultural Science', 
    'Commerce', 'Geography', 'History', 'Further Mathematics', 'Computer Science',
    # Adding these common subjects:
    'Islamic Studies', 'Yoruba', 'Igbo', 'Hausa', 'Civic Education', 
    'Technical Drawing', 'Physical Education', 'Food and Nutrition', 
    'Visual Art', 'Music', 'French'
]

# --- Put this right after your imports ---
def calculate_olevel_points(grades):
    grade_map = {'A1': 6, 'B2': 5, 'B3': 4, 'C4': 3, 'C5': 2, 'C6': 1, 'None': 0}
    points = sum([grade_map.get(grade, 0) for grade in grades])
    return points

def get_roadmap(jamb, olevel_points):
    tips = []
    if jamb < 250:
        tips.append("📈 **JAMB:** Aim for 250+ to increase your selection probability.")
    if olevel_points < 20:
        tips.append("📚 **O-Level:** Your point total is low. Consider retaking core subjects.")
    if not tips:
        tips.append("🌟 **Great profile!** Keep maintaining your current performance.")
    return tips
    

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

def save_data(name, status, prob, jamb, olevel, intv):
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(dict(st.secrets["gcp_service_account"]), scope)
    client = gspread.authorize(creds)
    
    # Use the unique ID from your sheet's URL
    spreadsheet = client.open_by_key("1mmG9VbogSnTLmLwWpOmVa3L1CWCCf5EcZmvJCAGCUp4")
    
    # This grabs the first tab in your sheet
    sheet = spreadsheet.get_worksheet(0) 
    
    # This appends the data
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
    
    # Language Picker: Automatically pulls all keys (English, Hausa, French, Yoruba, Igbo)
    lang = st.selectbox("🌍 Select Language", list(translations.keys()))
    
    # Dynamic navigation based on the selected language
    page = st.radio(
        translations[lang]["nav_title"], 
        ["Dashboard", "Admission Forecast", "Bulk Forecast", "History Log", "Export Reports", "Help & Support"]
    )
    
    st.divider()
    st.write("Developed by: **Ajayi Oluwatimileyin Daniel**")
    




# --- 5. PAGE LOGIC 
if page == "Dashboard":
    st.title("Welcome to Timmytech Admission Forecast System")
    
    # 1. Add the dashboard image
    st.image("https://images.unsplash.com/photo-1552664730-d307ca884978?q=80&w=2000", 
             caption="Admission Excellence", 
             use_container_width=True)

    # 2. Add professional metrics if data exists
    if len(st.session_state.history) > 0:
        df = pd.DataFrame(st.session_state.history)
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Forecasts", len(df))
        c2.metric("Success Rate", f"{(len(df[df['status'].str.contains('QUALIFIED')])/len(df))*100:.1f}%")
        c3.metric("Avg Probability", f"{df['prob'].mean()*100:.1f}%")

        # 3. Add a professional Bar Chart using Plotly
        st.subheader("Performance Overview")
        status_counts = df['status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        
        fig = px.bar(status_counts, x='Status', y='Count', color='Status', 
                     title="Admission Status Distribution")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No forecast data available yet. Head over to 'Admission Forecast' to start!")

elif page == "Admission Forecast":
    st.title(translations[lang]["title"])
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Student Profile Inputs")
        name = st.text_input("Full Name")
        jamb = st.slider("JAMB Score", 100, 400, 250)
        
        st.write("**Select your 5 core/required subjects:**")
        c_eng, c_mat = st.columns(2)
        with c_eng: eng = st.selectbox("English Language", ['None', 'A1', 'B2', 'B3', 'C4', 'C5', 'C6'])
        with c_mat: mat = st.selectbox("Mathematics", ['None', 'A1', 'B2', 'B3', 'C4', 'C5', 'C6'])
        
        c3, c4, c5 = st.columns(3)
        with c3: 
            sub3_name = st.selectbox("Subject 3", ALL_SUBJECTS)
            sub3_grade = st.selectbox("Grade 3", ['None', 'A1', 'B2', 'B3', 'C4', 'C5', 'C6'])
        with c4: 
            sub4_name = st.selectbox("Subject 4", ALL_SUBJECTS)
            sub4_grade = st.selectbox("Grade 4", ['None', 'A1', 'B2', 'B3', 'C4', 'C5', 'C6'])
        with c5: 
            sub5_name = st.selectbox("Subject 5", ALL_SUBJECTS)
            sub5_grade = st.selectbox("Grade 5", ['None', 'A1', 'B2', 'B3', 'C4', 'C5', 'C6'])
        
        olevel = calculate_olevel_points([eng, mat, sub3_grade, sub4_grade, sub5_grade])
        intv = st.slider("Interview Score", 0, 100, 50)
        
        # 1. THE FORECAST BUTTON
        if st.button(translations[lang]["btn"], type="primary"):
            if not name.strip(): 
                st.error("⚠️ Oops! Don't forget to enter your name, superstar!")
            elif "None" in [eng, mat, sub3_grade, sub4_grade, sub5_grade]:
                st.error("⚠️ Hold on! Make sure you select grades for all 5 subjects.")
            else:
                with st.spinner('Analyzing your profile, hang tight... 🚀'):
                    try:
                        input_data = pd.DataFrame({"jamb_score": [jamb], "waec_points": [olevel], "interview_score": [intv]})
                        prob = float(pipeline.predict(input_data)[0])
                        status_text = "QUALIFIED" if prob >= 0.5 else "NOT QUALIFIED"
                        status = f"{status_text} ({prob:.1%})"
                        
                        save_data(name, status, f"{prob:.1%}", str(jamb), str(olevel), str(intv))
                        st.session_state.last_result = {"name": name, "status": status, "prob": prob, "jamb": jamb, "olevel": olevel, "intv": intv}
                        st.session_state.history.append(st.session_state.last_result)
                        st.rerun() 
                    except Exception as e:
                        st.error(f"⚠️ A glitch occurred: {e}")
                        st.session_state.last_result = None

    # 2. THE RESULT DISPLAY (Must be INSIDE the elif page block to access col1 and col2)
    if "last_result" in st.session_state and st.session_state.last_result:
        res = st.session_state.last_result
        
        with col1:
            if res['prob'] >= 0.5:
                st.success(f"Success! {res['status']}")
            else:
                st.toast('Keep pushing!', icon='💪')
                st.warning(f"Result: {res['status']}")
            
            if 'create_shareable_card' in globals():
                try:
                    card_path = create_shareable_card(res['name'], res['status'], res['jamb'], res['olevel'], res['intv'])
                    if card_path and os.path.exists(card_path):
                        with open(card_path, "rb") as file:
                            st.download_button("📸 Download Result Card!", file, "official_result_card.png", "image/png")
                except Exception as e:
                    st.error(f"Could not generate card: {e}")
        
        with col2:
            st.subheader(translations[lang]["roadmap"])
            tips = get_roadmap(res['jamb'], res['olevel'])
            for tip in tips: st.info(tip)
            st.info(f"🚀 **Insight Summary:** Focus on {'Interview skills' if res['intv'] < 60 else 'academic subjects'}.")
            df_plot = pd.DataFrame({"Metric": ["JAMB", "O-Level", "INT"], "Score": [res['jamb']/4, res['olevel'], res['intv']]})
            fig = px.bar(df_plot, x="Metric", y="Score", color="Score", color_continuous_scale="Blues")
            st.plotly_chart(fig, use_container_width=True)


                                                  

elif page == "Bulk Forecast":
    st.title("📂 Bulk Applicant Processing")
    st.write("Upload a CSV file containing columns: `jamb_score`, `olevel_points`, `interview_score`.")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            required = ['jamb_score', 'olevel_points', 'interview_score']
            if all(col in df.columns for col in required):
                st.success("File format verified!")
                st.write("### Preview of uploaded data:")
                st.dataframe(df.head())
                if st.button("Process Batch"):
                    df_to_predict = df.copy()
                    df_to_predict = df_to_predict.rename(columns={'olevel_points': 'waec_points'})
                    predictions = pipeline.predict(df_to_predict[['jamb_score', 'waec_points', 'interview_score']])
                    df['Probability'] = predictions
                    df['Status'] = df['Probability'].apply(lambda x: 'QUALIFIED' if x >= 0.5 else 'NOT QUALIFIED')
                    st.success("Processing Complete!")
                    st.dataframe(df)
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button("Download Full Report", csv, "results.csv", "text/csv")
            else:
                st.error(f"Missing columns! Your file must include: {required}")
        except Exception as e:
            st.error(f"Error processing file: {e}. Please ensure your CSV is properly formatted.")
            
elif page == "History Log":
    st.title("📜 Prediction History")

    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df)
    else:
        st.info("No records found in your database.")
        


elif page == "Export Reports":
    st.title("🖨️ Export Official Reports")
    
    if not st.session_state.history:
        st.info("No records found in history to export.")
    else:
        st.write("Click below to download professional student result cards:")
        
        for i, s in enumerate(st.session_state.history):
            with st.container():
                st.markdown(f'<div class="report-card">', unsafe_allow_html=True)
                st.write(f"**Student:** {s['name']} | **Status:** {s['status']}")
                
                # Generate the professional card for each history item
                # This uses your 5-argument function!
                card_path = create_shareable_card(s['name'], s['status'], s['jamb'], s['olevel'], s['intv'])
                
                if os.path.exists(card_path):
                    with open(card_path, "rb") as file:
                        st.download_button(
                            label=f"📸 Download {s['name']}'s Result Card",
                            data=file,
                            file_name=f"{s['name']}_result.png",
                            mime="image/png",
                            key=f"dl_card_btn_{i}"
                        )
                st.markdown('</div>', unsafe_allow_html=True)
    


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
