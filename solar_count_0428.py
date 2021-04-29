import cv2
import numpy as np

img = cv2.imread('demo.JPG')

gauss = cv2.GaussianBlur(img, (3, 3), 0)  # 高斯模糊
gray = cv2.cvtColor(gauss, cv2.COLOR_BGR2GRAY)


canny = cv2.Canny(gray, 150, 255 )
closing = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, (3,3))



ret, thresh = cv2.threshold(closing, 200,255, cv2.THRESH_BINARY)
dilation = cv2.dilate(thresh,(3,3),iterations = 5)


contours, hierarchy = cv2.findContours(dilation.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
mask = np.zeros_like(dilation)
count=0
for i in range(len(contours)):
    count+=1
    cnt = contours[i]
    area = cv2.contourArea(cnt)

    if (1000 < area < 2000):
        (x, y, w, h) = cv2.boundingRect(cnt)
        #if (w < 500) and (h < 500):  
        #print("{}-area:{}".format(count,area),end="  ") #打印出每個板子的面積
        c_min = []
        c_min.append(cnt)
        cv2.drawContours(mask, c_min, -1, (255, 255, 255), thickness=-1)


erosion = cv2.erode(mask.copy(),(3,3),iterations = 5)
   
rgb = img.copy()
contours, hierarchy = cv2.findContours(erosion, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) # FindContours
count=0
ares_avrg=0
for c in contours:
    ares = cv2.contourArea(c)
    if (700< ares <1400):
        count+=1
        ares_avrg+=ares
        print("第{}塊-面積:{}".format(count,ares),end="  ") #打印出每個板子的面積
        rect = cv2.boundingRect(c) # 檢測輪廓
        print("x:{} y:{}".format(rect[0],rect[1]))#打印座標
        cv2.rectangle(rgb, rect, (0,0,255), 2)
        y=10 if rect[1]<10 else rect[1] #防止編號到圖片之外
        cv2.putText(img,str(c), (rect[0], y), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 0, 255), 1) #在左上角寫上編號
print("太陽能板平均面積:{}".format(round(ares_avrg/ares,2))) #打印出太陽能板的面積
        
cv2.namedWindow('mask', cv2.WINDOW_NORMAL)
cv2.imshow('mask', mask)
cv2.namedWindow('dilation', cv2.WINDOW_NORMAL)
cv2.imshow('dilation', dilation)
cv2.namedWindow('erosion', cv2.WINDOW_NORMAL)
cv2.imshow('erosion', erosion)
cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.imshow('img', rgb)
cv2.waitKey(0)