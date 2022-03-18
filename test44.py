import sys
import numpy as np
import cv2

img0 = 'images/photo1.jpg'
img = cv2.imread(img0)
cv2.imshow('img_undist1', img)
cv2.waitKey(0)
dist_coef = np.array([[-1.29056527e+00,  2.91293440e+01,  1.66309525e-02, -3.54592780e-02,
  -2.45822510e-01]])
#camera_matrix = np.array([[640, 0, 480], [0, 640, 480], [0, 0, 1]])
camera_matrix = np.array([[3.29266406e+03, 0.00000000e+00, 3.48629874e+02],
[0.00000000e+00, 3.04181422e+03, 1.54920825e+02],
[0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

img_undist = cv2.undistort(img, cameraMatrix=camera_matrix, distCoeffs=dist_coef)

cv2.imshow('img_undist', img_undist)  

cv2.waitKey()
cv2.destroyAllWindows()
