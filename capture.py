# -*- coding: utf-8 -*-
"""
https://sites.google.com/site/lifeslash7830/home/hua-xiang-chu-li/opencvniyoruhuaxiangchulidonghuanoruchuli
"""
import struct
import numpy as np
import cv2
import recogKeyboard
import getred
import pyaudio
import ground
#import vertex

rainbow = [(255,0,0),(255,165,0),(255,255,0),(0,128,0),(0,255,255),(0,0,255),(128,0,128)]

def get_playkey(key_freq,fingers_b):
    fing = [0,0,0,0,0]
    for i in range(5):
        for j in range(len(key_freq)):
            cnt = key_freq[j][0]
            point = fingers_b[i][0]
            if cv2.pointPolygonTest(cnt,tuple(point),False) == 1:
                fing[i] = j+1
    return fing


def get_horizontal_line():
    return 260
    raise NotImplementedError()


if __name__ == '__main__':
    fs = 8000
    chunk = 512
    A = 2 # loudness

    p = pyaudio.PyAudio()
    stream = p.open(format = pyaudio.paInt16,
            channels = 1,
            rate = int(fs),
            output = True)

    cap_birdsview  = cv2.VideoCapture(0)
    cap_horizontal = cv2.VideoCapture(2)
    hline_y = get_horizontal_line()
    print('initiating...')
#-----initiating-----
    ret, frame_b = cap_birdsview.read()
    key_freq = recogKeyboard.recognize_keys(frame_b)
    print('initiation finished')

    is_ground = np.array([0,0,0,0,0])
    sound = [[0,-1] for i in range(5)]

    while(True):
        ret, frame_b = cap_birdsview.read()
        ret, frame_h = cap_horizontal.read()
        hands_b = ground.find_largest_contour_of_red(frame_b)
        hands_h = ground.find_largest_contour_of_red(frame_h)
#for i in range(len(key_freq)):
#cv2.drawContours(frame_b,[key_freq[i][0]],-1,rainbow[i%7],3)
        if (not isinstance(hands_b, type(None))) and (not isinstance(hands_h, type(None))):

# 上からだと25でも行けるかもしれないが横からだと10とかじゃないとダメかも
            fingers_h = ground.finger_tip_horizontal(hands_h[0][::25])
            fingers_b = ground.finger_tip_from_birdview(hands_b[0][::20])
            cv2.drawContours(frame_b,fingers_b,-1,(0,0,255),3)
            is_ground_old = is_ground
            is_ground = ground.isGround(fingers_h,hline_y)
            sound_old = sound
            sound = [[0,-1] for i in range(5)]
            if np.any(is_ground - is_ground_old != 0):
                playkey = get_playkey(key_freq,fingers_b) #fingersの内,接地している指の位置ベクトルの配列を引数として渡す
                for i in range(5):
                    sound[i][0] = playkey[i]
                    if is_ground[i]:
                        sound[i][1] = sound_old[i][1]+1
                    else:
                        sound[i][1] = -1
            else:
                 for i in range(5):
                     sound[i][1] += 1

            # create dumping wave with length fda;oewigrewao
            data = np.array([])
            if len(np.where(is_ground == 1)[0]) == 0:
                for i in range(chunk):
                    data = np.append(data,0.)
            else:
                amp = float(A) / len(np.where(is_ground == 1)[0])
                for i in range(chunk):
                    s = 0.
                    d = 2.
                    for j in range(5):
                        f = sound[j][0]
                        t = sound[j][1] * chunk # you check
                        if sound[j][1] != -1:
                            s += amp * np.sin(2*np.pi*f*(i+t)/fs) * 2 / (1+np.exp(d*(i+t)/fs))

                    if s>1.:
                        s = 1.
                    elif s<-1.:
                        s = -1.
                    data = np.append(data,s)
            data *= 32767.
            data = data.astype(int)
            data = struct.pack("h"*data.shape[0], *data)

            buffer = data[0:chunk]
            stream.write(buffer)

        cv2.imshow('frame',frame_b)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    stream.close()
    p.terminate()
    cap_birdsview.release()
    cap_horizontal.release()
    cv2.destroyAllWindows()
