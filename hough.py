# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 09:18:47 2020

@author: pulme
"""



import cv2
import numpy as np
import random as rng

org=cv2.imread('C:/Users/pulme/Downloads/Buoy.jpg')
img=cv2.cvtColor(org,cv2.COLOR_BGR2GRAY)
#img=org[:,:,0]
cv2.imshow("Img",img)
img = cv2.GaussianBlur(img, (5,5), 0)
#img = cv2.bilateralFilter(img,9,75,75)

img = cv2.adaptiveThreshold(img, 255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 111, 12)
cv2.imshow("Mean Thresh", img)
kernel = np.ones((9,9),np.uint8)
erosion = cv2.erode(img,kernel,iterations = 2)
dilation = cv2.dilate(erosion,kernel,iterations =2 )
#opening = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel)
edges = cv2.Canny(dilation, 190, 255)
cv2.imshow("Canny", edges)

minLineLength = 5
maxLineGap = 5
lines = cv2.HoughLinesP(edges,60,np.pi/180,300,minLineLength,maxLineGap)
for line in lines:
    x1,y1,x2,y2=line[0]
    cv2.line(org,(x1,y1),(x2,y2),(0,0,255),2)


#lines = cv2.HoughLines(edges,10,np.pi/45,50)
#for line in lines:
#    rho,theta=line[0]
#    a = np.cos(theta)
#    b = np.sin(theta)
#    x0 = a*rho
#    y0 = b*rho
#    x1 = int(x0 + 1000*(-b))
#    y1 = int(y0 + 1000*(a))
#    x2 = int(x0 - 1000*(-b))
#    y2 = int(y0 - 1000*(a))
#
#    cv2.line(org,(x1,y1),(x2,y2),(0,255,0),2)

cv2.imshow("Hough",org)



#contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
##print("I count {} contours in this image".format(len(contours)))
##cons = org.copy()
##cv2.drawContours(cons, contours, -1, (0, 255, 0), 2)
##cv2.imshow("Contours", cons)


#contours_poly = [None]*len(contours)
#boundRect = [None]*len(contours)
#cir=[None]*len(contours)
#area=[None]*len(contours)
#def get_contour_center(contours):
#    M = cv2.moments(contours)
#    cx=-1
#    cy=-1
#    if (M['m00']!=0):
#        cx= int(M['m10']/M['m00'])
#        cy= int(M['m01']/M['m00'])
#    return cx, cy
#for i, c in enumerate(contours):
#        area[i] = cv2.contourArea(c)
##        perimeter= cv2.arcLength(c, True)
#        contours_poly[i] = cv2.approxPolyDP(c, 3, True)
#        boundRect[i] = cv2.boundingRect(contours_poly[i])
#        cir[i] = get_contour_center(c)
### 
#index=area.index(max(area))
#drawing = np.zeros((edges.shape[0], edges.shape[1], 3), dtype=np.uint8)   
###        #centers[i], radius[i] = cv.minEnclosingCircle(contours_poly[i])
###        
###        
##for i in range(len(contours)):
#color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
#cv2.drawContours(drawing, contours_poly, index, color)
#cv2.rectangle(drawing, (int(boundRect[index][0]), int(boundRect[index][1])), (int(boundRect[index][0]+boundRect[index][2]), int(boundRect[index][1]+boundRect[index][3])), (0,255,0), 2)
#rcx=int(boundRect[index][0]+boundRect[index][2]/2)
#rcy=int(boundRect[index][1]+boundRect[index][3]/2)
#cv2.circle(drawing, (rcx,rcy), 2, (0, 255, 0), -1)
###        
#res = cv2.resize(drawing,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)
#cv2.imshow('Contours1', res)
#    print ("Area: {}, Perimeter: {}".format(area, perimeter))
#res1 = cv2.resize(org,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)    
#cv2.imshow("Original",res1)
#cv2.imshow("Erode",erosion)
#cv2.imshow("Opening",opening)
#cv2.imshow("Contours", cons)
#cv2.resize(erosion, None, fx=0.3, fy=0.3)
#cv2.resize(opening, None, fx=0.3, fy=0.3)
#cv2.resize(cons, None, fx=0.3, fy=0.3)
cv2.waitKey(0)
cv2.destroyAllWindows()