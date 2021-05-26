# -*- coding:utf-8 -*-
"""
-------------------------------------------------
Project Name: toolkits
File Name: view_operation.py
Author: gaoyw
Create Date: 2021/5/26
Description: 
-------------------------------------------------
"""
import numpy as np
import torch


def oneD_view():
    print("===============oneD test begin==============")
    tensor = torch.tensor(np.array([1, 2, 3]))  # (3,)
    print("before_1D:\n{}".format(tensor))
    transform = tensor.view((-1, 1))  # (3,1)
    print("after_1D:\n{}".format(transform))
    print("===============oneD test end================")


def twoD_view():
    print("===============twoD test begin==============")
    tensor = torch.tensor(np.array([[1, 2, 3], [4, 5, 6]]))  # (2.3)
    print("before_2D:\n{}".format(tensor))
    transform = tensor.view((-1, 1))  # (6,1)
    print("after_2D:\n{}".format(transform))
    print("===============twoD test end================")


def threeD_view():
    """
    对于3D的转换在自然语言处理中比较常见，场景也比较复杂，
    测试其中一种场景：
    当我们使用lstm的双向模式，并且设置batch_first=True时，我们得到的hn的shape为（2，time_step,hidden_dim）
    假设如下：
    tensor([[[111, 112, 113],
            [121, 122, 123],
            [131, 132, 133]],

           [[211, 212, 213],
            [221, 222, 223],
            [231, 232, 233]]], dtype=torch.int32)
    我们预得到的是：
    tensor([[111, 112, 113, 211, 212, 213],
            [121, 122, 123, 221, 222, 223],
            [131, 132, 133, 231, 232, 233]], dtype=torch.int32)
    那这时候的操作可以是：
    permute_hn = hn.permute(1, 0, 2).contiguous()
    transform = permute_hn.view((3, 6))
    assert transform.equal(target)  # True



    """
    print("===============threeD test begin==============")
    hn = torch.tensor(np.array([[[111, 112, 113], [121, 122, 123], [131, 132, 133]],
                                [[211, 212, 213], [221, 222, 223], [231, 232, 233]]]))  # (2,3,3)
    target = torch.tensor(np.array([[111, 112, 113, 211, 212, 213],
                                    [121, 122, 123, 221, 222, 223],
                                    [131, 132, 133, 231, 232, 233]]))  # (3,6)
    print("before_2D:\n{}".format(hn))
    print("hn_first_seq:\n{}".format(hn[0, :, :]))
    permute_hn = hn.permute(1, 0, 2).contiguous()
    print("permute_hn:\n{}".format(permute_hn))
    print("permute_hn_first_seq:\n{}".format(permute_hn[:, 0, :]))
    transform = permute_hn.view((3, 6))
    assert transform.equal(target)
    print("after_2D:\n{}".format(transform))
    print("===============threeD test end================")


if __name__ == '__main__':
    oneD_view()
    twoD_view()
    threeD_view()
