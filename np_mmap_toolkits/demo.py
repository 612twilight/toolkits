# -*- coding:utf-8 -*-
"""
-------------------------------------------------
Project Name: toolkits
File Name: demo.py
Author: gaoyw
Create Date: 2021/5/13
构建的思路
将numpy.nddary对象以二进制的方式写入文件中 ，同时将读取的偏移量和长度写入另一个文件
读取思路：
记录偏移量和长度的文件可以是约定好的二进制格式，也应该可以是raw文件
-------------------------------------------------
"""


class IndexRecord(object):
    def __init__(self, path):
        self.path = path
        pass

    def write(self, sizes):
        pass


class RawIndexRecord(IndexRecord):
    def __init__(self, path):
        super().__init__(path)
        pass
