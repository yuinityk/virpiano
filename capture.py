# -*- coding: utf-8 -*-
"""
https://sites.google.com/site/lifeslash7830/home/hua-xiang-chu-li/opencvniyoruhuaxiangchulidonghuanoruchuli
"""
import numpy as np
import cv2
import grayscale

cap = cv2.VideoCapture(1)

while(True):
    ret, frame = cap.read()
    img = grayscale.recognize_keys(frame)
    cv2.imshow('frame',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
