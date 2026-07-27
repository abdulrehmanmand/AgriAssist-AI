import streamlit as st
from google import genai
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="AgriAssist: Farm AI", page_icon="🌾", layout="centered")

# 2. Header
st.title("🌾 AgriAssist")
st.write("Smart Farm Planning, Seed Explorer & Disease AI")

# 3. API Key Handling
api_key = None
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("🔑 Enter your Gemini API Key:", type="password")

if not api_key:
    st.warning("👈 Please enter your Gemini API Key in the sidebar to start.")
    st.stop()

client = genai.Client(api_key=api_key)
MODEL_ID = "gemini-3.6-flash"

# 4. Create App Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🗓️ Date & Weather Advisor", 
    "🌱 Seed Explorer", 
    "📈 Yield Optimizer", 
    "🍃 Disease Scanner"
])

# --- TAB 1: DATE & WEATHER ADVISOR ---
with tab1:
    st.header("Sowing Advisor & Weather Check")
    st.write("Input your date to get weather predictions, recommended seeds, and a fertilizer plan.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        region = st.text_input("Farm location (e.g., Punjab, Sindh):", key="loc_1")
        crop = st.text_input("Crop to plant (e.g., Rice, Wheat):", key="crop_1")
    with col_b:
        sow_date = st.date_input("Planned Sowing Date:")
        
    st.write("---")
    col_btn1, col_lang1 = st.columns(2)
    with col_lang1:
        lang1 = st.radio("Select Output Language:", options=["English", "Urdu (اردو)"], index=0, key="lang_t1", horizontal=True)
    with col_btn1:
        st.write("")
        btn1 = st.button("Check Date & Generate Plan", key="b_1")
        
    # Generate Initial Response
    if btn1:
        with st.spinner("Analyzing weather, seeds, and fertilizer needs..."):
            prompt = f"""
            I am a farmer in {region} planning to sow {crop} on {sow_date}. 
            1. Analyze the typical weather and monsoon conditions for this exact date. Is it a safe and optimal time to sow?
            2. If yes, what specific seed varieties are most appropriate for this date and weather?
            3. Provide a tailored fertilizer plan.
            Please provide the entire response in {lang1}.
            """
            response = client.models.generate_content(model=MODEL_ID, contents=prompt)
            st.session_state.chat_t1 = [("assistant", response.text)]
            st.session_state.ctx_t1 = prompt 
            
    # Render Chat History & Follow-up
    if "chat_t1" in st.session_state:
        st.write("---")
        st.subheader("💬 Discuss this Plan")
        for role, msg in st.session_state.chat_t1:
            with st.chat_message(role): st.write(msg)
            
        follow_up1 = st.chat_input("Ask a follow-up question...", key="in_t1")
        if follow_up1:
            st.session_state.chat_t1.append(("user", follow_up1))
            
            with st.spinner("Thinking..."):
                hist_text = f"Original Context: {st.session_state.ctx_t1}\n"
                for r, m in st.session_state.chat_t1: hist_text += f"{r.upper()}: {m}\n"
                hist_text += f"Answer the user's latest question in {lang1}."
                
                res = client.models.generate_content(model=MODEL_ID, contents=hist_text)
                st.session_state.chat_t1.append(("assistant", res.text))
            st.rerun()

# --- TAB 2: SEED EXPLORER ---
with tab2:
    st.header("Seed Variety Explorer")
    st.write("Discover the latest high-yield seeds for your region.")
    
    explore_crop = st.selectbox("Select a Crop:", ["Rice", "Wheat", "Corn", "Cotton", "Sugarcane", "Other"], key="exp_crop")
    if explore_crop == "Other":
        explore_crop = st.text_input("Type the crop name:", key="other_crop")
        
    st.write("---")
    col_btn2, col_lang2 = st.columns(2)
    with col_lang2:
        lang2 = st.radio("Select Output Language:", options=["English", "Urdu (اردو)"], index=0, key="lang_t2", horizontal=True)
    with col_btn2:
        st.write("")
        btn2 = st.button("Explore Seeds", key="b_2")
        
    if btn2:
        with st.spinner("Fetching seed database..."):
            prompt = f"""
            Provide a comprehensive guide on the best modern seed varieties available for {explore_crop}. 
            Include characteristics, drought/pest resistance, and yield potential.
            Please provide the entire response in {lang2}.
            """
            response = client.models.generate_content(model=MODEL_ID, contents=prompt)
            st.session_state.chat_t2 = [("assistant", response.text)]
            st.session_state.ctx_t2 = prompt
            
    if "chat_t2" in st.session_state:
        st.write("---")
        st.subheader("💬 Ask About These Seeds")
        for role, msg in st.session_state.chat_t2:
            with st.chat_message(role): st.write(msg)
            
        follow_up2 = st.chat_input("Ask a follow-up question...", key="in_t2")
        if follow_up2:
            st.session_state.chat_t2.append(("user", follow_up2))
            with st.spinner("Thinking..."):
                hist_text = f"Original Context: {st.session_state.ctx_t2}\n"
                for r, m in st.session_state.chat_t2: hist_text += f"{r.upper()}: {m}\n"
                hist_text += f"Answer the user's latest question in {lang2}."
                
                res = client.models.generate_content(model=MODEL_ID, contents=hist_text)
                st.session_state.chat_t2.append(("assistant", res.text))
            st.rerun()

# --- TAB 3: YIELD OPTIMIZER ---
with tab3:
    st.header("Maximize Your Harvest")
    yield_crop = st.text_input("Crop type:", key="ycrop_3")
    soil_type = st.selectbox("Soil Condition:", ["Clay", "Sandy", "Loam", "Silt", "Peat"], key="soil_3")
    fertilizer = st.text_input("Current fertilizers:", key="fert_3")
    
    st.write("---")
    col_btn3, col_lang3 = st.columns(2)
    with col_lang3:
        lang3 = st.radio("Select Output Language:", options=["English", "Urdu (اردو)"], index=0, key="lang_t3", horizontal=True)
    with col_btn3:
        st.write("")
        btn3 = st.button("Optimize Yield", key="b_3")
        
    if btn3:
        with st.spinner("Calculating strategy..."):
            prompt = f"""
            Growing {yield_crop} in {soil_type} soil using {fertilizer}. Give a step-by-step plan to maximize final crop yield.
            Please provide the entire response in {lang3}.
            """
            response = client.models.generate_content(model=MODEL_ID, contents=prompt)
            st.session_state.chat_t3 = [("assistant", response.text)]
            st.session_state.ctx_t3 = prompt
            
    if "chat_t3" in st.session_state:
        st.write("---")
        st.subheader("💬 Adjust Your Plan")
        for role, msg in st.session_state.chat_t3:
            with st.chat_message(role): st.write(msg)
            
        follow_up3 = st.chat_input("Ask a follow-up question...", key="in_t3")
        if follow_up3:
            st.session_state.chat_t3.append(("user", follow_up3))
            with st.spinner("Thinking..."):
                hist_text = f"Original Context: {st.session_state.ctx_t3}\n"
                for r, m in st.session_state.chat_t3: hist_text += f"{r.upper()}: {m}\n"
                hist_text += f"Answer the user's latest question in {lang3}."
                
                res = client.models.generate_content(model=MODEL_ID, contents=hist_text)
                st.session_state.chat_t3.append(("assistant", res.text))
            st.rerun()

# --- TAB 4: CROP DISEASE SCANNER ---
with tab4:
    st.header("Identify Crop Diseases")
    uploaded_file = st.file_uploader("Upload a leaf photo...", type=["jpg", "jpeg", "png"], key="img_4")
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        
        st.write("---")
        col_btn4, col_lang4 = st.columns(2)
        with col_lang4:
            lang4 = st.radio("Select Output Language:", options=["English", "Urdu (اردو)"], index=0, key="lang_t4", horizontal=True)
        with col_btn4:
            st.write("")
            btn4 = st.button("Scan for Disease", key="b_4")
        
        if btn4:
            with st.spinner("Analyzing image..."):
                prompt = f"""
                Identify any visible plant disease, pest damage, or deficiency in this leaf photo and give an action plan for treatment.
                Please provide the entire response in {lang4}.
                """
                response = client.models.generate_content(model=MODEL_ID, contents=[prompt, image])
                
                st.session_state.chat_t4 = [("assistant", response.text)]
                st.session_state.ctx_t4 = prompt
                st.session_state.saved_img = image 
                
        if "chat_t4" in st.session_state:
            st.write("---")
            st.subheader("💬 Discuss Diagnosis")
            for role, msg in st.session_state.chat_t4:
                with st.chat_message(role): st.write(msg)
                
            follow_up4 = st.chat_input("Ask a follow-up question...", key="in_t4")
            if follow_up4:
                st.session_state.chat_t4.append(("user", follow_up4))
                with st.spinner("Thinking..."):
                    hist_text = f"Original Context: {st.session_state.ctx_t4}\n"
                    for r, m in st.session_state.chat_t4: hist_text += f"{r.upper()}: {m}\n"
                    hist_text += f"Answer the user's latest question about the uploaded image in {lang4}."
                    
                    res = client.models.generate_content(
                        model=MODEL_ID, 
                        contents=[hist_text, st.session_state.saved_img]
                    )
                    st.session_state.chat_t4.append(("assistant", res.text))
                st.rerun()
