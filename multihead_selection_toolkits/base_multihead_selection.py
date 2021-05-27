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
    hn = torch.tensor(
        np.array([
            [[111, 112, 113], [121, 122, 123], [131, 132, 133]],
            [[211, 212, 213], [221, 222, 223], [231, 232, 233]]
        ])
    )  # (2,3,3)
    relation_emb = nn.Embedding(num_embeddings=10, embedding_dim=3)
    print(relation_emb)
    print(relation_emb.weight)
    B, L, H = hn.size()
    u = hn.unsqueeze(1).expand(B, L, L, -1)
    print(u)
    v = hn.unsqueeze(2).expand(B, L, L, -1)
    print(v)
    uv = torch.cat((u, v), dim=-1)
    print(uv)
    selection_logits = torch.einsum('bijh,rh->birj', uv, relation_emb.weight)
    print(selection_logits)


if __name__ == '__main__':
    classical_multihead_selection()
