import numpy as np
import cv2

def get_horizontal_line(img_color):
    thre = img_color.shape[1] * 0.25
    hsv = cv2.cvtColor(img_color,cv2.COLOR_BGR2HSV_FULL)
    h = hsv[:,:,0]
    print(img_color.shape)
    print(h.shape)
    s = hsv[:,:,1]
    v = hsv[:,:,2]
    mask = np.zeros(h.shape, dtype=np.uint8)
    mask[((h<20)|(h>200))&(s>80)&(v>50)]=255
    hline = h.shape[0]-1-np.argmax((np.count_nonzero(mask,axis=1)>thre)[::-1])
    print(hline)
    return hline

if __name__ == '__main__':

    capture = cv2.VideoCapture(0)
    while cv2.waitKey(30)<0:
        ret,frame=capture.read()
        hline = get_horizontal_line(frame)
        cv2.line(frame,(0,hline),(frame.shape[1],hline),(0,255,0),3)
        cv2.imshow('hori',frame)
    capture.release()
    '''
    img = cv2.imread('holi.jpg')
    hline = get_horizontal_line(img)
    cv2.line(img,(0,hline),(img.shape[1],hline),(0,255,0),3)
    cv2.imwrite('holiline.jpg',img)
    '''
