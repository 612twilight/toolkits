# -*- coding:utf-8 -*-
"""
-------------------------------------------------
Project Name: toolkits
File Name: permute_operation.py
Author: gaoyw
Create Date: 2021/5/26
Description: 
-------------------------------------------------
"""
import numpy as np
import torch


def threeD_permute():
    """
    对于3D的permute在自然语言处理中比较常见，场景也比较复杂，
    比如我们传入的顺序是bsz,time_step,dim
    但是实际上有的模型可以时间步优先，
    我们需要的是 time_step,bsz,dim
    测试其中一种场景：
    输入的tensor 是 (2，3, 3)
    hn = tensor([[[111, 112, 113],
            [121, 122, 123],
            [131, 132, 133]],

           [[211, 212, 213],
            [221, 222, 223],
            [231, 232, 233]]], dtype=torch.int32)

    可以获取第一句的tensor
    hn_first_seq = hn[0, :, :]
    tensor([[111, 112, 113],
            [121, 122, 123],
            [131, 132, 133]], dtype=torch.int32)

    这里进行一下转换
    permute_hn = hn.permute(1, 0, 2).contiguous()
    permute_hn：
    tensor([[[111, 112, 113],
             [211, 212, 213]],

            [[121, 122, 123],
             [221, 222, 223]],

           [[131, 132, 133],
            [231, 232, 233]]], dtype=torch.int32)
    那这时候再去获取第一句的tensor就变成了
    permute_hn_first_seq = permute_hn[:, 0, :]

    assert hn_first_seq.equal(permute_hn_first_seq)

    那这时候的操作可以是：
    permute_hn = hn.permute(1, 0, 2).contiguous()
    transform = permute_hn.view((3, 6))
    assert transform.equal(target)  # True
    """
    print("===============threeD test begin==============")
    hn = torch.tensor(np.array([[[111, 112, 113], [121, 122, 123], [131, 132, 133]],
                                [[211, 212, 213], [221, 222, 223], [231, 232, 233]]]))  # (2,3,3)
    print("before_2D:\n{}".format(hn))
    hn_first_seq = hn[0, :, :]
    print("hn_first_seq:\n{}".format(hn_first_seq))
    permute_hn = hn.permute(1, 0, 2).contiguous()
    print("permute_hn:\n{}".format(permute_hn))
    permute_hn_first_seq = permute_hn[:, 0, :]
    print("permute_hn_first_seq:\n{}".format(permute_hn_first_seq))
    assert hn_first_seq.equal(permute_hn_first_seq)
    print("===============threeD test end================")


if __name__ == '__main__':
    threeD_permute()
