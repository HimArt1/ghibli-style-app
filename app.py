import streamlit as st
import replicate
import requests
from PIL import Image
from io import BytesIO
import os

# إعداد التوكن من secrets
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
replicate_client = replicate.Client(api_token=REPLICATE_API_TOKEN)

# واجهة التطبيق
st.set_page_config(page_title="Ghibli Style Generator", layout="centered")
st.title("Ghibli Style Image Generator")
st.markdown("Upload an image and transform it into a dreamy Studio Ghibli style!")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image_bytes = uploaded_file.read()
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    st.image(image, caption="Original Image", use_container_width=True)

    if st.button("Generate Ghibli Image"):
        with st.spinner("Generating image..."):
            try:
                output = replicate_client.run(
                    "cjwbw/anything-v4.0",
                    input={
                        "image": BytesIO(image_bytes),
                        "prompt": "Ghibli style, soft background, dreamy anime landscape",
                        "width": 512,
                        "height": 512,
                        "num_inference_steps": 30,
                        "guidance_scale": 7.5,
                        "strength": 0.65
                    }
                )

                output_url = output[0] if isinstance(output, list) else output
                response = requests.get(output_url)
                result_image = Image.open(BytesIO(response.content))
                st.image(result_image, caption="Ghibli Result", use_container_width=True)
                st.markdown(f"[Download Image]({output_url})")

            except Exception as e:
                st.error(f"Error generating image: {e}")
