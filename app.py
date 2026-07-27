import streamlit as st
from google import genai
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="AgriAssist: Farm AI", page_icon="🌾", layout="centered")
st.title("🌾 AgriAssist: Farm Planning & Yield AI")
st.write("Plan your sowing, optimize your yield, and scan for crop diseases.")

# 2. Smart API Key Detection (Checks Secrets first, then sidebar)
api_key = None

if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    st.sidebar.header("Setup")
    api_key = st.sidebar.text_input("Enter your Google Gemini API Key:", type="password")

if not api_key:
    st.warning("👈 Please enter your Gemini API Key in the sidebar to start.")
    st.stop()

# Configure the GenAI client
client = genai.Client(api_key=api_key)

# 3. Create App Tabs
tab1, tab2, tab3 = st.tabs(["🌧️ Monsoon Sowing", "📈 Yield Optimizer", "🍃 Disease Scanner"])

# --- TAB 1: SOWING & MONSOON PLANNER ---
with tab1:
    st.header("Plan Sowing Around Monsoons")
    crop = st.text_input("What crop are you planting? (e.g., Wheat, Rice, Cotton)")
    region = st.text_input("Farm location (City/Region):")
    monsoon_date = st.date_input("Expected start of heavy monsoon rains:")
    
    if st.button("Generate Sowing Plan"):
        with st.spinner("Analyzing weather and crop data..."):
            prompt = f"I am a farmer in {region} planting {crop}. Heavy monsoons start {monsoon_date}. When is the exact optimal time to sow seeds to prevent washout, and what soil prep is needed?"
            
            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt
            )
            st.success("Plan Generated!")
            st.write(response.text)

# --- TAB 2: YIELD OPTIMIZER ---
with tab2:
    st.header("Maximize Your Harvest")
    yield_crop = st.text_input("Crop type:")
    soil_type = st.selectbox("Soil Condition:", ["Clay", "Sandy", "Loam", "Silt", "Peat"])
    fertilizer = st.text_input("Current fertilizers:")
    
    if st.button("Optimize Yield"):
        with st.spinner("Calculating strategy..."):
            prompt = f"Growing {yield_crop} in {soil_type} soil using {fertilizer}. Give a step-by-step plan to maximize final crop yield, including irrigation and fertilizer adjustments."
            
            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt
            )
            st.success("Optimization Ready!")
            st.write(response.text)

# --- TAB 3: CROP DISEASE SCANNER ---
with tab3:
    st.header("Identify Crop Diseases")
    uploaded_file = st.file_uploader("Upload a leaf photo...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        if st.button("Scan for Disease"):
            with st.spinner("Analyzing image..."):
                prompt = "Identify any visible plant disease, pest damage, or deficiency in this leaf photo and give a 3-step action plan for treatment."
                response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=[prompt, image]
                )
                st.success("Analysis Complete!")
                st.write(response.text)
