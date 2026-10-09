import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Smart Skin Care Assistant", page_icon="✨")

st.title("✨ Smart Skin Care Assistant (Gemini)")
st.write("Upload a photo of your face or the area you want to check, and Gemini AI will analyze it and provide a suitable skincare routine.")

# Enter Google Gemini API Key (Free)
api_key = st.text_input("Enter your Google Gemini API Key:", type="password")

uploaded_file = st.file_uploader("Choose or take a photo of your skin...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Skin Image', use_column_width=True)
    
    if st.button("Analyze Skin"):
        if not api_key:
            st.error("Please enter your Gemini API Key first!")
        else:
            try:
                genai.configure(api_key=api_key)
                # Call Gemini model capable of analyzing images
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                with st.spinner('Analyzing your skin with Gemini...'):
                    prompt = "You are a professional dermatologist. Analyze this skin image, identify any visible issues (like acne, dryness, redness, etc.), and provide a structured, helpful skincare routine and recommendations."
                    response = model.generate_content([prompt, image])
                    
                    st.subheader("Skincare Analysis & Routine:")
                    st.write(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")
                              
