import os
import glob
import matplotlib.pyplot as plt
import numpy as np
import cv2
import sys
import time
from PIL import *
from pylab import *


b=1
a=0
c=0
while b<153:
    c=0
    a=a+1
    print a
    for i in range (0,5):
        c=c+1
        
        filename=str(a)+ "/" + str(c) + ".png"
        img1 =cv2.imread(filename, 0)
        
        (thresh, im_bw) = cv2.threshold(img1, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        
    
        contours, hierarchy = cv2.findContours(im_bw,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)


        for cnt in contours:

             x,y,w,h = cv2.boundingRect(cnt)
       
             img2 = img1[y-20:y+h+20,x-20:x+w+20]

                   
        name= str(a)+ "/" + "crop"+ str(c)+".png"   
        cv2.imwrite(name,img2)

             
    b=b+1
    



