# import sys
# sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import numpy as np
import cv2 as cv
from math import exp,sqrt
# 2 meter is 512 pixels

im_size_x=512
im_size_y=int(im_size_x*2)

def gauss(x):
    # a = 512 # amplititude of peak
    a = 1.0 # amplititude of peak

    b = 512.0/2.0 # center of peak
    c = im_size_x/10.0# standard deviation
    # print (">>",a*exp(-((x-b)**2)/(2*(c**2))))
    return a*exp(-((x-b)**2)/(2*(c**2)))
#robot radius=0.04 m
# sensing radius =0.1
b=2
n=20
rr=0.06
rs=0.16
ar=np.pi*(rs)**2
ac=b*n*ar
R=int((sqrt(ac)/np.pi)*512.0/2.0)
print("R= ",R,"ac= ",ac," ",sqrt(ac/np.pi))
im=np.zeros((im_size_x,im_size_y))

# cv.circle(im,(int(im_size_y/2+100),int(im_size_x/2)),R,1,2)

# for i in range(0,R):
#     cv.circle(im,(int(im_size_y/4+50),int(im_size_x/2)),i,gauss(im_size_x/2-i),2)

for i in range(0,R):
    cv.circle(im,(int(3*im_size_y/4-50),int(im_size_x/2)),i,gauss(im_size_x/2-i),2)

hl=75 #75 is small side of rectangle
cv.rectangle(im,(0,int(im_size_x/2)-hl),(hl,int(im_size_x/2)+hl),0.25,1)
cv.rectangle(im,(im_size_y,int(im_size_x/2)-hl),(im_size_y-hl,int(im_size_x/2)+hl),0.25,1)
cv.rectangle(im,(int(im_size_y/2)-hl,0),(int(im_size_y/2)+hl,hl),0.25,1)
cv.rectangle(im,(int(im_size_y/2)-hl,im_size_x),(int(im_size_y/2)+hl,im_size_x-hl),0.25,1)


cv.imshow("im",im)
cv.waitKey()
for i in range(0,im_size_x):
    for j in range(0,im_size_y):
        im[i,j]=im[i,j]*255



# path="C:\\Users\\asus\\Desktop\\paper1\\webots\\2\worlds\\b1.jpg"
# cv.imwrite('Initial_background.png',im)
cv.imwrite('Secondary_background_T.png',np.transpose(im))
# cv.imwrite('All_together.png',im)
