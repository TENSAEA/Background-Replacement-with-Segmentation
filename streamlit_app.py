import streamlit as st
import cv2
import numpy as np
import os
from PIL import Image
import tempfile

# Function to create a mask for the person in the image using simple color thresholding
def create_person_mask(img):
    # Convert PIL image to OpenCV format
    if isinstance(img, Image.Image):
        img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    # Convert to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Define range for skin color in HSV
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    
    # Create mask for skin color
    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    
    # Apply morphological operations to clean up the mask
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # Find contours and create a more refined mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Create a refined mask with only the largest contour (assuming it's the person)
    refined_mask = np.zeros_like(mask)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        cv2.fillPoly(refined_mask, [largest_contour], 255)
    
    return refined_mask

# Function to process image with background removal
def remove_background(img, background_option, background_image=None, blur_strength=15):
    # Convert PIL image to OpenCV format if needed
    if isinstance(img, Image.Image):
        img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    # Create person mask
    mask = create_person_mask(img)
    
    # Create background based on option
    if background_option == "Solid Color":
        # Default solid color (purple)
        bg = np.full_like(img, (255, 0, 255))
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
        bg = np.full_like(img, (255, 0, 255))
    
    # Apply mask to combine foreground and background
    mask_3channel = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    img_out = np.where(mask_3channel == 255, img, bg)
    
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
        blur_strength = st.sidebar.slider("Blur Strength", 5, 51, 15, step=2)
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