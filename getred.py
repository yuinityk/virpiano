import numpy as np
import cv2

def getred(img):
    img_blue, img_green, img_red = cv2.split(img)
    if len(img.shape) == 3:
        height, width, channels = img.shape[:3]
    else:
        height, width = img.shape[:2]

    zeros = np.zeros((height,width),img.dtype)
    return cv2.merge((zeros,zeros,img_red))

def fdas(img):
    img_loc = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    cv2.medianBlur
