# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 09:22:45 2020

@author: pulme
"""

import cv2
import os
import time

cap = cv2.VideoCapture(0)
capture_duration = 10
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.mp4',fourcc, 24, (640,480))
path='D:/AUV/Opencv'

start_time = time.time()
while( int(time.time() - start_time) < capture_duration ):
    ret, frame = cap.read()
    if ret==True:
        out.write(frame)
        cv2.imshow(os.path.join(path,'frame'),frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
 
#while(cap.isOpened()):
#    ret, frame = cap.read()
#    if ret==True:
#        out.write(frame)
#        cv2.imshow(os.path.join(path,'frame'),frame)
#        if cv2.waitKey(1) & 0xFF == ord('q'):
#            break
#    else:
#        break


cap.release()
out.release()
cv2.destroyAllWindows()