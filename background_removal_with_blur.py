import cv2
import numpy as np

def create_blur_background(frame, blur_level=25):
    """Create a blurred version of the frame to use as background"""
    return cv2.GaussianBlur(frame, (blur_level, blur_level), 0)

def create_solid_color_background(frame, color=(255, 255, 255)):
    """Create a solid color background"""
    return np.full_like(frame, color)

def segment_person(frame, lower_bound=(0, 0, 100), upper_bound=(150, 100, 255)):
    """
    Simple person segmentation using color thresholding in HSV color space.
    This is a basic approach and may not work perfectly for all cases.
    """
    # Convert to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Create mask for skin color
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    
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

def remove_background_with_blur(frame, background_type="blur", blur_level=25):
    """
    Remove background from frame and replace with blur or solid color
    
    Args:
        frame: Input frame
        background_type: "blur" for blurred background, "solid" for solid color
        blur_level: Blur level for background (odd number)
    
    Returns:
        Frame with background removed and replaced
    """
    # Ensure blur_level is odd
    if blur_level % 2 == 0:
        blur_level += 1
    
    # Segment person in the frame
    mask = segment_person(frame)
    
    # Create background
    if background_type == "blur":
        background = create_blur_background(frame, blur_level)
    else:
        background = create_solid_color_background(frame)
    
    # Apply mask to combine foreground and background
    mask_3channel = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    result = np.where(mask_3channel == 255, frame, background)
    
    return result, mask

def main():
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    # Set camera properties
    cap.set(3, 640)  # Width
    cap.set(4, 480)  # Height
    
    background_type = "blur"  # "blur" or "solid"
    blur_level = 25  # Blur level for background
    
    print("Controls:")
    print("Press 'b' to toggle between blur and solid background")
    print("Press '+' to increase blur level")
    print("Press '-' to decrease blur level")
    print("Press 'q' to quit")
    
    while True:
        success, frame = cap.read()
        if not success:
            print("Error: Could not read frame")
            break
        
        # Remove background
        result, mask = remove_background_with_blur(frame, background_type, blur_level)
        
        # Stack original and result frames
        stacked = np.hstack((frame, result))
        
        # Display frame
        cv2.imshow("Background Removal - Original (Left) | Result (Right)", stacked)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('b'):
            background_type = "solid" if background_type == "blur" else "blur"
            print(f"Background type: {background_type}")
        elif key == ord('+') and background_type == "blur":
            blur_level = min(blur_level + 2, 99)  # Keep it odd and within reasonable range
            print(f"Blur level: {blur_level}")
        elif key == ord('-') and background_type == "blur":
            blur_level = max(blur_level - 2, 5)  # Keep it odd and within reasonable range
            print(f"Blur level: {blur_level}")
    
    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()