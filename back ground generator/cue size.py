import numpy as np
import cv2 as cv
from math import exp,sqrt
m2pix=512/2
ROBN=100
im_size_x=int(5*m2pix)
im_size_y=im_size_x*2
RR=5
R=int(RR*m2pix)
def gauss(x):
    a = 1.0 # amplititude of peak

    b = im_size_x/2.0 # center of peak
    c = im_size_x*RR/14# standard deviation
    return a*exp(-((x-b)**2)/(2*(c**2)))
im=np.zeros((im_size_x,im_size_y))
for i in range(0,R):
    cv.circle(im,(int((im_size_y/4)),int(im_size_x/2)),i,gauss(im_size_x/2-i),2)
hl=int(0.94*512/2) #75 is small side of rectangle
cv.imshow("im",im)
cv.waitKey()
for i in range(0,im_size_x):
    for j in range(0,im_size_y):
        im[i,j]=im[i,j]*255
cv.imwrite("20__1 "+str(RR)+".png",im)
