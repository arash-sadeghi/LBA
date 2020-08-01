# import sys
# sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import numpy as np
import cv2 as cv
from math import exp,sqrt
import matplotlib.pyplot as plt
# 2 meter is 512 pixels
m2pix=512/2
# im_size_x=512
# im_size_x=int(sqrt(10)*512/2)
# im_size_x=int(2*sqrt(2)*512/2)
ROBN=100
# im_size_x=int(2*sqrt(2)*m2pix*sqrt(ROBN/20))
# im_size_x=int(5*m2pix*sqrt(ROBN/20))
im_size_x=int(2*m2pix)
im_size_y=im_size_x*2

# R=int(1.5*m2pix*sqrt(ROBN/20))
# R=int(0.7*m2pix*sqrt(ROBN/20))
R=int(0.4*m2pix)

def gauss(x):
    # a = 512 # amplititude of peak
    a = 1.0 # amplititude of peak

    b = im_size_x/2.0 # center of peak
    c = im_size_x/15# standard deviation
    # print (">>",a*exp(-((x-b)**2)/(2*(c**2))))
    return a*exp(-((x-b)**2)/(2*(c**2)))
#robot radius=0.04 m
# sensing radius =0.1
# b=2
# n=40
# rr=0.06
# rs=0.16
# ar=np.pi*(rs)**2
# ac=b*n*ar
# R=int((sqrt(ac)/np.pi)*512.0/2.0)
# print("R= ",R,"ac= ",ac," ",sqrt(ac/np.pi))
im=np.zeros((im_size_x,im_size_y))

# cv.circle(im,(int(im_size_y/2+100),int(im_size_x/2)),R,1,2)
data=[]
for i in range(0,R):
    # cv.circle(im,(int((1+1.5)*512/2),int(im_size_y/2)),i,gauss(im_size_x/2-i),2)
    cv.circle(im,(int((im_size_y/4)),int(im_size_x/2)),i,gauss(im_size_x/2-i),2)
    # data.append(gauss(im_size_x/2-i))
# for i in range(120,380):
#     data.append(im[im_size_x//2,i]*255)
# plt.plot(data)
# plt.ylim(0,255)
# plt.show()
# for i in range(0,R):
#     cv.circle(im,(int(3*im_size_y/4-50),int(im_size_x/2)),i,gauss(im_size_x/2-i),2)

# hl=75 #75 is small side of rectangle
# hl=int(0.75*512/2) #75 is small side of rectangle
hl=int(0.94*512/2) #75 is small side of rectangle

# cv.rectangle(im,(0,int(im_size_x/2)-hl),(hl,int(im_size_x/2)+hl),0.25,1)
# cv.rectangle(im,(im_size_y,int(im_size_x/2)-hl),(im_size_y-hl,int(im_size_x/2)+hl),0.25,1)
# cv.rectangle(im,(int(im_size_y/2)-hl,0),(int(im_size_y/2)+hl,hl),0.25,1)
# cv.rectangle(im,(int(im_size_y/2)-hl,im_size_x),(int(im_size_y/2)+hl,im_size_x-hl),0.25,1)

# cv.rectangle(im,(int(im_size_y/3)+hl-int(512*0.3/2)-100,im_size_x),(int(im_size_y/3)-hl-int(512*0.3/2)-100,im_size_x-hl),0.25,1)
# cv.rectangle(im,(int(2*im_size_y/3)+hl+int(512*0.3/2)+100,im_size_x),(int(2*im_size_y/3)-hl+int(512*0.3/2)+100,im_size_x-hl),0.25,1)

# cv.rectangle(im,(int(im_size_y/3)+hl-int(512*0.3/2)-100,0),(int(im_size_y/3)-hl-int(512*0.3/2)-100,hl),0.25,1)
# cv.rectangle(im,(int(2*im_size_y/3)+hl+int(512*0.3/2)+100,0),(int(2*im_size_y/3)-hl+int(512*0.3/2)+100,hl),0.255,1)

# ----------------------------------------------------
# off=int(100*2.5)
# cv.rectangle(im,(0,int(im_size_x/2)-hl),(hl,int(im_size_x/2)+hl),0.25,1)
# cv.rectangle(im,(im_size_y,int(im_size_x/2)-hl),(im_size_y-hl,int(im_size_x/2)+hl),0.25,1)


# cv.rectangle(im,(int(im_size_y/2)-hl,0),(int(im_size_y/2)+hl,hl),0.25,1)
# cv.rectangle(im,(int(im_size_y/2)-hl,im_size_x),(int(im_size_y/2)+hl,im_size_x-hl),0.25,1)

# cv.rectangle(im,(int(im_size_y/3)+hl-int(512*0.3/2)-off,im_size_x),(int(im_size_y/3)-hl-int(512*0.3/2)-off,im_size_x-hl),0.25,1)
# cv.rectangle(im,(int(2*im_size_y/3)+hl+int(512*0.3/2)+off,im_size_x),(int(2*im_size_y/3)-hl+int(512*0.3/2)+off,im_size_x-hl),0.25,1)

# cv.rectangle(im,(int(im_size_y/3)+hl-int(512*0.3/2)-off,0),(int(im_size_y/3)-hl-int(512*0.3/2)-off,hl),0.25,1)
# cv.rectangle(im,(int(2*im_size_y/3)+hl+int(512*0.3/2)+off,0),(int(2*im_size_y/3)-hl+int(512*0.3/2)+off,hl),0.255,1)
#-------------------------------------------------------
# iv=im_size_y/4
# center= int(iv-100*sqrt(2)*sqrt(2)*2.5)
# center2=int(2*iv)
# center3=int(3*iv+100*sqrt(2)*sqrt(2)*2.5)
# c=[center, center2 ,center3]
# for center1 in c:
#     cv.circle(im,(center1,0),10,1,-1) # for an unknown reason palces of x and y are cahnged. x represents columns
#     cv.circle(im,(center1+hl,0),10,1,-1) # for an unknown reason palces of x and y are cahnged. x represents columns
#     cv.circle(im,(center1-hl,0),10,1,-1) # for an unknown reason palces of x and y are cahnged. x represents columns
#     cv.circle(im,(center1+hl,hl),10,1,-1) # for an unknown reason palces of x and y are cahnged. x represents columns
#     cv.circle(im,(center1-hl,hl),10,1,-1) # for an unknown reason palces of x and y are cahnged. x represents columns

# print(np.shape(im))

# cv.imshow("im",im)
# cv.waitKey()
for i in range(0,im_size_x):
    for j in range(0,im_size_y):
        im[i,j]=im[i,j]*255



# path="C:\\Users\\asus\\Desktop\\paper1\\webots\\2\worlds\\b1.jpg"
# cv.imwrite('present.png',np.transpose(im))
# cv.imwrite('Secondary_background.png',np.transpose(im))
# cv.imwrite(str(ROBN)+'__1_setup2.png',im)
cv.imwrite("Supervisor//Initial_background.png",im)
# cv.imwrite("Supervisor//Initial_background xx.png",im)
