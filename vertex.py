import cv2
import numpy as np

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


def vertex(contour):
    ans = []
    for i in range(len(contour)-2):
        v0=(contour[i+1][0]-contour[i][0])/np.linalg.norm(contour[i+1][0]-contour[i][0])
        v1=(contour[i+2][0]-contour[i+1][0])/np.linalg.norm(contour[i+2][0]-contour[i+1][0])
        dot = np.dot(v0,v1)
        cross = np.cross(v0,v1)
        if len(ans)<5:
            if cross<0:
                ans.append([contour[i+1][0],dot])
        elif cross<0:
            for j in range(5):
                if ans[j][1] > dot:
                    for k in range(4-j):
                        ans[4-k] = ans[3-k]
                    ans[j] = [contour[i+1][0],dot]
                    break
    print [np.array([x[0]]) for x in ans]
    return [np.array([x[0]]) for x in ans]


if __name__ == "__main__":

    capture = cv2.VideoCapture(1)
    while cv2.waitKey(30)<0:
        ret, frame = capture.read()
        c = find_largest_contour_of_red(frame)
        if not isinstance(c,type(None)):
            #cv2.drawContours(frame,[c[0]],-1,(0,0,255),3)
            #cv2.drawContours(frame,[c[1]],-1,(0,0,255),3)
            hull = c[0][::25]
            ans = vertex(hull)
            cv2.drawContours(frame,ans,-1,(0,0,255),3)
        else:
            print('none')
        cv2.imshow('red',frame)
    capture.release()
   
