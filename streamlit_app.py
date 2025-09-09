import streamlit as st
import numpy as np
import os
from PIL import Image
import tempfile

# Function to create a mask for the person in the image using simple color thresholding
def create_person_mask(img):
    # Convert PIL image to numpy array
    if isinstance(img, Image.Image):
        img = np.array(img)
    
    # Convert to HSV color space
    # We'll use a simple approach with RGB values instead of converting to HSV
    # This avoids the need for OpenCV
    
    # Define range for skin color in RGB (approximate)
    # These values might need adjustment based on the images
    lower_skin = np.array([50, 40, 30], dtype=np.uint8)
    upper_skin = np.array([255, 200, 180], dtype=np.uint8)
    
    # Create mask for skin color
    mask = np.all((img >= lower_skin) & (img <= upper_skin), axis=2)
    
    # Convert boolean mask to uint8 (0 or 255)
    mask = mask.astype(np.uint8) * 255
    
    # Apply morphological operations to clean up the mask
    # Simple erosion and dilation using scipy
    from scipy import ndimage
    
    # Erosion
    mask = ndimage.binary_erosion(mask, iterations=2)
    # Dilation
    mask = ndimage.binary_dilation(mask, iterations=2)
    
    # Convert back to uint8
    mask = mask.astype(np.uint8) * 255
    
    return mask

# Function to apply Gaussian blur to an image
def gaussian_blur(img, blur_strength=15):
    from scipy import ndimage
    # Ensure blur_strength is odd
    if blur_strength % 2 == 0:
        blur_strength += 1
    
    # Apply Gaussian filter
    if isinstance(img, Image.Image):
        img = np.array(img)
    
    blurred = ndimage.gaussian_filter(img, sigma=blur_strength/3)
    return blurred

# Function to process image with background removal
def remove_background(img, background_option, background_image=None, blur_strength=15):
    # Convert PIL image to numpy array if needed
    if isinstance(img, Image.Image):
        img_array = np.array(img)
    else:
        img_array = img
    
    # Create person mask
    mask = create_person_mask(img)
    
    # Ensure mask has the same dimensions as the image
    if mask.shape[:2] != img_array.shape[:2]:
        # Resize mask to match image
        from PIL import Image as PILImage
        mask_pil = PILImage.fromarray(mask)
        mask_pil = mask_pil.resize((img_array.shape[1], img_array.shape[0]), PILImage.NEAREST)
        mask = np.array(mask_pil)
    
    # Create background based on option
    if background_option == "Solid Color":
        # Default solid color (purple)
        bg = np.full_like(img_array, (255, 0, 255), dtype=np.uint8)
    elif background_option == "Blur":
        # Create blurred background
        bg = gaussian_blur(img_array, blur_strength)
    elif background_option == "Image" and background_image is not None:
        # Resize background image to match input image
        bg = np.array(background_image.resize((img_array.shape[1], img_array.shape[0])))
    else:
        # Default to solid color if no valid option
        bg = np.full_like(img_array, (255, 0, 255), dtype=np.uint8)
    
    # Apply mask to combine foreground and background
    # Expand mask to 3 channels if needed
    if mask.ndim == 2:
        mask_3channel = np.stack([mask, mask, mask], axis=2)
    else:
        mask_3channel = mask
    
    # Normalize mask to 0-1 range
    mask_normalized = mask_3channel / 255.0
    
    # Blend the images
    img_out = img_array * mask_normalized + bg * (1 - mask_normalized)
    
    # Convert to uint8
    img_out = img_out.astype(np.uint8)
    
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