# 🌾 AgriAssist: AI-Powered Farm Planning & Disease Scanner

AgriAssist is an end-to-end, AI-driven web application designed to support the agriculture sector. It leverages Google Gemini's multimodal AI to provide actionable, bilingual (English/Urdu) insights for farmers, ranging from weather-based sowing schedules to visual crop disease diagnosis. 

## 🌍 Real-World Impact: The Monsoon Problem
Agriculture is highly vulnerable to unpredictable weather, especially during severe monsoon seasons. Recently, many farmers have suffered significant financial losses when heavy rains unexpectedly flooded fields and drowned newly sown crops. While we cannot control the weather, preparedness is the best defense. 

AgriAssist was built to tackle this exact vulnerability. By leveraging AI to analyze proposed planting dates against expected weather conditions, the app gives farmers the foresight they need. Whether it means shifting a sowing schedule earlier to avoid peak rains or switching to a more water-resilient seed variety, AgriAssist empowers farmers to plan proactively, mitigate risks, and protect their livelihoods from sudden climate shifts.

## 🚀 Live Demo
**[Click here to view the live application on Streamlit Cloud]** *(https://agriassistai.streamlit.app/)*

## ✨ Key Features

The application is divided into four primary modules, each featuring a continuous context-aware AI chat for follow-up questions:

* **🗓️ Date & Weather Advisor:** Analyzes geographical locations (e.g., Punjab, Sindh) and planting dates against typical monsoon/weather patterns. It recommends optimal sowing windows and tailored fertilizer plans to prevent weather-related crop failure.
* **🌱 Seed Explorer:** Acts as a knowledge base for modern, high-yield seed varieties, detailing their drought resistance, pest resilience, and maturity durations.
* **📈 Yield Optimizer:** Generates step-by-step agricultural strategies based on specific crop types, existing soil conditions (Clay, Sandy, Loam, etc.), and current fertilizer usage.
* **🍃 Disease Scanner:** Utilizes computer vision via Gemini's multimodal capabilities to analyze uploaded leaf photos (JPG/PNG). It identifies visible plant diseases, pest damage, or nutrient deficiencies and provides a 3-step treatment action plan.
* **💬 Contextual AI Chat:** Every module includes an inline chat system powered by Streamlit Session State, allowing users to ask natural, follow-up questions about their specific results without losing context.
* **🌐 Bilingual Output:** Full support for generating AI responses and chat interactions in both English and Urdu (اردو) to ensure accessibility for local farming communities.

## 🛠️ Technology Stack

* **Frontend & Framework:** Streamlit (Python)
* **Artificial Intelligence:** Google GenAI SDK (`gemini-3.6-flash` model)
* **Image Processing:** Pillow (PIL)
* **Deployment:** Streamlit Community Cloud
* **Version Control:** Git & GitHub

## 💻 Local Installation & Setup

If you wish to run this application locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/abdulrehmanmand/AgriAssist-AI.git]
   cd AgriAssist-AI
