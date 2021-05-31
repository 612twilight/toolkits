# -*- coding:utf-8 -*-
"""
-------------------------------------------------
Project Name: toolkits
File Name: mask_select_op.py
Author: gaoyw
Create Date: 2021/5/28
Description: 
-------------------------------------------------
"""

import numpy as np
import torch


def masked_select_op():
    hn = torch.FloatTensor(
        np.array([
            [[111, 112, 113], [121, 122, 123], [131, 132, 133], [141, 142, 143]],
            [[211, 212, 213], [221, 222, 223], [231, 232, 233], [241, 242, 243]]
        ])
    )  # 编码后的向量(2,4,3) 分别对应着bsz,time,hidden
    mask_index = torch.tensor(np.array([[[1, 1, 1], [1, 1, 1], [1, 1, 1], [0, 0, 0]],
                                        [[0, 0, 0], [1, 1, 1], [1, 1, 1], [1, 1, 1]]]),
                              dtype=torch.bool)  # 第一个batch，只选择0,1，2，第二个batch，只选择1,2,3
    mask_result = hn.masked_select(mask_index)
    print(mask_result)


if __name__ == '__main__':
    masked_select_op()
