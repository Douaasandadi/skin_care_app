import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Smart Skin Care Assistant")
st.title("✨ Smart Skin Care Assistant (Gemini)")

api_key = st.text_input("Enter your Google Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    # هادو هما الموديلات اللي خدامين دابا
    model = genai.GenerativeModel("gemini-3.8-flash") 

    uploaded_file = st.file_uploader("Choose or take a photo", type=["jpg","png","jpeg"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        if st.button("Analyze Skin"):
            with st.spinner("كَنحلل..."):
                try:
                    prompt = """
                    أنت مساعد معلوماتي عام حول نظافة البشرة فقط.
                    لا تقدم تشخيص طبي أبدا. لا تذكر اسم مرض.
                    صف ما تراه بوصف عام فقط (مثال: احمرار خفيف، مسام، جفاف)
                    ثم قدم 3 نصائح عامة للنظافة (غسول لطيف، ترطيب non-comedogenic، واقي شمس)
                    وختم بهذه الجملة حرفيا: هذه معلومات عامة فقط، ليست تشخيص طبي، يرجى استشارة صيدلي أو طبيب جلد إذا استمر الأمر.
                    """
                    response = model.generate_content([prompt, image])
                    st.success("النتيجة:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
