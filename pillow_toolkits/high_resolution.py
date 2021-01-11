# -*- coding:utf-8 -*-
"""
-------------------------------------------------
Project Name: toolkits
File Name: high_resolution.py
Author: gaoyw
Create Date: 2020/12/30
-------------------------------------------------
"""

from PIL import Image


def ResizeImage(filein, fileout, scale=1):
    """
    改变图片大小
    :param filein: 输入图片
    :param fileout: 输出图片
    :param width: 输出图片宽度
    :param height: 输出图片宽度
    :param type: 输出图片类型（png, gif, jpeg...）
    :return:
    """
    img = Image.open(filein)
    width = int(img.size[0] * scale)
    height = int(img.size[1] * scale)
    type = img.format
    out = img.resize((width, height), Image.ANTIALIAS)
    # 第二个参数：
    # Image.NEAREST ：低质量
    # Image.BILINEAR：双线性
    # Image.BICUBIC ：三次样条插值
    # Image.ANTIALIAS：高质量
    out.save(fileout, type)


if __name__ == "__main__":
    print("开始运行")
    filein = 'C:/Users/FH/Desktop/ocrtupianjieya/icpr_mtwi_task1/test_line_image_transfer/line_100031.jpg'
    fileout = 'line_100031_higher.jpg'
    ResizeImage(filein, fileout, scale=10)
