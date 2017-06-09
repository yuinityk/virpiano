# -*- coding:utf-8 -*-
import numpy as np
import cv2


def two_means(clusters):
    if len(clusters) < 2:
        return np.zeros(len(clusters))
    label = np.random.rand(len(clusters))
    label *= 2
    label = np.floor(label)
    label[0] = 0
    label[1] = 1
    areas = [cv2.contourArea(clusters[j]) for j in range(len(clusters))]
    for i in range(10):
        sum_zero = 0.
        sum_one = 0.
        for j in np.where(label==0)[0]:
            sum_zero += areas[j]
        for j in np.where(label==1)[0]:
            sum_one += areas[j]
        if len(np.where(label==0)[0])>0:
            sum_zero /= len(np.where(label==0)[0])
        if len(np.where(label==1)[0])>0:
            sum_one /= len(np.where(label==1)[0])
        for j in range(len(clusters)):
            if abs(sum_zero-areas[j])>abs(sum_one-areas[j]):
                label[j]=1
            else:
                label[j]=0
        if len(areas) > 0 and areas[0] > np.mean(areas) and len(label)>0 and label[0] == 0:
            label = np.ones(len(label))-label
    return label

def recognize_keys(img):
    img_color = img
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, thresh = cv2.threshold(img,70,255,cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    rainbow = [(255,0,0),(255,165,0),(255,255,0),(0,128,0),(0,255,255),(0,0,255),(128,0,128)]
    keys = []
    maxc = []
    for c in contours:
        if cv2.contourArea(c) < 800: # 小さい雑多なものは弾く
            continue
        if cv2.contourArea(c) > img_color.size/3.1:
            continue
        epsilon = 0.01*cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)
        keys.append(approx)
        if len(maxc)<1:
            maxc.append(approx)
        elif cv2.contourArea(approx)>cv2.contourArea(maxc[0]):
            maxc[0] = approx
    for c in keys:
        epsilon = 0.005*cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)

        if cv2.contourArea(approx) in [cv2.contourArea(maxc[0])]:
            try:
                keys.remove(c)
                break
            except ValueError:
                print(c)
                print(keys)
    if len(keys) < 2:
        return img_color,[]
    label = two_means(keys)

    for i in range(len(keys)):
        cv2.fillPoly(img_color, pts=[keys[i]], color=(255*label[i],255*label[i],255*label[i]))
    keys = sorted(keys, key=lambda x: int(cv2.moments(x)['m10']/max(cv2.moments(x)['m00'],0.01)))

    count = 0
    for c in keys:
        cv2.drawContours(img_color, [c], -1, rainbow[count%7],3)
        count+=1

    #cv2.imwrite('fad.png',img_color)
    if len(keys) < 18:
        return img_color, [[keys[i], i] for i in range(len(keys))]
    else:
        return img_color, [[keys[i], i-12] for i in range(len(keys))]

if __name__ == '__main__':
    capture = cv2.VideoCapture(1)
    while cv2.waitKey(30)<0:
        ret, frame = capture.read()
        frame = cv2.flip(frame,-1)
        keyret = recognize_keys(frame)
        img_color = keyret[0]
        print(len(keyret[1]))
        cv2.imshow('red',img_color)
    capture.release()
