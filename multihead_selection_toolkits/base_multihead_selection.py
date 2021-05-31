# -*- coding:utf-8 -*-
"""
-------------------------------------------------
Project Name: toolkits
File Name: base_multihead_selection.py
Author: gaoyw
Create Date: 2021/5/27
Description: 
-------------------------------------------------
"""
import numpy as np
import torch

from torch import nn


def classical_multihead_selection():
    """
    经典的多头选择机制
    """
    hn = torch.FloatTensor(
        np.array([
            [[111, 112, 113], [121, 122, 123], [131, 132, 133]],
            [[211, 212, 213], [221, 222, 223], [231, 232, 233]]
        ])
    )  # 编码后的向量(2,3,3) 分别对应着bsz,time,hidden
    embedding_weight = torch.FloatTensor(
        np.array([[1, 1, 1, 1, 1, 1],
                  [0, 0, 0, 0, 0, 0],
                  [1, 1, 1, 1, 1, 1],
                  [0, 0, 0, 0, 0, 0],
                  [1, 1, 1, 1, 1, 1],
                  [0, 0, 0, 0, 0, 0],
                  [1, 1, 1, 1, 1, 1],
                  [0, 0, 0, 0, 0, 0],
                  [1, 1, 1, 1, 1, 1],
                  [0, 0, 0, 0, 0, 0],
                  ])
    )  # 类别embedding，固定初始化便于校验计算
    relation_emb = nn.Embedding(num_embeddings=10, embedding_dim=6, _weight=embedding_weight)
    # relation_emb = nn.Embedding(num_embeddings=10, embedding_dim=6)
    print(relation_emb)
    print(relation_emb.weight)
    B, L, H = hn.size()
    u = hn.unsqueeze(1).expand(B, L, L, -1)
    print(u)
    v = hn.unsqueeze(2).expand(B, L, L, -1)
    print(v)
    uv = torch.cat((u, v), dim=-1)  # 进行不同时间步的笛卡尔积组合，形成bsz,time,time,2*hidden
    print(uv)
    selection_logits = torch.einsum('bijh,rh->birj', uv, relation_emb.weight)
    # 生成类别logits，这里用的是爱因斯坦求和约定 即 birj = \sum{h}{bijh*rh}
    print("bijh,rh->birj:\n{}".format(selection_logits))
    # 这里进行一下验证
    h_all = uv.size(-1)
    b = 1
    i = 2
    r = 2
    j = 1
    need_cal = selection_logits[b, i, r, j]
    result = []
    for h in range(h_all):
        result.append(uv[b, i, j, h] * relation_emb.weight[r, h])
    cal_result = sum(result)
    print("birj中1,2,2,1的值为:\n{}".format(need_cal))
    print("自己计算得到的值为{}".format(cal_result))


    # 下面是验证一下爱因斯坦求和约定的一些功能，
    # 我们换一种表述，先得到的维度是bijr，然后转置为bijr，
    # 其结果与上述计算一样，所以求和约定表述能力很强
    tmp_logits = torch.einsum('bijh,rh->bijr', uv, relation_emb.weight)
    print('bijh,rh->bijr:\n{}'.format(tmp_logits))
    result = torch.einsum('birj->bijr', selection_logits)
    print("bijh,rh->birj->bijr:\n{}".format(result))
    assert result.equal(tmp_logits)


if __name__ == '__main__':
    classical_multihead_selection()
