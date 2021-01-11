# -*- coding:utf-8 -*-
"""
-------------------------------------------------
Project Name: toolkits
File Name: paddle_demo.py
Author: gaoyw
Create Date: 2020/12/29
-------------------------------------------------
"""
# 快速使用

import os
import shutil
import time

from paddleocr import PaddleOCR


def demo_use():
    # Paddleocr目前支持中英文、英文、法语、德语、韩语、日语，可以通过修改lang参数进行切换，参数依次为`ch`, `en`, `french`, `german`, `korean`, `japan`。

    ocr = PaddleOCR(use_angle_cls=True, lang="en", use_gpu=False)

    # 输入待识别图片路径

    img_path = "C:/Users/FH/Desktop/ocrtupianjieya/icpr_mtwi_task1/test_line_image_transfer/line_101415.jpg"
    # img_path = "C:/Users/FH/Desktop/line_101415_angel.jpg"
    # img_path = "../pillow_toolkits/line_100031_higher_gray.jpg"

    # 输出结果保存路径
    result = ocr.ocr(img_path, det=False, cls=True)
    print(result)


def demo_use2():
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")
    file_dir = "C:/Users/FH/Desktop/ocrtupianjieya/icpr_mtwi_task1/test_line_image_transfer"
    file_names = os.listdir(file_dir)
    reader = open("C:/Users/FH/Desktop/ocrtupianjieya/icpr_mtwi_task1/result_transfer.txt", 'r', encoding='utf8')
    already_files = [i.strip().split(" ")[0] for i in reader.readlines()]
    reader.close()
    writer = open("C:/Users/FH/Desktop/ocrtupianjieya/icpr_mtwi_task1/result_transfer.txt", 'a+', encoding='utf8')
    import time
    begin_time = time.time()
    count = 0
    for index, file_name in enumerate(file_names):
        if file_name in already_files:
            continue
        count += 1
        out = ""
        try:
            file_path = os.path.join(file_dir, file_name)
            result = ocr.ocr(file_path, det=False, cls=False)
            if result:
                out = result[0][0]
            writer.write(file_name + " " + out + "\n")
            if count <= 10:
                print(result)
            if (index + 1) % 500 == 0:
                print("当前已处理{}条数据，目前处理平均速度为{}条/s".format(index + 1, count / (time.time() - begin_time)))
                writer.flush()
            # if index == 5000:
            #     break
        except Exception as e:
            print("============error===========")
            print(e)
            print(file_name)
            writer.write(file_name + " " + out + "\n")
    writer.close()


def check_un_rec():
    reader = open("C:/Users/FH/Desktop/ocrtupianjieya/icpr_mtwi_task1/sample_result.txt", 'r', encoding='utf8')
    already_files = [1 for i in reader.readlines() if len(i.strip().split(" ")) == 1]
    reader.close()
    print(len(already_files))


def copy_not_rec_file():
    dst_root_file_dir = "C:/Users/FH/Desktop/ocrtupianjieya/icpr_mtwi_task1/result20201230"
    not_rec_file = "E:/gyw/toolkits/ocr_toolkits/not_recog.txt"
    reader = open(not_rec_file, 'r', encoding='utf8')
    already_files = [i.strip() for i in reader.readlines()]
    reader.close()
    raw_not_rec_dir = os.path.join(dst_root_file_dir, "raw_not_rec")
    transfer_not_rec_dir = os.path.join(dst_root_file_dir, "transfer_not_rec")
    os.makedirs(raw_not_rec_dir, exist_ok=True)
    os.makedirs(transfer_not_rec_dir, exist_ok=True)
    transfer_file_dir = "C:/Users/FH/Desktop/ocrtupianjieya/icpr_mtwi_task1/test_line_image_transfer"
    raw_file_dir = "C:/Users/FH/Desktop/ocrtupianjieya/icpr_mtwi_task1/test_line_image"
    for file_name in already_files:
        shutil.copy(os.path.join(raw_file_dir, file_name), os.path.join(raw_not_rec_dir, file_name))
        shutil.copy(os.path.join(transfer_file_dir, file_name), os.path.join(transfer_not_rec_dir, file_name))


def for_not_rec_test():
    ocr = PaddleOCR(use_angle_cls=True, lang="ch", use_gpu=False)
    en_ocr = PaddleOCR(use_angle_cls=True, lang="en", use_gpu=False)

    dst_root_file_dir = "C:/Users/FH/Desktop/ocrtupianjieya/icpr_mtwi_task1/result20201230"
    transfer_not_rec_dir = os.path.join(dst_root_file_dir, "transfer_not_rec")

    file_names = os.listdir(transfer_not_rec_dir)
    test_result_path = os.path.join(dst_root_file_dir, "rec_test.txt")
    already_files = []
    if os.path.exists(test_result_path):
        reader = open(test_result_path, 'r', encoding='utf8')
        already_files = [i.strip().split(" ")[0] for i in reader.readlines()]
        reader.close()
    writer = open(test_result_path, 'a+', encoding='utf8')
    begin_time = time.time()
    count = 0
    for index, file_name in enumerate(file_names):
        if file_name in already_files:
            continue
        count += 1
        out = ""
        try:
            file_path = os.path.join(transfer_not_rec_dir, file_name)
            result = ocr.ocr(file_path, det=False, cls=True)
            en_result = en_ocr.ocr(file_path, det=False, cls=True)
            if result:
                out = "".join(i[0] for i in result)
            if en_result:
                en_out = "".join(i[0] for i in en_result)
                if len(en_out) > len(out):
                    out = en_out
            writer.write(file_name + " " + out + "\n")
            if count <= 10:
                print(out)
            if (index + 1) % 500 == 0:
                print("当前已处理{}条数据，目前处理平均速度为{:.2f}条/s".format(index + 1, count / (time.time() - begin_time)))
                writer.flush()
            # if index == 5000:
            #     break
        except Exception as e:
            print("============error===========")
            print(e)
            print(file_name)
            writer.write(file_name + " " + out + "\n")
    writer.close()


if __name__ == '__main__':
    demo_use()
