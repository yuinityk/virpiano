import numpy as np
import cv2

def n_resize(im,n): #resize im to 1/n scale
    height = im.shape[0]
    width = im.shape[1]
    half_size = cv2.resize(im,(width / n, height / n))
    return half_size

def two_means(clusters):
    label = np.random.rand(len(clusters))
    label *= 2
    label = np.floor(label)
    areas = [cv2.contourArea(clusters[j]) for j in range(len(clusters))]
    for i in range(10):
        sum_zero = 0.
        sum_one = 0.
        for j in np.where(label==0)[0]:
            sum_zero += areas[j]
        for j in np.where(label==1)[0]:
            sum_one += areas[j]
        sum_zero /= len(np.where(label==0)[0])
        sum_one /= len(np.where(label==1)[0])
        for j in range(len(clusters)):
            if abs(sum_zero-areas[j])>abs(sum_one-areas[j]):
                label[j]=1
            else:
                label[j]=0
    if areas[0] > np.mean(areas) and label[0] == 0:
        label = np.ones(len(label))-label
    return label


img = cv2.imread('key.jpg',0)
img_color = cv2.imread('key.jpg')
cv2.imwrite('gray.png',img)


'''
しきい値の適性検査→70がいいっぽい
for i in range(6,17):
    ret, thresh = cv2.threshold(img,i*10,255,cv2.THRESH_BINARY)
    cv2.imwrite('test_'+str(i)+'.png',thresh)
'''

ret, thresh = cv2.threshold(img,70,255,cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#thresh = cv2.drawContours(img, contours, -1, (0,255,0),3)
#cv2.imwrite('contour.png',img)

rainbow = [(255,0,0),(255,165,0),(255,255,0),(0,128,0),(0,255,255),(0,0,255),(128,0,128)]
keys = []
maxc = []
for c in contours:
    if cv2.contourArea(c) < 90:
        continue
    if cv2.contourArea(c) > img_color.size/3.5:
        continue
    epsilon = 0.005*cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, epsilon, True)
    keys.append(approx)
    if len(maxc)<1:
        maxc.append(approx)
    elif cv2.contourArea(approx)>cv2.contourArea(maxc[0]):
        maxc[0] = approx

for c in keys:
    if c in maxc:
        keys.remove(c)
        break

label = two_means(keys)
print(label)

for i in range(len(keys)):
    cv2.fillPoly(img_color, pts=[keys[i]], color=(255*label[i],255*label[i],255*label[i]))
keys = sorted(keys, key=lambda x: int(cv2.moments(x)['m10']/cv2.moments(x)['m00']))

count = 0
for c in keys:
    print(cv2.contourArea(c))
    cv2.drawContours(img_color, [c], -1, rainbow[count%7],3)
    count+=1

cv2.imwrite('contour.png',img_color)


