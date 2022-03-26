import sys
import numpy as np
import cv2

img0 = 'basler.bmp'
img = cv2.imread(img0)
#cv2.imshow('img_undist1', img)
cv2.waitKey(0)
dist_coef = np.array([[ 2.04038247e+00, -3.23621188e+02,  1.07636960e-02, -1.16155724e-03,
   1.14084132e+04]])
#camera_matrix = np.array([[640, 0, 480], [0, 640, 480], [0, 0, 1]])
camera_matrix = np.array([[5.30176732e+03, 0.00000000e+00, 1.06642613e+03],
 [0.00000000e+00, 5.08421392e+03, 6.59997778e+02],
 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

img_undist = cv2.undistort(img, cameraMatrix=camera_matrix, distCoeffs=dist_coef)
#img_undist = img_undist[300:1100, 300:1400]
cv2.imshow('img_undist', img_undist)  

cv2.waitKey()
cv2.destroyAllWindows()
