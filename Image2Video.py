# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 16:56:02 2020

@author: pulme
"""

import cv2
import numpy as np
import glob
 
img_array = []
for filename in glob.glob('C:/Users/pulme/Desktop/Working/Video2res/*.jpg'):
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
 
 
out = cv2.VideoWriter('project.avi',cv2.VideoWriter_fourcc(*'DIVX'), 7, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()