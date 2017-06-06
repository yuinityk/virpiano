# -*- coding: utf-8 -*-
"""
https://sites.google.com/site/lifeslash7830/home/hua-xiang-chu-li/opencvniyoruhuaxiangchulidonghuanoruchuli
"""
import time
import struct
import numpy as np
import cv2
import recogKeyboard
import pyaudio
import ground

rainbow = [(255,0,0),(255,165,0),(255,255,0),(0,128,0),(0,255,255),(0,0,255),(128,0,128)]
freqlist = [262*(2.0**(i/12.0)) for i in range(13)]

def get_playkey(key_freq,fingers_b):
    fing = [0,0,0,0,0]
    print(len(fingers_b))
    for i in range(len(fingers_b)):
        for j in range(len(key_freq)):
            cnt = key_freq[j][0]
            point = fingers_b[i][0]
            if cv2.pointPolygonTest(cnt,tuple(point),False) == 1:
                fing[i] = j+1
    return fing


def get_horizontal_line(frames_h):
    thre = frames_h.shape[1] * 0.25
    hsv = cv2.cvtColor(frames_h,cv2.COLOR_BGR2HSV_FULL)
    h = hsv[:,:,0]
    s = hsv[:,:,1]
    v = hsv[:,:,2]
    mask = np.zeros(h.shape, dtype=np.uint8)
    mask[((h<20)|(h>200))&(s>80)&(v>50)]=255
    hline = h.shape[0]-1-np.argmax((np.count_nonzero(mask,axis=1)>thre)[::-1])
    return hline

t=time.time()
if __name__ == '__main__':
    t_old=t
    t=time.time()
    dt=t-t_old
    fs = 8000
    chunk = 20
    A = 2 # loudness

    p = pyaudio.PyAudio()
    stream = p.open(format = pyaudio.paInt16,
            channels = 1,
            rate = int(fs),
            output = True)

    cap_birdsview  = cv2.VideoCapture(0)
    cap_horizontal = cv2.VideoCapture(1)
    print('Getting Keys...')
    while cv2.waitKey(30)<0:
        ret, frame_b = cap_birdsview.read()
        img,key_freq = recogKeyboard.recognize_keys(frame_b)
        cv2.imshow('keys',img)

    print('Getting Horizontal Line...')
    while cv2.waitKey(30)<0:
        ret, frame_h = cap_horizontal.read()
        hline = get_horizontal_line(frame_h)
        cv2.line(frame_h,(0,hline),(frame_h.shape[1],hline),(0,255,0),3)
        cv2.imshow('horizontal',frame_h)
    print('Initialization finished')

    is_ground = np.array([0,0,0,0,0])
    sound = [[0,-1] for i in range(5)]

    while(True):
        ret, frame_b = cap_birdsview.read()
        ret, frame_h = cap_horizontal.read()
        hands_b = ground.find_largest_contour_of_red(frame_b)
        hands_h = ground.find_largest_contour_of_red(frame_h)
        if (not isinstance(hands_b, type(None))) and (not isinstance(hands_h, type(None))):
            fingers_h = ground.finger_tip_horizontal(hands_h[0][::25])
            fingers_b = ground.finger_tip_from_birdview(hands_b[0][::20])
#for i in range(len(key_freq)):
#cv2.drawContours(frame_b,[key_freq[i][0]],-1,rainbow[i%7],3)
        if (not isinstance(hands_b, type(None))) and (not isinstance(hands_h, type(None))) and (not isinstance(hands_b[0], type(None))) and (len(fingers_h)!= 0) and (len(fingers_b)!= 0):

# 上からだと25でも行けるかもしれないが横からだと10とかじゃないとダメかも
            cv2.drawContours(frame_b,fingers_b,-1,(0,0,255),3)
            is_ground_old = is_ground
            is_ground = ground.isGround(fingers_h,hline)
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
                     sound[i][1] += sound_old[i][1]+1

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
                        f = freqlist[sound[j][0]]
                        t = sound[j][1] * chunk # you check
                        if sound[j][1] != -1:
                            s += amp * np.sin(2*np.pi*f*(i+t)*dt/fs)# * 2 / (1+np.exp(d*(i+t)/fs))

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

        for i, [k,_] in enumerate(key_freq):
            cv2.drawContours(frame_b, [k], -1, rainbow[i%7],3)
        cv2.line(frame_h,(0,hline),(frame_h.shape[1],hline),(0,255,0),3)
        frame = np.concatenate((frame_b,frame_h),axis=1)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    stream.close()
    p.terminate()
    cap_birdsview.release()
    cap_horizontal.release()
    cv2.destroyAllWindows()
