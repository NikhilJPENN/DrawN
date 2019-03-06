import os
import glob
import matplotlib.pyplot as plt
import numpy as np
import cv2
import sys
import time
from PIL import *
from pylab import *


hog = cv2.HOGDescriptor()

img1 = cv2.imread('edgeshot1.png', 0)   # replace image for trials

ht, wid = img1.shape[:2]
scale = 2
ht = ht/scale
wid = wid/scale


G1=np.zeros((153,5,45360))
s=zeros(6)
indexm=zeros(153)
simm=zeros(153)
b=1
a=0
c=0
while b<153:
    c=0
    a=a+1
    for i in range (0,5):
        c=c+1
        
        filename=str(a)+ "/" + str(c) + ".png"
        img1 = cv2.imread(filename, 0)
        img1 = cv2.resize(img1, (wid, ht), interpolation=cv2.INTER_CUBIC)
        print a
        print b
        
        h = hog.compute(img1, winStride=(64,128), padding=(0, 0))
        h=np.asarray(h)
        h11= h/np.linalg.norm(h)
        h1=h11[:,0]
        G1[a,i,:]=h1
            
    b=b+1
    
    np.save("3Darray.npy", G1)  
