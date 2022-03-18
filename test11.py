import sys
import numpy as np
import cv2 as cv
import math


dist_coef = np.array([[-1.29056527e+00,  2.91293440e+01,  1.66309525e-02, -3.54592780e-02, -2.45822510e-01]])
camera_matrix = np.array([[3.29266406e+03, 0.00000000e+00, 3.48629874e+02],
[0.00000000e+00, 3.04181422e+03, 1.54920825e+02],
[0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

def get_miny_point(box):
    ymin = box[0]
    for p in box:
        if p[1] < ymin[1]:
            ymin = p
    return ymin

def get_minx_point(box):
    xmin = box[0]
    for p in box:
        if p[0] < xmin[0]:
            xmin = p
    return xmin


color_blue = (255, 0, 0)
color_yellow = (0, 255, 255)

if __name__ == '__main__':
    fn = 'images/photo1.jpg'
    img = cv.imread(fn)
    


    img_undist = cv.undistort(img, cameraMatrix=camera_matrix, distCoeffs=dist_coef)

    hsv = cv.cvtColor(img_undist, cv.COLOR_BGR2GRAY)  # цвет меняю с BGR на HSV
    img_binary = cv.threshold(hsv, 200, 255, cv.THRESH_BINARY)[1]
    cv.imshow("1", img_binary)
    contours0, hierarchy = cv.findContours(img_binary.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # перебираю  все найденные контуры в цикле
    for cnt in contours0:
        rect = cv.minAreaRect(cnt)  # пытаемся вписать прямоугольник
        print(rect)
        box = cv.boxPoints(rect)  # поиск четырех вершин прямоугольника
        box = np.int0(box)  # округление координат
        center = (int(rect[0][0]), int(rect[0][1]))
        area = int(rect[1][0] * rect[1][1])  # вычисление площади
        if area > 10000 and area < 1000000:           
            pymin = get_miny_point(box)# точка с  мин у среди всех вершин квадрата 
            pxmin = get_minx_point(box)# точка с  мин х среди всех вершин квадрата 
            usedEdge = np.int0((pxmin[0] - pymin[0], pxmin[1] - pymin[1]))
            reference = (1, 0)  # горизонтальный вектор, задающий горизонт

            # вычисляем угол между самой длинной стороной прямоугольника и горизонтом
            angle = 180 -  (180.0 / math.pi * math.acos(
                (reference[0] * usedEdge[0] + reference[1] * usedEdge[1]) / (cv.norm(reference) * cv.norm(usedEdge))))

            if area > 500:
                cv.drawContours(img_undist, [box], 0, (255, 0, 0), 2)  # рисуем прямоугольник
                cv.circle(img_undist, center, 5, color_yellow, 2)  # рисуем маленький кружок в центре прямоугольника
                # выводим в кадр величину угла наклона
                cv.putText(img_undist, "%d" % int(angle), (center[0] + 20, center[1] - 20),
                    cv.FONT_HERSHEY_SIMPLEX, 1, color_yellow, 2)

        cv.imshow('contours', img_undist)

    cv.waitKey()
    cv.destroyAllWindows()