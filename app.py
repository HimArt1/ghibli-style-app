import streamlit as st
import replicate
import requests
from PIL import Image
from io import BytesIO
import os

# إعداد الصفحة
st.set_page_config(page_title="Ghibli Style Generator", layout="centered")
st.title("Ghibli Style Image Generator")
st.markdown("Upload an image and transform it into a dreamy Ghibli-style artwork!")

# الحصول على التوكن من ستريملت سكريتس
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
replicate_client = replicate.Client(api_token=REPLICATE_API_TOKEN)

# رفع صورة
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image_bytes = uploaded_file.read()
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    st.image(image, caption="Original Image", use_container_width=True)

    prompt = st.text_input("Describe your Ghibli scene", value="ghibli style, dreamy background, soft lighting")

    if st.button("Generate Ghibli-style Image"):
        with st.spinner("Generating image... please wait"):
            try:
                output = replicate_client.run(
                    "stability-ai/sdxl",
                    input={
                        "prompt": prompt,
                        "image": BytesIO(image_bytes),
                        "strength": 0.7,
                        "num_inference_steps": 30,
                        "guidance_scale": 7.5
                    }
                )

                result_url = output[0] if isinstance(output, list) else output
                response = requests.get(result_url)
                result_image = Image.open(BytesIO(response.content))
                st.success("Done! Here's your Ghibli-style image")
                st.image(result_image, caption="Ghibli Result", use_container_width=True)
                st.markdown(f"[Download Image]({result_url})")

            except Exception as e:
                st.error(f"Error generating image: {e}")
