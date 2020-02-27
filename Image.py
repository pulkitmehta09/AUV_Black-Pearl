 # -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import cv2
import time
import os


print(cv2.__version__)
cap = cv2.VideoCapture('C:/Users/pulme/Downloads/2.mp4')
ret ,image = cap.read()
count = 0
path='C:/Users/pulme/Downloads/Pool Videos'
while True:
  cv2.imwrite(os.path.join(path,"frame%d.jpg" % count), image)     # save frame as JPEG file
  ret,image = cap.read()
  #cv2.imshow('frame',image)
  print ('Read a new frame: ', ret)
  count += 1
  if cv2.waitKey(1) & 0xFF == ord('q'):
      break
  #time.sleep(5)
cap.release()
cv2.destroyAllWindows()