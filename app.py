import base64
import streamlit as st
from openai import OpenAI

# Page configuration
st.set_page_config(page_title="Smart Skin Care Assistant", page_icon="✨", layout="centered")

st.title("✨ Smart Skin Care Assistant")
st.write(
    "Upload a photo of your face or the area you want to check, and the AI will analyze it and provide a suitable skincare routine."
)

# OpenAI API Key input
api_key = st.text_input("Enter your OpenAI API Key:", type="password")

# File uploader for image (supports camera or gallery on mobile)
uploaded_file = st.file_uploader(
    "Choose or take a photo of your skin...", type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
  # Display the uploaded image
  st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

  if st.button("Analyze Skin Now"):
    if not api_key:
      st.error("Please enter your API Key first!")
    else:
      with st.spinner("Analyzing skin and preparing recommendations..."):
        try:
          client = OpenAI(api_key=api_key)

          # Convert image to base64 format for the model
          image_bytes = uploaded_file.getvalue()
          base64_image = base64.b64encode(image_bytes).decode("utf-8")

          # Send request to GPT-4o
          response = client.chat.completions.create(
              model="gpt-4o",
              messages=[
                  {
                      "role": "system",
                      "content": (
                          "You are an intelligent assistant specialized in skincare. "
                          "Analyze the image and provide cosmetic advice and a suitable skincare routine. "
                          "Include a disclaimer stating that this is not a final medical diagnosis and that a specialist "
                          "doctor should be consulted if needed."
                      ),
                  },
                  {
                      "role": "user",
                      "content": [
                          {
                              "type": "text",
                              "text": (
                                  "What are your observations on my skin and what is the suitable routine?"
                              ),
                          },
                          {
                              "type": "image_url",
                              "image_url": {
                                  "url": f"data:image/jpeg;base64,{base64_image}"
                              },
                          },
                      ],
                  },
              ],
              max_tokens=600,
          )

          # Display the result
          st.success("Analysis completed successfully!")
          st.markdown("### 🧴 Results & Personalized Recommendations:")
          st.write(response.choices[0].message.content)

        except Exception as e:
          st.error(f"An error occurred: {e}")