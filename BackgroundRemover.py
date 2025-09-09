import cv2
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import os
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
# cap.set(cv2.CAP_PROP_FPS, 60)

segmentor = SelfiSegmentation()

# imgBG = cv2.imread("BackgroundImages/3.jpg")

listImg = os.listdir("BackgroundImages")
imgList = []
for imgPath in listImg:
    img = cv2.imread(f'BackgroundImages/{imgPath}')
    if img is not None:  # Check if image was loaded successfully
        imgList.append(img)

# Add blur effect option
blurImage = np.zeros((480, 640, 3), np.uint8)
blurImage = cv2.GaussianBlur(np.zeros((480, 640, 3), np.uint8), (55, 5), 0)
imgList.append(blurImage)

indexImg = 0

print("Controls:")
print("Press 'a' to go to previous background")
print("Press 'd' to go to next background")
print("Press 'q' to quit")

while True:
    success, img = cap.read()
    if not success:
        break
    
    # Check if we have any background images
    if len(imgList) > 0 and indexImg < len(imgList):
        # imgOut = segmentor.removeBG(img, (255,0,255), cutThreshold=0.83)
        imgOut = segmentor.removeBG(img, imgList[indexImg], cutThreshold=0.8)
    else:
        # If no background images, just show the original
        imgOut = img

    # Create side by side comparison
    try:
        imgStack = cvzone.stackImages([img, imgOut], 2, 1)
        cv2.imshow("image", imgStack)
    except Exception as e:
        # Fallback if stackImages fails
        cv2.imshow("Original", img)
        cv2.imshow("Background Removed", imgOut)
    
    key = cv2.waitKey(1)
    if key == ord('a'):
        if indexImg > 0:
            indexImg -= 1
    elif key == ord('d'):
        if indexImg < len(imgList) - 1:
            indexImg += 1
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

