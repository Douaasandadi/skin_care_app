import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Smart Skin Care Assistant", page_icon="✨")
st.title("✨ Smart Skin Care - نصائح عامة")
st.write("هاد التطبيق كيعطي نصائح عامة للنظافة فقط، ماشي تشخيص طبي.")

# 1. API Key
api_key = st.text_input("دخل Google Gemini API Key ديالك:", type="password")

if not api_key:
    st.info("دخل الـ API Key باش يخدم التطبيق.")
    st.stop()

genai.configure(api_key=api_key)

# 2. استعمل موديل اللي خدام دابا ومكيبلوكيش
# جربنا 3.8-flash و flash-latest هما اللي خدامين
model = genai.GenerativeModel("gemini-flash-latest")

uploaded_file = st.file_uploader("حط تصويرة واضحة (غير للوجه قريبة)", type=["jpg","jpeg","png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Get General Tips"):
        with st.spinner("كنوجد ليك نصائح عامة..."):
            try:
                prompt = """
                You are a general cosmetic hygiene assistant.
                DO NOT provide medical diagnosis. DO NOT name any disease or skin condition.
                Only describe the image in general cosmetic terms like lighting, general appearance.
                Then give 3 short general hygiene tips: gentle cleanser, non-comedogenic moisturizer, sunscreen.
                End with exactly this sentence in Arabic: هذه معلومات تجميلية عامة فقط وليست نصيحة طبية، يرجى استشارة صيدلي أو طبيب إذا لزم الأمر.
                Keep it short and friendly.
                """

                response = model.generate_content([prompt, image])
                st.success("النتيجة - نصائح عامة:")
                st.write(response.text)

            except Exception as e:
                st.error(f"Error: {e}")
                st.warning("إلا شفتي Error 403: سيري لـ aistudio.google.com وديري Create API Key in NEW project، حيث القديم تبلوكا.")
