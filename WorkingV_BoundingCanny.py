# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 11:46:32 2020

@author: pulme
"""



import cv2
import numpy as np
import random as rng

cam=cv2.VideoCapture('C:/Users/pulme/Videos/AUV Media/Testing Video/R2G1.mp4')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output1.mp4',fourcc, 60, (640,480))
while(True):
    ret,org=cam.read()
    if not ret:
        break
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
    
    
    contours_poly = [None]*len(contours)
    boundRect = [None]*len(contours)
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
            contours_poly[i] = cv2.approxPolyDP(c, 3, True)
            boundRect[i] = cv2.boundingRect(contours_poly[i])
            cir[i] = get_contour_center(c)
    ## 
    index=area.index(max(area))
    asp_Rat=float(boundRect[index][2])/boundRect[index][3]
    if (asp_Rat>0.8 and asp_Rat<1.2):
        drawing = np.zeros((edges.shape[0], edges.shape[1], 3), dtype=np.uint8)   
        ##        #centers[i], radius[i] = cv.minEnclosingCircle(contours_poly[i])
        ##        
        ##        
        #for i in range(len(contours)):
        color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
        cv2.drawContours(drawing, contours_poly, index, color)
        cv2.rectangle(drawing, (int(boundRect[index][0]), int(boundRect[index][1])), (int(boundRect[index][0]+boundRect[index][2]), int(boundRect[index][1]+boundRect[index][3])), (0,0,255), 20)
        rcx=int(boundRect[index][0]+boundRect[index][2]/2)
        rcy=int(boundRect[index][1]+boundRect[index][3]/2)
        cv2.circle(drawing, (rcx,rcy), 10, (0,0,255),10)
        ##        
        drawing=drawing+org
        res = cv2.resize(drawing,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)
        cv2.imshow('Contours1', res)
        #    print ("Area: {}, Perimeter: {}".format(area, perimeter))
        res1 = cv2.resize(org,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)    
        cv2.imshow("Original",res1)
        out.write(res)
        
        
    
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
cam.release()
cv2.destroyAllWindows()