import os
import sys
import math
import cv2 as cv
import numpy as np

img_name = "Coordinate_system/carla_town03_allmap_points.png"
# name = "Town03.jpg" 
file_name = 'Coordinate_system/img_label_2.txt'
data = []
def readImage(img_name):
    """读取图片"""
    # filelist = os.listdir(dir)
    # imgname = os.path.join(dir, name)
    img1 = cv.imread(img_name)  # 这里必须用cv库里面的imread，否则格式不对会报错
    return img1

# 定义一个窗口
def draw_(event, x, y,flag, param):
    global  data, img1 
    if event == cv.EVENT_LBUTTONDOWN:
        """左键单击打标签"""
        xy = "%d,%d" % (x, y)
        cv.circle(img1, (x, y),2, (255, 0, 0), thickness=-1)
        data.append([x,y])
def save_points(file_name):
    with open(file_name, 'w') as f:
        for i in range(len(data)):
            f.write(f"{data[i][0]}, {data[i][1]}\n")
        f.close()
    ab_filename = os.path.abspath(file_name)
    print(ab_filename)

try:
    cv.namedWindow('image',cv.WINDOW_NORMAL)
    cv.setMouseCallback('image', draw_)

    img1 = readImage(img_name)

    while 1:
        cv.imshow('image', img1)
        # mode = True

        c = cv.waitKey(10) & 0xFF
        if c == ord('c'): #按c退出
            break

        f = cv.waitKey(10) & 0xFF    # 按f保存
        if f == ord('f'):
            save_points(file_name)

finally:
    cv.destroyAllWindows()