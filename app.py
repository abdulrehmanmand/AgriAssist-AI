import streamlit as st
from google import genai
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="AgriAssist: Farm AI", page_icon="🌾", layout="centered")
st.title("🌾 AgriAssist: Farm Planning & Yield AI")
st.write("Plan your sowing around monsoons, optimize crop yields, and scan for plant diseases.")

# 2. Sidebar API Setup
st.sidebar.header("🔑 Setup")
api_key = st.sidebar.text_input("Enter your Google Gemini API Key:", type="password")

if not api_key:
    st.warning("👈 Please enter your Gemini API Key in the sidebar to activate the AI features.")
    st.stop()

# Initialize Google GenAI client
client = genai.Client(api_key=api_key)

# 3. Create Navigation Tabs
tab1, tab2, tab3 = st.tabs(["🌧️ Monsoon Sowing", "📈 Yield Optimizer", "🍃 Disease Scanner"])

# --- TAB 1: MONSOON & SOWING PLANNER ---
with tab1:
    st.header("Plan Sowing Around Monsoons")
    crop = st.text_input("What crop are you planting?", placeholder="e.g., Wheat, Rice, Cotton")
    region = st.text_input("Farm Location / Region:", placeholder="e.g., Punjab, Sindh, Lahore")
    monsoon_date = st.date_input("Expected start of heavy monsoon rains:")
    
    if st.button("Generate Sowing Plan"):
        if crop and region:
            with st.spinner("Analyzing weather windows and crop cycles..."):
                prompt = (
                    f"I am a farmer in {region} planning to grow {crop}. "
                    f"Heavy monsoon rains are expected to start around {monsoon_date}. "
                    f"Provide an actionable plan detailing:\n"
                    f"1. The exact optimal window to sow seeds to prevent seed washout.\n"
                    f"2. Necessary soil preparation techniques before heavy rains.\n"
                    f"3. Initial drainage strategies."
                )
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                st.success("Plan Generated!")
                st.markdown(response.text)
        else:
            st.error("Please fill in both the crop type and location.")

# --- TAB 2: YIELD OPTIMIZER ---
with tab2:
    st.header("Maximize Your Harvest")
    yield_crop = st.text_input("Target Crop:", placeholder="e.g., Maize, Sugarcane")
    soil_type = st.selectbox("Soil Condition:", ["Clay", "Sandy", "Loam", "Silt", "Peat"])
    fertilizer = st.text_input("Current Fertilizers / Management:", placeholder="e.g., Urea, NPK 15-15-15")
    
    if st.button("Optimize Yield"):
        if yield_crop:
            with st.spinner("Calculating optimal crop strategy..."):
                prompt = (
                    f"I am growing {yield_crop} in {soil_type} soil using {fertilizer}. "
                    f"Provide a step-by-step agronomic plan to achieve maximum yield, including:\n"
                    f"1. Recommended fertilizer adjustments and application schedule.\n"
                    f"2. Optimized irrigation timing.\n"
                    f"3. Key growth stage interventions."
                )
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                st.success("Optimization Plan Ready!")
                st.markdown(response.text)
        else:
            st.error("Please specify a target crop.")

# --- TAB 3: CROP DISEASE SCANNER ---
with tab3:
    st.header("Identify Crop Diseases")
    uploaded_file = st.file_uploader("Upload a clear photo of a sick leaf or plant...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Plant Sample", use_container_width=True)
        
        if st.button("Scan Plant Image"):
            with st.spinner("Analyzing image with Vision AI..."):
                prompt = (
                    "You are an expert agronomist. Examine this image carefully and provide:\n"
                    "1. Diagnosis: Potential disease, pest infestation, or nutrient deficiency.\n"
                    "2. Symptoms: Key visible signs on the leaf/plant.\n"
                    "3. Action Plan: Organic or chemical treatment steps to cure or contain the issue."
                )
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[prompt, image]
                )
                st.success("Diagnosis Complete!")
                st.markdown(response.text)
