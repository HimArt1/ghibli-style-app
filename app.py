import streamlit as st
import replicate
import requests
from PIL import Image
from io import BytesIO

# إعداد الصفحة
st.set_page_config(page_title="Ghibli Style Converter", layout="centered")
st.title("Ghibli Style Image Converter")
st.markdown("Upload an image and click the button below to generate a dreamy Ghibli-style scene!")

# مفتاح Replicate API
REPLICATE_API_TOKEN = "ضع_توكن_Replicate_هنا"
replicate_client = replicate.Client(api_token=REPLICATE_API_TOKEN)

# واجهة رفع الصورة
uploaded_file = st.file_uploader("Upload an image (JPG, PNG)", type=["jpg", "jpeg", "png"])

# معالجة الصورة
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Original Image", use_column_width=True)

    # زر التحويل
    if st.button("Generate Ghibli Image"):
        with st.spinner("Generating image, please wait..."):
            try:
                output_url = replicate_client.run(
                    "fofr/anything-v4.0:7e0c09fc79ee8b19d4f804a8d3da8cf7e811b148a772dfb671a2c7c00c2c3c3b",
                    input={
                        "image": uploaded_file,
                        "prompt": "ghibli style, dreamy, soft colors, anime landscape, cinematic",
                        "num_inference_steps": 30,
                        "guidance_scale": 7.5,
                        "width": 512,
                        "height": 512
                    }
                )

                response = requests.get(output_url)
                result_image = Image.open(BytesIO(response.content))
                st.success("Ghibli image created successfully!")
                st.image(result_image, caption="Ghibli Style Result", use_column_width=True)
                st.markdown(f"[Download Image]({output_url})")

            except Exception as e:
                st.error(f"An error occurred while generating the image: {e}")
