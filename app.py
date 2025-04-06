import streamlit as st
import replicate
import requests
from PIL import Image
from io import BytesIO

# إعداد الصفحة
st.set_page_config(page_title="Ghibli Style Image Generator", layout="centered")
st.title("Ghibli Style Image Generator")
st.markdown("Upload an image and transform it into a dreamy Ghibli-style scene.")

# مفتاح Replicate
REPLICATE_API_TOKEN = "r8_dIxABC123xyz456"
replicate_client = replicate.Client(api_token=REPLICATE_API_TOKEN)

# رفع الصورة
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Original Image", use_container_width=True)

    if st.button("Generate Ghibli Image"):
        with st.spinner("Creating Ghibli-style art..."):
            try:
                # إرسال الصورة كنص بايت
                output = replicate_client.run(
                    "cjwbw/anything-v4.0",  # نموذج Stable Diffusion متوافق
                    input={
                        "prompt": "ghibli style, anime scene, dreamy, vibrant colors, soft light",
                        "image": BytesIO(uploaded_file.read()),
                        "width": 512,
                        "height": 512,
                        "strength": 0.6,
                        "num_inference_steps": 30,
                        "guidance_scale": 7.5
                    }
                )

                # عرض النتيجة
                if isinstance(output, list):
                    output_url = output[0]
                else:
                    output_url = output

                response = requests.get(output_url)
                result = Image.open(BytesIO(response.content))
                st.image(result, caption="Ghibli Style Result", use_container_width=True)
                st.markdown(f"[Download Image]({output_url})")

            except Exception as e:
                st.error(f"Error generating image: {e}")
