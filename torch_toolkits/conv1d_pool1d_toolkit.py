# -*- coding:utf-8 -*-
"""
-------------------------------------------------
Project Name: toolkits
File Name: conv1d_pool1d_toolkit.py
Author: gaoyw
Create Date: 2021/1/11
-------------------------------------------------
"""
import numpy as np
import torch
from torch import nn


def conv1d_pool1d_test():
    max_seq_len = 10
    filter_size = 4
    bsz = 5
    embedding_dim = 5
    num_filters = 6
    embedding_layer = nn.Embedding(num_embeddings=50, embedding_dim=embedding_dim)
    conv1d = nn.Conv1d(in_channels=embedding_dim, out_channels=num_filters, kernel_size=filter_size)
    # N,C,L卷积后L变成了 L - kernel_size + 1，即max_seq_len-filter_size+1
    # 由于该池化层的kernel—size就是卷积后的-1维度大小，因此赤化就是剩下了最大的那个值
    pool1d_kernel_size = max_seq_len - filter_size + 1
    pool1d = nn.MaxPool1d(kernel_size=pool1d_kernel_size, stride=1)
    input_seq = torch.LongTensor(np.arange(max_seq_len * bsz).reshape(bsz, max_seq_len))
    print(input_seq)
    embedding = embedding_layer(input_seq)
    print("转置前的embedding大小为：{}".format(embedding.size()))
    embedding = embedding.permute(0, 2, 1)
    print("转置后的embedding大小为：{}".format(embedding.size()))
    convs = conv1d(embedding)
    print("卷积后、池化前的embedding大小为：{}".format(convs.size()))
    print("卷积后、池化前的embedding为：{}".format(convs))
    convs = nn.LeakyReLU()(convs)
    convs = pool1d(convs)
    print("池化层的kernel_size是：{}".format(pool1d_kernel_size))
    print("卷积后的embedding大小为：{}".format(convs.size()))


def pool1d_test():
    """
    池化1d是对一个N,C,L的矩阵进行池化，其中C是channel或者embedding维度，L是序列长度，对L维度进行池化的结果是
    找到了每个channel中L个值中最大的那个，也就是说对于一个原始的NLC，留下的是NC，其中C维度是每个L维度中最大的那个，
    假如有下面的NLC，
    1，2，3，4
    3,1,2,6
    4,3,2,5
    或者permute之后的NCL，
    1,3,4
    2,1,3
    3,2,2
    4,6,5
    那么经过L维度的最大卷积之后，就是
    4,3,3,6
    """
    max_seq_len = 10
    bsz = 4
    embedding_dim = 5
    pool1d_kernel_size = max_seq_len
    pool1d = nn.MaxPool1d(kernel_size=pool1d_kernel_size, stride=1)
    embedding = torch.Tensor(np.random.rand(max_seq_len * bsz * embedding_dim).reshape(bsz, max_seq_len, embedding_dim))
    print("转置前的embedding大小为：{}".format(embedding.size()))
    print("转置前的embedding为：{}".format(embedding))
    embedding = embedding.permute(0, 2, 1)
    print("转置后的embedding大小为：{}".format(embedding.size()))
    print("转置后的embedding为：{}".format(embedding))
    convs = pool1d(embedding)  # N,C,L进行池化是对L维度进行池化，依据kernel_size的维度，将对其进行最大池化，剩余的L维度变为L-pool1d_kernel_size+1
    print("池化层的kernel_size是：{}".format(pool1d_kernel_size))
    print("池化后的embedding大小为：{}".format(convs.size()))
    print("池化后的embedding为：{}".format(convs))


if __name__ == '__main__':
    pool1d_test()
