# -*- coding:utf-8 -*-
"""
-------------------------------------------------
Project Name: toolkits
File Name: selected_multihead_selection.py
Author: gaoyw
Create Date: 2021/5/28
Description: 有时候，我们不需要进行完全形式的笛卡尔积两两运算，只需要进行一部分运算
-------------------------------------------------
"""
import numpy as np
import torch

from torch import nn


def test_argmax_1():
    """
    这种情形需要创建矩阵，创建过程无法反向传播
    """
    ner_label = [
        [1, 1, 2, 3, 0],
        [0, 0, 2, 3, 0],
        [0, 1, 0, 3, 0]
    ]
    ner_label = np.array(ner_label)
    ner_label = torch.tensor(ner_label)
    bsz = ner_label.size(0)
    seq_len = ner_label.size(1)
    not_eq_0 = ~ner_label.eq(0)
    sum_result = torch.sum(not_eq_0, dim=-1)
    max_entity = sum_result.max().int()
    result = not_eq_0.unsqueeze(-1).unsqueeze(1).expand(bsz, max_entity, seq_len, -1)  # bsz,max_entity,seq_len,1
    # max_entity维度应该是每个只有一个实体
    # result应该与一个mask矩阵相乘
    print(result)
    hidden_dim = 5
    hidden = torch.rand(bsz, seq_len, hidden_dim)
    hidden = hidden.unsqueeze(1).expand(bsz, max_entity, seq_len, hidden_dim)
    side = hidden * result
    print(side)
    print(side.size())

def test_argmax_2():
    """
    这里继续使用单独抽取的技术吧
    这里从标签矩阵里面获取所需标签位置信息，最多实体数目，然后利用标签信息构建mask矩阵
    """
    ner_label = [
        [1, 1, 2, 3, 0],
        [0, 0, 2, 3, 0],
        [0, 1, 0, 3, 0]
    ]
    ner_label = np.array(ner_label)
    ner_label = torch.tensor(ner_label)
    bsz = ner_label.size(0)
    seq_len = ner_label.size(1)
    not_eq_0 = ~ner_label.eq(0)
    sum_result = torch.sum(not_eq_0, dim=-1)
    max_entity = sum_result.max().int()
    result = not_eq_0.unsqueeze(-1).unsqueeze(1).expand(bsz, max_entity, seq_len, -1)  # bsz,max_entity,seq_len,1
    # max_entity维度应该是每个只有一个实体
    # result应该与一个mask矩阵相乘
    print(result)
    hidden_dim = 5
    hidden = torch.rand(bsz, seq_len, hidden_dim)
    hidden = hidden.unsqueeze(1).expand(bsz, max_entity, seq_len, hidden_dim)
    side = hidden * result
    print(side)
    print(side.size())


def selected_multihead_selection():
    select_time_step = np.array([[0, 1, 2], [1, 2, 3]])  # 第一个batch，只选择0,1，2，第二个batch，只选择1,2,3
    select_time_step = torch.tensor(select_time_step, dtype=torch.int64)  # 第一个batch，只选择0,1，2，第二个batch，只选择1,2,3
    hn = torch.FloatTensor(
        np.array([
            [[111, 112, 113], [121, 122, 123], [131, 132, 133], [141, 142, 143]],
            [[211, 212, 213], [221, 222, 223], [231, 232, 233], [241, 242, 243]]
        ])
    )  # 编码后的向量(2,4,3) 分别对应着bsz,time,hidden
    embedding_weight = torch.FloatTensor(
        np.array([
            [1, 1, 1, 1, 1, 1],
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


if __name__ == '__main__':
    test_argmax()
