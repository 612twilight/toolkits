# -*- coding:utf-8 -*-
"""
-------------------------------------------------
Project Name: toolkits
File Name: pymouse_demo.py
Author: gaoyw
Create Date: 2021/1/16
-------------------------------------------------
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
from pymouse import PyMouse
from selenium import webdriver
from pykeyboard import PyKeyboard
import time


def xx():
    br = webdriver.Chrome(r"D:/迅雷下载/chromedriver_win32/chromedriver.exe")
    br.implicitly_wait(30)
    # 设置浏览器最大化
    br.maximize_window()
    br.get('http://www.baidu.com')
    m = PyMouse()
    kb = PyKeyboard()
    time.sleep(3)

    m.click(650, 358, 1)
    # kb.press_key(kb.control_key)
    # kb.press_key(kb.shift_key)
    # kb.release_key(kb.control_key)
    # kb.release_key(kb.shift_key)
    kb.type_string("test")
    kb.press_key(kb.enter_key)
    kb.release_key(kb.enter_key)
    time.sleep(5)
    m.click(763, 143, 1)
    time.sleep(10)

    # 获取当前坐标的位置
    tt = m.position()
    print(tt)

    # kb.type_string('Hello, World!')
    # kb.tap_key(kb.enter_key)
    # kb.tap_key(kb.enter_key)
    # m.click(500, 300, 1)
    # import time
    # time.sleep(10)
    # br.quit()

def zz():
    # import the module
    from pymouse import PyMouse

    # instantiate an mouse object
    m = PyMouse()

    # move the mouse to int x and int y (these are absolute positions)
    m.move(200, 200)
    # import time
    # time.sleep(10)
    # click works about the same, except for int button possible values are 1: left, 2: right, 3: middle
    m.click(500, 300, 1)
    import time
    time.sleep(10)
    # get the screen size
    m.screen_size()
    # (1024, 768)

    # get the mouse position
    info = m.position()
    print(info)
    # (500, 300)

if __name__ == '__main__':
    xx()
