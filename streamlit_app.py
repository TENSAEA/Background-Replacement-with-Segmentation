import streamlit as st
import cv2
import numpy as np
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import os
from PIL import Image
import tempfile

# Initialize the segmentor
segmentor = SelfiSegmentation()

# Function to process image with background removal
def remove_background(img, background_option, background_image=None, blur_strength=15):
    # Convert PIL image to OpenCV format if needed
    if isinstance(img, Image.Image):
        img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    # Create background based on option
    if background_option == "Solid Color":
        # Default solid color (purple)
        bg = (255, 0, 255)
    elif background_option == "Blur":
        # Create blurred background
        bg = cv2.GaussianBlur(img, (blur_strength, blur_strength), 0)
    elif background_option == "Image" and background_image is not None:
        # Resize background image to match input image
        bg = cv2.resize(np.array(background_image), (img.shape[1], img.shape[0]))
        # Convert PIL to OpenCV if needed
        if isinstance(bg, Image.Image):
            bg = np.array(bg)
            bg = cv2.cvtColor(bg, cv2.COLOR_RGB2BGR)
    else:
        # Default to solid color if no valid option
        bg = (255, 0, 255)
    
    # Remove background
    img_out = segmentor.removeBG(img, bg, cutThreshold=0.8)
    
    # Convert back to RGB for displaying in Streamlit
    img_out = cv2.cvtColor(img_out, cv2.COLOR_BGR2RGB)
    
    return img_out

# Streamlit app
def main():
    st.title("Real-Time Background Remover")
    st.write("Remove backgrounds from your images with various background options")
    
    # Sidebar for options
    st.sidebar.header("Background Options")
    background_option = st.sidebar.selectbox(
        "Choose background type:",
        ("Solid Color", "Blur", "Image")
    )
    
    # Additional options based on selection
    if background_option == "Blur":
        blur_strength = st.sidebar.slider("Blur Strength", 5, 15, step=2)
    elif background_option == "Image":
        background_image_file = st.sidebar.file_uploader("Upload background image", type=["jpg", "jpeg", "png"])
        background_image = None
        if background_image_file is not None:
            background_image = Image.open(background_image_file)
    
    # Main content
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Read the image
        image = Image.open(uploaded_file)
        st.image(image, caption="Original Image", use_container_width=True)
        
        # Process the image
        with st.spinner("Processing image..."):
            if background_option == "Image" and 'background_image' in locals() and background_image is not None:
                result = remove_background(image, background_option, background_image)
            elif background_option == "Blur":
                result = remove_background(image, background_option, blur_strength=blur_strength)
            else:
                result = remove_background(image, background_option)
        
        # Display result
        st.image(result, caption="Background Removed", use_container_width=True)
        
        # Download button
        result_pil = Image.fromarray(result)
        buf = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        result_pil.save(buf.name, format="PNG")
        with open(buf.name, "rb") as f:
            st.download_button(
                label="Download Result",
                data=f,
                file_name="background_removed.png",
                mime="image/png"
            )
        
        # Clean up temporary file
        os.unlink(buf.name)
    else:
        st.info("Please upload an image to get started")

if __name__ == "__main__":
    main()