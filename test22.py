import cv2
import threading
import numpy as np
from pypylon import pylon

count1 = 0

dist_coef = np.array([[ 2.04038247e+00, -3.23621188e+02,  1.07636960e-02, -1.16155724e-03, 1.14084132e+04]])
camera_matrix = np.array([[5.30176732e+03, 0.00000000e+00, 1.06642613e+03],
            [0.00000000e+00, 5.08421392e+03, 6.59997778e+02],
            [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

    #cb_func = my_callback.datastream_callback
try:
    # conecting to the first available camera
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

    # Grabing Continusely (video) with minimal delay
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
    converter = pylon.ImageFormatConverter()

    # converting to opencv bgr format
    converter.OutputPixelFormat = pylon.PixelType_BGR8packed
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

    print("To terminate, focus on the OpenCV window and press any key.")

    while camera.IsGrabbing():

        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        if grabResult.GrabSucceeded():
            image = converter.Convert(grabResult)
            img_arr = image.GetArray()

            img_undist = cv2.undistort(img_arr, cameraMatrix=camera_matrix, distCoeffs=dist_coef)
            img_undist = img_arr[300:1100, 300:1400]

            cv2.imshow('img', img_undist)
            

            k = cv2.waitKey(1)
            if k == 27:
                cv2.imwrite(f"photo0{count1}.jpg", img_undist)
                count1+=1
        grabResult.Release()
        
    # Releasing the resource    
    camera.StopGrabbing()

except Exception as exception:
    print(exception)
