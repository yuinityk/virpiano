# -*- coding:utf-8 -*-
import numpy as np
import cv2
import vertex
import time
import recogKeyboard
import ground

if __name__ == '__main__':
    capture = cv2.VideoCapture(1)
    ret, frame_b = capture.read()
    time.sleep(3)
    print('initiating...')
    img, keyfreq = recogKeyboard.recognize_keys(frame_b)
    if len(keyfreq)==0:
        print('fa')
    print('initiation finished')
    time.sleep(3)

    try:
        while cv2.waitKey(30)<0:
            ret, frame_b = capture.read()
            hands_b = ground.find_largest_contour_of_red(frame_b)
            ans = ground.finger_tip_from_birdview(hands_b[0][::20])
            samplecnt = np.array([[1,1],[1,10],[10,10],[10,1]])
            for i in range(len(ans)):
                for j in range(len(keyfreq)):
                    cnt = keyfreq[j][0]
                    point = ans[i][0]
                    if cv2.pointPolygonTest(cnt,tuple(point),False) == 1:
                        print(str(i+1)+'th finger is in ' + str(j+1)+'th key')
#print(ans[i])
            cv2.drawContours(frame_b,ans,-1,(0,0,255),3)
            cv2.imshow('key',frame_b)
    except KeyboardInterrupt:
            capture.release()
            print('sys exit')


    '''
            for i in range(len(ans)):
                for j in range(len(keyfreq)):
                    cnt = keyfreq[j][0]
                    point = ans[i]
                    if cv2.pointPolygonTest(cnt,point,False) == 1:
                        print(str(i+1)+'th finger is in ' +str(j)+'th key')
                cv2.drawContours(frame_b,ans[i])
#cv2.imwrite('fad.png',img_color)
            cv2.imshow('key',frame_b)
            '''
