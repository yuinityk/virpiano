# -*- coding: utf-8 -*-
"""
https://sites.google.com/site/lifeslash7830/home/hua-xiang-chu-li/opencvniyoruhuaxiangchulidonghuanoruchuli
"""
import time
import numpy as np
import cv2
import grayscale
import getred


def get_playkey(fingers):
    pass



if __name__ == '__main__':
    cap_birdsview  = cv2.VideoCapture(1)
    cap_horizontal = cv2.VideoCapture(2)
    hline_y = get_horizontal_line()
    time.sleep(3)
    print('initiating...')
#-----initiating-----
    ret, frame_b = cap_birdsview.read()
    key_freq = grayscale.recognize_keys(frame_b)
    print('initiation finished')

    while(True):
        ret, frame_b = cap_birdsview.read()
        ret, frame_h = cap_horizontal.read()
        hands_b = vertex.find_largest_contour_of_red(frame_b)
        hands_h = vertex.find_largest_contour_of_red(frame_h)
        if (not isinstance(hands_b, type(None))) and (not isinstance(hands_h, type(None))):

            hull = hands_b[0][::25] 
# 上からだと25でも行けるかもしれないが横からだと10とかじゃないとダメかも
            fingers = vertex.vertex(hull)
            is_ground = vertex.isGround(fingers,hline_y)
            playing_finger_index = np.where(is_ground == 1)
        #ここではfingers,is_groundedがx座標順にソートされていると仮定する
            playkey = get_playkey(fingers[playing_finger_index]) #fingersの内,接地している指の位置ベクトルの配列を引数として渡す
            play(playkey)
        cv2.imshow('frame',img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
