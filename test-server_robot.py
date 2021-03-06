import sys
sys.path.append('..')
import logging
import numpy as np
import cv2 as cv
import math
import rtde.rtde as rtde
import rtde.rtde_config as rtde_config

# logging.basicConfig(level=logging.INFO)

ROBOT_HOST = 'localhost'
ROBOT_PORT = 30004
config_filename = 'control_loop_configuration.xml'

keep_running = True

logging.getLogger().setLevel(logging.INFO)

conf = rtde_config.ConfigFile(config_filename)
state_names, state_types = conf.get_recipe('state')
setp_names, setp_types = conf.get_recipe('setp')
watchdog_names, watchdog_types = conf.get_recipe('watchdog')

con = rtde.RTDE(ROBOT_HOST, ROBOT_PORT)
con.connect()

# get controller version
con.get_controller_version()

# setup recipes
con.send_output_setup(state_names, state_types)
setp = con.send_input_setup(setp_names, setp_types)
watchdog = con.send_input_setup(watchdog_names, watchdog_types)

# Setpoints to move the robot to
#setp1 = [-0.12, -0.43, 0.14, 0, 3.11, 0.04]
#setp2 = [-0.12, -0.51, 0.21, 0, 3.11, 0.04]

setp.input_double_register_0 = 0
setp.input_double_register_1 = 0
setp.input_double_register_2 = 0
setp.input_double_register_3 = 0
setp.input_double_register_4 = 0
setp.input_double_register_5 = 0

# The function "rtde_set_watchdog" in the "rtde_control_loop.urp" creates a 1 Hz watchdog
watchdog.input_int_register_0 = 0

wm = 490
hm = 350
wp = 819
wh = 599
pixel_mm1 = wm / wp
pixel_mm2 = hm / wh


#коэфеценты для исправления искажения изображения
dist_coef = np.array([[-2.02945255e+00,  1.90093052e+02,  2.66508451e-02,  2.24567271e-02,   
  -6.01011230e+03]])
camera_matrix = np.array([[3.89167040e+03, 0.00000000e+00, 1.01148810e+03],
 [0.00000000e+00, 3.72302190e+03, 4.89507813e+02],
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


def setp_to_list(setp):
    list = []
    for i in range(0, 6):
        list.append(setp.__dict__["input_double_register_%i" % i])
    return list


def list_to_setp(setp, list):
    for i in range(0, 6):
        setp.__dict__["input_double_register_%i" % i] = list[i]
    return setp


# start data synchronization
if not con.send_start():
    sys.exit()

# control loop
while keep_running:
    # receive the current state
    state = con.receive()

    fn = 'images/photo00.jpg'
    img = cv.imread(fn)
    
    img_undist = img

    hsv = cv.cvtColor(img_undist, cv.COLOR_BGR2GRAY)  # цвет меняю с BGR на HSV
    img_binary = cv.threshold(hsv, 200, 255, cv.THRESH_BINARY)[1]
    cv.imshow("1", img_binary)
    contours0, hierarchy = cv.findContours(img_binary.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # перебираю  все найденные контуры в цикле
    if contours0 != 0:
        for cnt in contours0:
            rect = cv.minAreaRect(cnt)  # пытаемся вписать прямоугольник
            print(rect)
            box = cv.boxPoints(rect)  # поиск четырех вершин прямоугольника
            box = np.int0(box)  # округление координат
            center = (int(rect[0][0]), int(rect[0][1]))
            # ищу координаты центра квадрата
            X = center[0]
            Y = center[1]
            print(X, Y)
            # перевожу в мм
            Xm = (X * pixel_mm1) / 1000
            Ym = (Y * pixel_mm2) / 1000
            area = int(rect[1][0] * rect[1][1])  # вычисление площади
            if area > 10000 and area < 1000000:
                print(Xm, Ym)
                pymin = get_miny_point(box)  # точка с  мин у среди всех вершин квадрата
                pxmin = get_minx_point(box)  # точка с  мин х среди всех вершин квадрата
                usedEdge = np.int0((pxmin[0] - pymin[0], pxmin[1] - pymin[1]))
                reference = (1, 0)  # горизонтальный вектор, задающий горизонт

                # вычисляем угол между самой длинной стороной прямоугольника и горизонтом
                angle = 180 - (180.0 / math.pi * math.acos(
                    (reference[0] * usedEdge[0] + reference[1] * usedEdge[1]) / (
                                cv.norm(reference) * cv.norm(usedEdge))))
                angle1 = (math.pi * angle) / 180
                setp1 = [Xm, Ym, 0.14, angle1, 3.14, 0]

                if area > 500:
                    cv.drawContours(img_undist, [box], 0, (255, 0, 0), 2)  # рисуем прямоугольник
                    cv.circle(img_undist, center, 5, color_yellow, 2)  # рисуем маленький кружок в центре прямоугольника
                    # выводим в кадр величину угла наклона
                    cv.putText(img_undist, "%d" % int(angle), (center[0] + 20, center[1] - 20),
                                cv.FONT_HERSHEY_SIMPLEX, 1, color_yellow, 2)
            
    else:
        setp1 = [0, 0, 0, 0, 0, 0]
    
    cv.imshow('contours', img_undist)

    if state is None:
        break;
    
    list_to_setp(setp, setp1)
    
    con.send(setp)

    # kick watchdog
    con.send(watchdog)

con.send_pause()

con.disconnect()
