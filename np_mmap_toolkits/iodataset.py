# -*- coding:utf-8 -*-
"""
-------------------------------------------------
Project Name: toolkits
File Name: iodataset.py
Author: gaoyw
Create Date: 2021/5/13

创造一种从io获取数据集中某个元素的方式
构建方法，存储偏移量和size  存储二进制文件
-------------------------------------------------
"""
import os.path as path
from tempfile import mkdtemp

import numpy as np
import torch


def build_and_read():
    # write
    dtype = np.float32
    dtype_size = dtype().itemsize
    print("dtype_size={}".format(dtype_size))
    filename = path.join(mkdtemp(), 'dataset.file')
    dataset = [torch.arange(5), torch.arange(4),
               torch.arange(7), torch.arange(10)]
    print("dataset={}".format(dataset))
    data_offsets = [0]
    dim_offsets = [0]
    sizes = []
    with open(filename, 'wb') as writer:
        for data in dataset:
            bytes = writer.write(np.array(data, dtype=dtype))
            data_offsets.append(data_offsets[-1] + bytes / dtype_size)
            for i in data.size():
                sizes.append(i)
            dim_offsets.append(dim_offsets[-1] + len(data.size()))

    # read
    index = 1
    reader = open(filename, 'rb', buffering=0)
    tensor_size = sizes[dim_offsets[index]:dim_offsets[index + 1]]
    a = np.empty(tensor_size, dtype=dtype)
    offset = int(data_offsets[index] * dtype_size)
    reader.seek(offset)
    reader.readinto(a)
    print(a)


if __name__ == '__main__':
    build_and_read()
