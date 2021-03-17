# -*- coding:utf-8 -*-
"""
-------------------------------------------------
Project Name: toolkits
File Name: view_demo.py
Author: gaoyw
Create Date: 2021/3/11
-------------------------------------------------
"""

import numpy as np


def falt_demo():
    a = np.array([[1, 2], [3, 4], [5, 6]])
    a = a.flatten()
    print(a.tolist())


if __name__ == '__main__':
    falt_demo()
