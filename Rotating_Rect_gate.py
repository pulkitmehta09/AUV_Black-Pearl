# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 15:32:19 2020

@author: pulme
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 11:46:32 2020

@author: pulme
"""



import cv2
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt

cam=cv2.VideoCapture('C:/Users/pulme/Videos/AUV Media/Testing Video/R2G1.mp4')
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('output1.mp4',fourcc, 60, (640,480))
Data_Features = ['x', 'y','area','asp_Rat','angle','time']
Data_Points = pd.DataFrame(data = None, columns = Data_Features , dtype = float)
start = time.time()
while(True):
    ret,org=cam.read()
    if not ret:
        break
    current_time = time.time() - start
    img=cv2.cvtColor(org,cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (5,5), 0)


    img = cv2.adaptiveThreshold(img, 255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 55, 8)
    cv2.imshow("Mean Thresh", img)
    kernel = np.ones((9,9),np.uint8)
    erosion = cv2.erode(img,kernel,iterations = 1)
    dilation = cv2.dilate(erosion,kernel,iterations =1 )
    opening = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel)
    edges = cv2.Canny(opening, 150, 255,apertureSize=3)
    cv2.imshow("Canny", edges)
    
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #print("I count {} contours in this image".format(len(contours)))
    #cons = org.copy()
    #cv2.drawContours(cons, contours, -1, (0, 255, 0), 2)
    #cv2.imshow("Contours", cons)
    
    
#    contours_poly = [None]*len(contours)
#    boundRect = [None]*len(contours)
    cir=[None]*len(contours)
    area=[None]*len(contours)
    def get_contour_center(contours):
        M = cv2.moments(contours)
        cx=-1
        cy=-1
        if (M['m00']!=0):
            cx= int(M['m10']/M['m00'])
            cy= int(M['m01']/M['m00'])
        return cx, cy
    for i, c in enumerate(contours):
            area[i] = cv2.contourArea(c)
    #        perimeter= cv2.arcLength(c, True)
#            contours_poly[i] = cv2.approxPolyDP(c, 3, True)
#            boundRect[i] = cv2.boundingRect(contours_poly[i])
            cir[i] = get_contour_center(c)
    ## 
    index=area.index(max(area))
    rect = cv2.minAreaRect(contours[index])
    asp_Rat=rect[1][0]/rect[1][1]
    angle=rect[2]
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    if (asp_Rat>0.8 and asp_Rat<1.2):
        img = cv2.drawContours(org,[box],-1,(0,0,255),2)
        Data_Points.loc[Data_Points.size/6] = [cir[index][0] , cir[index][1],area[index],asp_Rat,angle, current_time]
        cv2.circle(img, (cir[index][0],cir[index][1]), 2, (0,0,255),5)
        
        cv2.imshow("Image",img)
        
    
    key = cv2.waitKey(1) & 0xFF
                    	# if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

#cv2.imshow("Erode",erosion)
#cv2.imshow("Opening",opening)
#cv2.imshow("Contours", cons)
#cv2.resize(erosion, None, fx=0.3, fy=0.3)
#cv2.resize(opening, None, fx=0.3, fy=0.3)
#cv2.resize(cons, None, fx=0.3, fy=0.3)
#cv2.waitKey(0)
X0=640
Y0=360
time0=0
Data_Points['x'] = Data_Points['x']- X0
Data_Points['y'] = Data_Points['y'] - Y0
Data_Points['time'] = Data_Points['time'] - time0
plt.subplot(2,2,1)
plt.plot(Data_Points['time'], Data_Points['x'],label='x')
plt.plot(Data_Points['time'], Data_Points['y'],label='y')
plt.xlabel('Time')
plt.subplot(2,2,2)
plt.plot(Data_Points['time'], Data_Points['area'],label='area')
plt.xlabel('Time')
plt.subplot(2,2,3)
plt.plot(Data_Points['time'], Data_Points['asp_Rat'],label='Aspect Ratio')
plt.xlabel('Time')
plt.subplot(2,2,4)
plt.plot(Data_Points['time'], Data_Points['angle'],label='Angle')
plt.xlabel('Time')
plt.legend(framealpha=1, frameon=True);
cam.release()
cv2.destroyAllWindows()