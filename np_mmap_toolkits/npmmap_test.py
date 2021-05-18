# -*- coding:utf-8 -*-
"""
-------------------------------------------------
Project Name: toolkits
File Name: npmmap_test.py
Author: gaoyw
Create Date: 2021/5/13
-------------------------------------------------
"""

import os.path as path
from tempfile import mkdtemp

import numpy as np


def _warmup_mmap_file(path):
    with open(path, "rb") as stream:
        while stream.read(100 * 1024 * 1024):
            pass


def mmap_write_and_write():
    data = np.arange(12, dtype='float32')
    data.resize((3, 4))
    print("内存中创立的对象{}".format(data))
    filename = path.join(mkdtemp(), 'newfile.dat')
    fp = np.memmap(filename, dtype='float32', mode='w+', shape=(3, 4))
    fp[:] = data[:]
    assert fp.filename == path.abspath(filename)
    fp.flush()
    newfp = np.memmap(filename, dtype='float32', mode='r', shape=(3, 4))
    print("写入后，mmap中的对象\n{}".format(newfp))

    fpr = np.memmap(filename, dtype='float32', mode='r', shape=(3, 4))  # 只读
    assert not fpr.flags.writeable

    fpc = np.memmap(filename, dtype='float32', mode='c', shape=(3, 4))  # 可读写
    assert fpc.flags.writeable
    fpc[0, :] = 0  # 这里只是写入内存，没有写入磁盘，fpr里面的没有变
    print("对mmap可读写模式下第0行数据进行了改写")
    print("fpc[0, :]发生了改变{}".format(fpc[0, :]))
    print("fpr[0, :]没有发生改变{}".format(fpr[0, :]))
    print("说明可读写模式下只对自身内存里的生效，对文件中没有修改")

    fpo = np.memmap(filename, dtype='float32', mode='r', offset=16)
    print("使用偏移量offset=16开始进行读，得到的结果{}".format(fpo))


def frombuffer_read_and_write():
    dtype = np.float32
    dtype_size = dtype().itemsize
    filename = path.join(mkdtemp(), 'newfile.dat')
    data = np.arange(12, dtype=dtype)
    data.resize((3, 4))
    file_writer = open(filename, "wb")
    for i in data:
        print(i)
        file_writer.write(i.tobytes(order="C"))
    file_writer.flush()
    file_writer.close()
    _warmup_mmap_file(filename)
    buffer = np.memmap(filename, mode='r', order='C')
    buffer = memoryview(buffer)
    # count = 10 * dtype_size
    count = 2
    offset_count = 5
    offset = offset_count * dtype_size
    # 起始偏移量，从flat之后的第index为offset_count元素开始，往后读取count个元素
    result = np.frombuffer(buffer, dtype=dtype, offset=offset, count=count)
    print(result)
    result = np.frombuffer(buffer, dtype=dtype, offset=offset, count=count)
    print(result)


if __name__ == '__main__':
    frombuffer_read_and_write()
