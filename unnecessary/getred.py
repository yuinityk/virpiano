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
    cv2.medianBlur(img_loc)

def find_largest_contour_of_red(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)
    h = hsv[:,:,0]
    s = hsv[:,:,1]
    mask = np.zeros(h.shape, dtype=np.uint8)
    mask[((h<30)|(h>190))&(s>10)]=255
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours)==0:
        return None
    c = [contours[0],contours[0]]
    for contour in contours:
        if cv2.contourArea(contour) < 200:
            continue
        if cv2.contourArea(contour) > cv2.contourArea(c[0]):
            c[1] = c[0]
            c[0] = contour
        elif cv2.contourArea(contour) > cv2.contourArea(c[1]):
            c[1] = contour
    return c

def fingertip(contour):
    points = c[0][::50]
    print(points)

if __name__ == "__main__":
    capture = cv2.VideoCapture(1)
    k = 0
    while cv2.waitKey(30)<0:
        ret, frame = capture.read()
        c = find_largest_contour_of_red(frame)
        if not isinstance(c,type(None)):
            cv2.drawContours(frame,c[0][::50],-1,(0,0,255),3)
#cv2.drawContours(frame,[c[1]],-1,(0,0,255),3)
        else:
            print('none')
        cv2.imshow('red',frame)
        if k == 50:
            print(type(c[0][::50][0]))
        k += 1
    capture.release()
    cv2.destroyAllWindows()
