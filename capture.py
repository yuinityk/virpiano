# -*- coding: utf-8 -*-
"""
https://sites.google.com/site/lifeslash7830/home/hua-xiang-chu-li/opencvniyoruhuaxiangchulidonghuanoruchuli
"""
import time
import struct
import numpy as np
import cv2
import grayscale
import getred
import pyaudio
import ground

def get_playkey(key_freq,hands_b):
    fing = [0,0,0,0,0]
    fingertip = ground.finger_tip_from_birdview(hands_b[0][::20])
    for i in range(5):
        for j in range(len(key_freq)):
            cnt = key_freq[j][0]
            point = fingertip[i][0]
            if cv2.pointPolygonTest(cnt,tuple(point),False) == 1:
                fing[i] = j+1
    return fing


def get_horizontal_line():
    raise NotImplementedError()


if __name__ == '__main__':
    p = pyaudio.PyAudio()
    stream = p.open(format = pyaudio.paInt16,
            channels = 1,
            rate = int(fs),
            output = True)
    fs = 8000
    chunk = 1024

    A = 2 # loudness

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
            is_ground_old = is_ground
            is_ground = vertex.isGround(fingers,hline_y)
            sound_old = sound
            sound = [[0,-1] for i in range(5)]
            if is_ground != is_ground_old:
                playkey = get_playkey(key_freq,hands_b) #fingersの内,接地している指の位置ベクトルの配列を引数として渡す
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
                data.append(s)
            data *= 32767.
            data = data.astype(int)
            data = struct.pack("h"*data.shape[0], *data)

            buffer = data[0:chunk]
#while buffer != '':
            stream.write(buffer)
            sp = sp + chunk
            buffer = data[sp:sp+chunk]

        cv2.imshow('frame',img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    stream.close()
    p.terminate()
    cap.release()
    cv2.destroyAllWindows()
