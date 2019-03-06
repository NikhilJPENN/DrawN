import cv2
import numpy as np
import pygame

#img = cv2.imread('filename.png',0)

b=0
a=0

while b<6:

    a=a+1

    filename=str(a)+ ".png"
    #pygame.image.save(srf, filename)

    QR_orig = cv2.imread(filename, cv2.CV_LOAD_IMAGE_GRAYSCALE)

    #(thresh, im_bw) = cv2.threshold(QR_orig, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    edges = cv2.Canny(QR_orig,10,70)

    edgename="edgeshota"+ str(a)+ ".png"   

    cv2.imwrite(edgename,edges)
    b=b+1
    
'''    
a=a+1

filename="screenshot"+ str(a)+ ".png"
#pygame.image.save(srf, filename)
#print filename

QR_orig = cv2.imread(filename, cv2.CV_LOAD_IMAGE_GRAYSCALE)
cv2.imshow('image1',QR_orig)

(thresh, im_bw) = cv2.threshold(QR_orig, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
edges = cv2.Canny(im_bw,10,100)

edgename="edgeshot"+ str(a)+ ".png"   

cv2.imwrite('edgeimage.png',edges)
b=b+1
'''


#print edges.max()
#print img.max()


#cv2.imshow('image',edges)
#cv2.imwrite('test3.png',edges)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
