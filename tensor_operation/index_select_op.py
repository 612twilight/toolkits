# -*- coding:utf-8 -*-
"""
-------------------------------------------------
Project Name: toolkits
File Name: index_select_op.py
Author: gaoyw
Create Date: 2021/5/28
Description: 
-------------------------------------------------
"""
import numpy as np
import torch


def index_select_op():
    hn = torch.FloatTensor(
        np.array([
            [[111, 112, 113], [121, 122, 123], [131, 132, 133], [141, 142, 143]],
            [[211, 212, 213], [221, 222, 223], [231, 232, 233], [241, 242, 243]]
        ])
    )  # 编码后的向量(2,4,3) 分别对应着bsz,time,hidden
    index = torch.tensor(np.array([0, 1, 2]), dtype=torch.int64)
    selected_hn = hn.index_select(dim=1, index=index)
    # 获取的是dim为1 ，里面的数值
    print(selected_hn)
    result = hn[:, index, :]
    print(result)
    assert selected_hn.equal(result)


if __name__ == '__main__':
    index_select_op()
