# -*- coding:utf-8 -*-
"""
-------------------------------------------------
Project Name: toolkits
File Name: demo.py
Author: gaoyw
Create Date: 2021/6/10
Description: 
-------------------------------------------------
"""
import os


def recu_list_dirs_by_dictionary_order(path, indent=0, maxi=-1, only_dir=True):
    """
    按字典序递归输出目录结构
    :param path: str 文件路径
    :param indent: int 首次缩进空格(默认为 0，一般不用改变)
    :param maxi: int 最大展开层数(默认为 -1，表示全部展开)
    """
    if maxi != 0:
        try:
            lsdir = os.listdir(path)
        except PermissionError:  # 对于权限不够的文件不作处理
            pass
        else:
            for item in lsdir:
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    print(' ' * indent, '+', item)
                    recu_list_dirs_by_dictionary_order(full_path, indent + 4, maxi - 1)
                if not only_dir and os.path.isfile(full_path):
                    print(' ' * indent, '-', item)


if __name__ == '__main__':
    recu_list_dirs_by_dictionary_order("E:\gyw\dl_lab_toolkits/raw_data\ccks2021面向保险领域的低资源文档信息抽取")
