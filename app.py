import streamlit as st
import replicate
import requests
from PIL import Image
from io import BytesIO
import os

# إعداد الصفحة
st.set_page_config(page_title="Ghibli Style Image Generator", layout="centered")
st.title("Ghibli Style Image Generator")
st.markdown("Upload a photo and generate a dreamy Ghibli-style anime image!")

# تحميل التوكن من secrets
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
replicate.Client(api_token=REPLICATE_API_TOKEN)

# رفع صورة
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
prompt = st.text_input("Describe the Ghibli scene", value="ghibli style anime, dreamy landscape")

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Original Image", use_column_width=True)

    if st.button("Generate Ghibli-style Image"):
        with st.spinner("Generating..."):
            try:
                # رفع الصورة إلى موقع مؤقت
                image_bytes = BytesIO()
                image.save(image_bytes, format="PNG")
                image_bytes.seek(0)
                response = requests.post("https://api.imgbb.com/1/upload", {
                    "key": "YOUR_IMGBB_API_KEY",  # استبدل هذا بمفتاح imgbb الخاص بك (مجاني)
                }, files={"image": image_bytes})
                image_url = response.json()["data"]["url"]

                # استدعاء نموذج مجاني
                output = replicate.run(
                    "lucataco/animagine-xl",
                    input={"prompt": prompt, "image": image_url}
                )

                st.image(output, caption="Ghibli-style Image", use_column_width=True)

            except Exception as e:
                st.error(f"Error generating image: {e}")
