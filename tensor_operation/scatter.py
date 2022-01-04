# -*- coding:utf-8 -*-
"""
-------------------------------------------------
Project Name: toolkits
File Name: scatter.py
Author: gaoyw
Create Date: 2021/9/27
Description: 
-------------------------------------------------
"""
import torch


def scatter_add_test():
    batch_size = 3
    output_length = 4
    src_length = 5
    num_type = 10
    src_token = torch.randint(0,num_type, (batch_size, src_length))
    index = src_token[:, None, :]
    index = index.expand(batch_size, output_length, src_length)
    print(index.size())
    print(index)
    attn = torch.rand(batch_size, output_length, src_length).float()
    print(attn)
    attn_dists_size = (batch_size, output_length, num_type)
    attn_dists = attn.new_zeros(attn_dists_size)
    """
    :attr:`self`, :attr:`index` and :attr:`src` should have same number of
        dimensions. It is also required that ``index.size(d) <= src.size(d)`` for all
        dimensions ``d``, and that ``index.size(d) <= self.size(d)`` for all dimensions
        ``d != dim``.
        
    """
    attn_dists.scatter_add_(2, index, attn)
    print(attn_dists)


# def test2():
#     x = torch.rand(2, 3,5)
#     print(x)
#     res = torch.ones(3, 5).scatter_add_(1, torch.tensor([[0, 1, 2, 0, 0], [2, 0, 0, 1, 2]]), x)
#     print(res)


if __name__ == '__main__':
    scatter_add_test()
