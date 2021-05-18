# -*- coding:utf-8 -*-
"""
-------------------------------------------------
Project Name: toolkits
File Name: simple_attention.py
Author: gaoyw
Create Date: 2021/5/18
-------------------------------------------------
"""
import numpy as np
import torch
import torch.nn.functional as F
from torch import nn


class SimpleAttention(nn.Module):
    def __init__(self, hidden_size):
        super(SimpleAttention, self).__init__()
        # params
        self.hidden_size = hidden_size

        self.query_layer = torch.nn.Sequential(nn.Linear(self.hidden_size, self.hidden_size), nn.Tanh())
        self.key_layer = torch.nn.Parameter(torch.FloatTensor(self.hidden_size))

    def forward(self, x, lengths):
        # x-> bsz,seq_len,hidden_size
        query = self.query_layer(x)  # bsz,seq_len,hidden_size
        print("query.size():{}".format(query.size()))
        attn_weight = query.matmul(self.key_layer)  # bsz,seq_len  # 这里就认为是计算得到的权重了
        print("atten_weight.size():{}".format(attn_weight.size()))
        attended_outputs = torch.stack(
            [F.softmax(attn_weight[i, :lengths[i]], dim=0).matmul(x[i, :lengths[i]]) for i in
             range(len(lengths))], dim=0)
        # F.softmax(attn_weight[i, :lengths[i]], dim=0)  (seq_len,)
        # x[i, :lengths[i]]  seq_len,dim
        # F.softmax(attn_weight[i, :lengths[i]], dim=0).matmul(x[i, :lengths[i]])  bsz,dim
        # 这种只能生成一个基于attention的句子表征向量
        print(attended_outputs.size())
        return attended_outputs


def test_simpleattention():
    hidden_size = 5
    input_tensor = torch.FloatTensor(np.arange(2 * 3 * hidden_size, ).reshape(2, 3, hidden_size))
    print(input_tensor)
    decoder = SimpleAttention(hidden_size=hidden_size)
    result = decoder(input_tensor, lengths=[3, 4])
    print(result)


class SelfAttention(nn.Module):
    def __init__(self, hidden_size):
        super(SelfAttention, self).__init__()
        # params
        self.hidden_size = hidden_size

        self.query_layer = torch.nn.Sequential(nn.Linear(self.hidden_size, self.hidden_size), nn.Tanh())
        self.key_layer = torch.nn.Parameter(torch.FloatTensor(self.hidden_size))

    def forward(self, x, lengths):
        # x-> bsz,seq_len,hidden_size
        query = self.query_layer(x)  # bsz,seq_len,hidden_size
        print("query.size():{}".format(query.size()))
        attn_weight = query.matmul(self.key_layer)  # bsz,seq_len  # 这里就认为是计算得到的权重了
        print("atten_weight.size():{}".format(attn_weight.size()))
        attended_outputs = torch.stack(
            [F.softmax(attn_weight[i, :lengths[i]], dim=0).matmul(x[i, :lengths[i]]) for i in
             range(len(lengths))], dim=0)
        # F.softmax(attn_weight[i, :lengths[i]], dim=0)  (seq_len,)
        # x[i, :lengths[i]]  seq_len,dim
        # F.softmax(attn_weight[i, :lengths[i]], dim=0).matmul(x[i, :lengths[i]])  bsz,dim
        # 这种只能生成一个基于attention的句子表征向量
        print(attended_outputs.size())
        return attended_outputs

if __name__ == '__main__':
    pass
