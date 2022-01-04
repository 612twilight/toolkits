# -*- coding:utf-8 -*-
"""
-------------------------------------------------
Project Name: toolkits
File Name: mul.py
Author: gaoyw
Create Date: 2021/9/27
Description: 
-------------------------------------------------
"""
import torch


def mul_op():
    gen_dists = torch.arange(0, 3 * 4 * 5).view(3, 4, 5)
    print(gen_dists)
    p_gens = torch.sigmoid(torch.arange(0, 3 * 4 * 1).view(3, 4, 1).float())
    print(p_gens)
    result = torch.mul(gen_dists, p_gens)  # (batch, tgt_len, num_embeddings) (batch, tgt_len, 1)
    print(result)


if __name__ == '__main__':
    mul_op()
