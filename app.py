import streamlit as st
import replicate
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Ghibli Image Converter", layout="centered")
st.title("Ghibli Style Image Converter")
st.markdown("Upload any image and transform it into a dreamy Ghibli-style scene!")

REPLICATE_API_TOKEN = "your_replicate_api_token_here"
replicate_client = replicate.Client(api_token=REPLICATE_API_TOKEN)

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Original Image", use_column_width=True)

    if st.button("Convert to Ghibli Style"):
        with st.spinner("Transforming..."):
            output = replicate_client.run(
                "fofr/anything-v4.0:7e0c09fc79ee8b19d4f804a8d3da8cf7e811b148a772dfb671a2c7c00c2c3c3b",
                input={
                    "image": uploaded_file,
                    "prompt": "ghibli style, dreamy, soft colors, anime background, magical vibe",
                    "num_inference_steps": 30,
                    "guidance_scale": 7.5,
                    "width": 512,
                    "height": 512
                }
            )

            response = requests.get(output)
            result_image = Image.open(BytesIO(response.content))
            st.image(result_image, caption="Ghibli Style Image", use_column_width=True)
            st.markdown(f"[Download Image]({output})")
