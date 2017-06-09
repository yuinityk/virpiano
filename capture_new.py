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
freqlist = [523*(2.0**(i/12.0)) for i in range(13)]

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

if __name__ == '__main__':
    fs = 8000
    chunk = 20
    A = 2 # loudness
    ts = 1. #timespan

    p = pyaudio.PyAudio()
    stream = p.open(format = pyaudio.paInt16,
            channels = 1,
            rate = int(fs),
            output = True)

    cap_birdsview  = cv2.VideoCapture(1)
    cap_horizontal = cv2.VideoCapture(2)
    print('Getting Keys...')
    while cv2.waitKey(30)<0:
        ret, frame_b = cap_birdsview.read()
        frame_b = cv2.flip(frame_b,-1)
        img,key_freq = recogKeyboard.recognize_keys(frame_b)
        cv2.imshow('keys',img)

    cv2.destroyWindow('keys')

    print('Getting Horizontal Line...')
    while cv2.waitKey(30)<0:
        ret, frame_h = cap_horizontal.read()
        hline = get_horizontal_line(frame_h)
        cv2.line(frame_h,(0,hline),(frame_h.shape[1],hline),(0,255,0),3)
        cv2.imshow(str(len(key_freq)),frame_h)
    print('Initialization finished')

    cv2.destroyWindow('horizontal')

    is_ground = np.array([0,0,0,0,0])
    sound = [[0,-1] for i in range(5)]

    t = time.time()
    while(True):
        ret, frame_b = cap_birdsview.read()
        ret, frame_h = cap_horizontal.read()
        frame_b = cv2.flip(frame_b,-1)
        t_now = time.time()

        if t_now-t>ts:
            t = t_now
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
                playkey = [0,0,0,0,0]
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
                print 'playkey: ',
                print(playkey)

                # create dumping wave with length fda;oewigrewao
                data = np.zeros(int(fs*ts))
                if len(np.where(is_ground == 1)[0]) != 0:
                    amp = float(A) / len(np.where(is_ground == 1)[0])
                    data = np.zeros(int(fs*ts))
                    for j in range(5):
                        f = freqlist[sound[j][0]-1]
                        if sound[j][1] != -1 and sound[j][0] != 0:
                            tmp = 2*np.pi*f*np.arange(int(fs*ts))
                            tmp /= fs
                            data += 2 * amp * np.sin(tmp) / (1+np.exp(2.*np.arange(int(fs*ts))/fs))
                            #s += amp * np.sin(2*np.pi*f*t/fs)# * 2 / (1+np.exp(d*(i+t)/fs))
                    data[np.where(data>1.)[0]]=1.
                    data[np.where(data<-1.)[0]]=-1.
                data *= 32767.
                data = data.astype(int)
                data = struct.pack("h"*data.shape[0], *data)
                stream.write(data)

        c = ground.find_largest_contour_of_red(frame_h)
        if not isinstance(c,type(None)):
            hull = c[0][::20]
            fingers = ground.finger_tip_horizontal(hull)
            cv2.drawContours(frame_h,[c[0]],-1,(0,255,0),3)
            cv2.drawContours(frame_h,fingers,-1,(0,0,255),3)

        c = ground.find_largest_contour_of_red(frame_b)
        if not isinstance(c,type(None)):
            hull = c[0][::20]
            fingers = ground.finger_tip_from_birdview(hull)
            cv2.drawContours(frame_b,[c[0]],-1,(0,255,0),3)
            cv2.drawContours(frame_b,fingers,-1,(0,0,255),3)


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
