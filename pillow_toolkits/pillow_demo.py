# -*- coding:utf-8 -*-
"""
-------------------------------------------------
Project Name: toolkits
File Name: pillow_demo.py
Author: gaoyw
Create Date: 2020/12/29
-------------------------------------------------
"""
from PIL import Image


def image_border(src, dst, loc='a', width=3, color=(0, 0, 0)):
    '''
    src: (str) 需要加边框的图片路径
    dst: (str) 加边框的图片保存路径
    loc: (str) 边框添加的位置, 默认是'a'(
        四周: 'a' or 'all'
        右: 'r' or 'rigth'
        下: 'b' or 'bottom'
        左: 'l' or 'left'
    )
    width: (int) 边框宽度 (默认是3)
    color: (int or 3-tuple) 边框颜色 (默认是0, 表示黑色; 也可以设置为三元组表示RGB颜色)
    '''
    # 读取图片
    img_ori = Image.open(src)
    w = img_ori.size[0]
    h = img_ori.size[1]

    # 添加边框
    if loc in ['a', 'all']:
        w += 2 * width
        h += 2 * width
        img_new = Image.new('RGB', (w, h), color)
        img_new.paste(img_ori, (width, width))
    elif loc in ['t', 'top']:
        h += width
        img_new = Image.new('RGB', (w, h), color)
        img_new.paste(img_ori, (0, width, w, h))
    elif loc in ['r', 'right']:
        w += width
        img_new = Image.new('RGB', (w, h), color)
        img_new.paste(img_ori, (0, 0, w - width, h))
    elif loc in ['b', 'bottom']:
        h += width
        img_new = Image.new('RGB', (w, h), color)
        img_new.paste(img_ori, (0, 0, w, h - width))
    elif loc in ['l', 'left']:
        w += width
        img_new = Image.new('RGB', (w, h), color)
        img_new.paste(img_ori, (width, 0, w, h))
    else:
        pass

    # 保存图片
    img_new.save(dst)


def transfer_one():
    image_border("C:/Users/FH/Desktop/ocrtupianjieya/icpr_mtwi_task1/test_line_image/line_70896.jpg", '../new.jpg', 'a',
                 10, color=(255, 255, 255))


def transfer_batch():
    import os
    src_dir = "C:/Users/FH/Desktop/ocrtupianjieya/icpr_mtwi_task1/test_line_image"
    file_names = os.listdir(src_dir)
    dst_dir = "C:/Users/FH/Desktop/ocrtupianjieya/icpr_mtwi_task1/test_line_image_transfer"
    os.makedirs(dst_dir, exist_ok=True)
    for index, file_name in enumerate(file_names):
        src_path = os.path.join(src_dir, file_name)
        dst_path = os.path.join(dst_dir, file_name)
        image_border(src_path, dst_path, 'a', 10, color=(255, 255, 255))
        if (index + 1) % 500 == 0:
            print("已经处理了{}份图片".format(index + 1))


if __name__ == "__main__":
    transfer_batch()
