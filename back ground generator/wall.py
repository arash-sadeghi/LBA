import numpy as np
import cv2 as cv
import qrcode
# 2 meter is 512 pixels


# for i in range(0,im_size_x):
#     for j in range(0,im_size_y):
#         # im[i,j]=im[i,j]*255
#         if i>(im_size_x/2)-50 and i<(im_size_x/2)+50: im[i,j]=1

# cv.imshow("im",im)
# cv.waitKey()

# cv.imwrite('wall11.png',im)
qr=qrcode.QRCode(box_size=2)
qr.make('QR1')
img = qr.make_image()
img.save('QR1.png')
img=cv.imread('QR1.png')
imm = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

imms=np.size(imm,0)
print(imms)

im_size_x=512
im_size_y=imms
im=np.zeros((im_size_x,im_size_y))+0.25

# print("before",im)
for i in range(0,im_size_x):
    for j in range(0,im_size_y):
        if i>=(im_size_x/2)-imms/2 and i<=(im_size_x/2)+imms/2:
            # print("\n\n>>",i,j,(im_size_x/2)-imms/2-i,int((im_size_y/2)-imms/2)-j)
            im[i,j]=imm[int((im_size_x/2)-imms/2-i),j]
# print("before",im)


# im=np.transpose(im)
cv.imshow("im",im)
cv.waitKey()

for i in range(0,im_size_x):
    for j in range(0,im_size_y):
        im[i,j]=im[i,j]*255

cv.imwrite('wallqrx.png',im)