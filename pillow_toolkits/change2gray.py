# -*- coding:utf-8 -*-
"""
-------------------------------------------------
Project Name: toolkits
File Name: change2gray.py
Author: gaoyw
Create Date: 2020/12/30
-------------------------------------------------
"""
import cv2


def graychange():
    image = cv2.imread('line_100031_higher.jpg', cv2.IMREAD_GRAYSCALE)
    cv2.imwrite('line_100031_higher_gray.jpg', image)


def graychange2():
    image = cv2.imread("C:/Users/FH/Desktop/compress/mtwi_2018_train/image_train/T1.3BPFFJdXXXXXXXX_!!0-item_pic.jpg.jpg", cv2.IMREAD_GRAYSCALE)
    cv2.imwrite('test2.jpg', image)


if __name__ == '__main__':
    graychange2()
