import streamlit as st
import replicate
import requests
from PIL import Image
from io import BytesIO
import os

# إعداد الصفحة
st.set_page_config(page_title="Ghibli Style Generator", layout="centered")
st.title("Ghibli Style Image Generator")

# جلب التوكن من أسرار ستريملت
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
replicate_client = replicate.Client(api_token=REPLICATE_API_TOKEN)

# رفع الصورة
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Original Image", use_container_width=True)

    if st.button("Generate Ghibli Image"):
        with st.spinner("Generating..."):
            try:
                output = replicate_client.run(
                    "lucataco/ghibli-diffusion:5fb473f6bfb2cf2b0e6b735a6a91a6d9a97cf8c3b18fc3a1541fca7ba55a54c3",
                    input={"image": uploaded_file}
                )
                result_url = output["output"]
                st.image(result_url, caption="Ghibli Image", use_container_width=True)
                st.markdown(f"[Download Image]({result_url})")

            except Exception as e:
                st.error(f"Error generating image: {e}")
