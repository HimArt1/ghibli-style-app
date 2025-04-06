import streamlit as st
import replicate
import os
import requests
from PIL import Image
from io import BytesIO
import base64

# إعداد التوكن
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
replicate.Client(api_token=REPLICATE_API_TOKEN)

# إعداد الصفحة
st.set_page_config(page_title="Anime Style Generator")
st.title("Anime Style Image Generator")
st.markdown("Upload your photo and get an anime-style version!")

# رفع صورة
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# وصف المشهد
prompt = st.text_input("Describe the anime scene", value="a dreamy anime landscape, ghibli style")

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Original Image", use_container_width=True)

    # تحويل الصورة إلى base64
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    if st.button("Generate Anime Image"):
        with st.spinner("Generating..."):
            try:
                output = replicate.run(
                    "cjwbw/anything-v3-better-vae:db21e45c2f2eb1a1b8e079b1671ec9bfa16e14221f5cb3d47d08c5863b2c982b",
                    input={
                        "prompt": prompt,
                        "image": f"data:image/png;base64,{img_str}",
                        "scale": 7,
                        "steps": 30,
                        "strength": 0.6,
                        "scheduler": "K_EULER_ANCESTRAL"
                    }
                )

                # عرض الصورة الناتجة
                result_url = output["image"]
                st.image(result_url, caption="Anime-style Result", use_container_width=True)
                st.markdown(f"[Download Image]({result_url})")

            except Exception as e:
                st.error(f"Error generating image: {e}")
