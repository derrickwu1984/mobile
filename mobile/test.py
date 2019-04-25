from selenium import  webdriver
from PIL import Image
from selenium.webdriver.support.select import Select
import  time,pytesseract,logging
import numpy as np

import cv2 as cv


def read_img():
    src = cv.imread("D:/2.png")
    gray = cv.cvtColor(src,cv.COLOR_BGR2GRAY)
    # 二值化处理
    ret, im_inv = cv.threshold(gray, 127, 255, cv.THRESH_BINARY_INV)
    kernel = 1 / 16 * np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]])
    im_blur = cv.filter2D(im_inv, -1, kernel)
    # 降噪后，我们对图片再做一轮二值化处理
    ret, im_res = cv.threshold(im_blur, 127, 255, cv.THRESH_BINARY)
    # 用opencv的findContours来提取轮廓
    # im2, contours, hierarchy = cv.findContours(im_res, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
    # kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, 6))  # 去除线
    # binl = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel)
    # kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 1))
    # open_out = cv.morphologyEx(binl, cv.MORPH_OPEN, kernel)
    # cv.bitwise_not(open_out, open_out)  # 背景变为白色
    cv.imshow("fuck",im_res)
    cv.waitKey(0)
    cv.destroyAllWindows()
read_img()