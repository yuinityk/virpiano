# -*- coding:utf-8 -*-
import numpy as np
import cv2
import sys
import time
import vertex
import recogKeyboard
import ground

rainbow = [(255,0,0),(255,165,0),(255,255,0),(0,128,0),(0,255,255),(0,0,255),(128,0,128)]

if __name__ == '__main__':
    capture = cv2.VideoCapture(0)
    ret, frame_b = capture.read()
    time.sleep(3)
    print('initiating...')
    img, keyfreq = recogKeyboard.recognize_keys(frame_b)
    if len(keyfreq)==0:
        print('initiation failed')
        sys.exit()
    print('initiation finished')
    time.sleep(3)

    try:
        while cv2.waitKey(30)<0:
            ret, frame_b = capture.read()
            hands_b = ground.find_largest_contour_of_red(frame_b)
            ans = ground.finger_tip_from_birdview(hands_b[0][::20])
            fing = [0,0,0,0,0]
            for i in range(len(ans)):
                for j in range(len(keyfreq)):
                    cnt = keyfreq[j][0]
                    point = ans[i][0]
                    if cv2.pointPolygonTest(cnt,tuple(point),False) == 1:
                        fing[i] = j+1
            print(fing)
            cv2.drawContours(frame_b,ans,-1,(0,0,255),3)
            for i in range(len(keyfreq)):
                cv2.drawContours(frame_b,[keyfreq[i][0]],-1,rainbow[i%7],3)
            cv2.imshow('key',frame_b)
    except KeyboardInterrupt:
            capture.release()
            print('sys exit')

