import streamlit as st
import requests
from io import BytesIO
from PIL import Image

# Backend API URL
BACKEND_API_URL = "https://c807-2001-8f8-1d36-c1c0-a432-1928-8866-27a3.ngrok-free.app/generate-image/"

# Streamlit app
st.title("AI Image Generator")

# User input form
with st.form("image_form"):
    prompt = st.text_input("Enter a text prompt for the image:", help="Describe the image you want to generate.")
    model = st.selectbox(
        "Select a model:",
        ["flux", "flux-realism", "flux-cablyai", "flux-anime", "flux-3d", "any-dark", "flux-pro", "turbo", "cartoon"]
    )
    seed = st.number_input("Random seed (optional):", min_value=0, value=None, step=1, format="%d")
    width = st.slider("Image width (pixels):", 64, 2048, 512)
    height = st.slider("Image height (pixels):", 64, 2048, 512)
    enhance = st.checkbox("Enhance the image", value=True)
    safe = st.checkbox("Ensure the image is safe", value=True)
    
    # Submit button
    submitted = st.form_submit_button("Generate Image")

if submitted:
    if not prompt:
        st.error("Please provide a text prompt.")
    else:
        st.info("Generating image... This may take a moment.")

        # Prepare request payload
        payload = {
            "prompt": prompt,
            "model": model,
            "seed": seed if seed != 0 else None,
            "width": width,
            "height": height,
            "enhance": enhance,
            "safe": safe,
        }

        try:
            # Send POST request to backend API
            response = requests.post(BACKEND_API_URL, json=payload, stream=True)

            # Check if the request was successful
            if response.status_code == 200:
                st.success("Image generated successfully!")
                image = Image.open(BytesIO(response.content))
                st.image(image, caption="Generated Image", use_column_width=True)
            else:
                st.error(f"Failed to generate image: {response.json().get('error', 'Unknown error')}")

        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
