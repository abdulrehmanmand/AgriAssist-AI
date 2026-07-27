import streamlit as st
from google import genai
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="AgriAssist: Farm AI", page_icon="🌾", layout="centered")
st.title("🌾 AgriAssist: Smart Farm & Seed AI")

# 2. Setup & Localization in Sidebar
st.sidebar.header("⚙️ Setup & Language")

# Language Selector
language = st.sidebar.selectbox(
    "Select Language / زبان منتخب کریں", 
    ["English", "Urdu (اردو)", "Roman Urdu"]
)
# This prompt gets secretly attached to every AI request
lang_prompt = f"Please provide the entire response in {language}."

# API Key Handling (Checks Secrets first, then sidebar)
api_key = None
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Enter your Google Gemini API Key:", type="password")

if not api_key:
    st.warning("👈 Please enter your Gemini API Key in the sidebar to start.")
    st.stop()

# Configure the GenAI client with the latest 2026 model
client = genai.Client(api_key=api_key)
MODEL_ID = "gemini-3.6-flash"

# 3. Create App Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🗓️ Date & Weather Advisor", 
    "🌱 Seed Explorer", 
    "📈 Yield Optimizer", 
    "🍃 Disease Scanner"
])

# --- TAB 1: DATE & WEATHER ADVISOR ---
with tab1:
    st.header("Sowing Advisor & Weather Check")
    st.write("Input your date to get weather predictions, recommended seeds, and a specific fertilizer plan.")
    
    col1, col2 = st.columns(2)
    with col1:
        region = st.text_input("Farm location (e.g., Punjab, Sindh):")
        crop = st.text_input("Crop to plant (e.g., Rice, Wheat):")
    with col2:
        sow_date = st.date_input("Planned Sowing Date:")
        
    if st.button("Check Date & Generate Plan"):
        with st.spinner("Analyzing weather, seeds, and fertilizer needs..."):
            prompt = f"""
            I am a farmer in {region} planning to sow {crop} on {sow_date}. 
            1. Analyze the typical weather and monsoon conditions for this exact date. Is it a safe and optimal time to sow? Will the crop grow perfectly?
            2. If yes, what specific seed varieties are most appropriate for this exact date and weather? (If no, suggest a better date).
            3. Provide a tailored fertilizer plan specifically for the recommended seeds.
            {lang_prompt}
            """
            response = client.models.generate_content(model=MODEL_ID, contents=prompt)
            st.success("Plan Generated!")
            st.write(response.text)

# --- TAB 2: SEED EXPLORER (KNOWLEDGE BASE) ---
with tab2:
    st.header("Seed Variety Explorer")
    st.write("Discover the latest high-yield seeds for your region.")
    
    explore_crop = st.selectbox("Select a Crop:", ["Rice", "Wheat", "Corn", "Cotton", "Sugarcane", "Other"])
    if explore_crop == "Other":
        explore_crop = st.text_input("Type the crop name:")
        
    if st.button("Explore Seeds"):
        with st.spinner("Fetching seed database..."):
            prompt = f"""
            Provide a comprehensive guide on the best modern seed varieties available for {explore_crop}. 
            Include their characteristics, drought/pest resistance, maturity duration, and expected yield potential.
            {lang_prompt}
            """
            response = client.models.generate_content(model=MODEL_ID, contents=prompt)
            st.write(response.text)

# --- TAB 3: YIELD OPTIMIZER ---
with tab3:
    st.header("Maximize Your Harvest")
    yield_crop = st.text_input("Crop type:")
    soil_type = st.selectbox("Soil Condition:", ["Clay", "Sandy", "Loam", "Silt", "Peat"])
    fertilizer = st.text_input("Current fertilizers:")
    
    if st.button("Optimize Yield"):
        with st.spinner("Calculating strategy..."):
            prompt = f"""
            Growing {yield_crop} in {soil_type} soil using {fertilizer}. Give a step-by-step plan to maximize final crop yield, including irrigation and fertilizer adjustments.
            {lang_prompt}
            """
            response = client.models.generate_content(model=MODEL_ID, contents=prompt)
            st.success("Optimization Ready!")
            st.write(response.text)

# --- TAB 4: CROP DISEASE SCANNER ---
with tab4:
    st.header("Identify Crop Diseases")
    uploaded_file = st.file_uploader("Upload a leaf photo...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        if st.button("Scan for Disease"):
            with st.spinner("Analyzing image..."):
                prompt = f"""
                Identify any visible plant disease, pest damage, or deficiency in this leaf photo and give a 3-step action plan for treatment.
                {lang_prompt}
                """
                response = client.models.generate_content(model=MODEL_ID, contents=[prompt, image])
                st.success("Analysis Complete!")
                st.write(response.text)
