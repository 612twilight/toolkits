# -*- coding:utf-8 -*-
"""
-------------------------------------------------
Project Name: toolkits
File Name: select_op.py
Author: gaoyw
Create Date: 2021/5/28
Description: 
-------------------------------------------------
"""
import numpy as np
import torch


def select_op():
    hn = torch.FloatTensor(
        np.array([
            [[111, 112, 113], [121, 122, 123], [131, 132, 133], [141, 142, 143]],
            [[211, 212, 213], [221, 222, 223], [231, 232, 233], [241, 242, 243]]
        ])
    )  # 编码后的向量(2,4,3) 分别对应着bsz,time,hidden
    select_result = hn.select(dim=1, index=0)
    print(select_result)


def select_op2():
    src_tokens = torch.arange(0, 3 * 4).view(3, 4)
    print(src_tokens)
    index = src_tokens[:, None, :]
    print(index.size())
    index = index.expand(3, 5,4)
    print(index)


if __name__ == '__main__':
    select_op2()
