import cv2
import numpy as np
import pygame

#img = cv2.imread('filename.png',0)

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
        img2=255-img1
    
        name= str(a)+ "/" + "shadow"+ str(c)+".png"   
        cv2.imwrite(name,img2)

             
    b=b+1
    










