# -*- coding:utf-8 -*-
"""
-------------------------------------------------
Project Name: toolkits
File Name: pack_pad.py
Author: gaoyw
Create Date: 2021/3/9

pack_padded_sequence
输入的数据是经过pad的，比如输入shape为2，3,4，共有两个句子，句子最大长度为3，embedding维度为4
而两个句子的真实的长度：3,2

关于batch_first
在输入进入pack_padded_sequence中后，如果batch_first是True
则原始数据不用变化，以原shape输入即可，
pack_padded_sequence之后的数据shape为：3,2，同时，其数据项shape为5,4，已经移除了pad的字，这里的数据项顺序为
第一句的第一个，第二句的第一个，第一句的第二个，第二句的第二个。。。。碰到pad则不纳入其中


假如输入在进入pack_padded_sequence中后，如果batch_first是False
则原始数据需要进行转置，以[1,0,2]进行转置，即时间步放到第0维度来
除此之外，输出的是一样的


关于enforce_sorted

如果enforce_sorted参数设置为True
那么输入的lengths必须是降序的
若果enforce_sorted参数设置是False
那么不在意lengths的顺序，但是

-------------------------------------------------
"""
import torch
from torch import nn


def rnn_forwarder(rnn, inputs, seq_lengths, enforce_sorted=True):
    """
    :param rnn: RNN instance
    :param inputs: FloatTensor, shape [batch, time, dim] if rnn.batch_first else [time, batch, dim]
    :param seq_lengths: LongTensor shape [batch]
    :return: the result of rnn layer,
    """
    batch_first = rnn.batch_first
    # assume seq_lengths = [3, 5, 2]
    # 对序列长度进行排序(降序), sorted_seq_lengths = [5, 3, 2]
    # indices 为 [1, 0, 2], indices 的值可以这么用语言表述
    # 原来 batch 中在 0 位置的值, 现在在位置 1 上.
    # 原来 batch 中在 1 位置的值, 现在在位置 0 上.
    # 原来 batch 中在 2 位置的值, 现在在位置 2 上.
    # sorted_seq_lengths, indices = torch.sort(seq_lengths, descending=True)

    # 如果我们想要将计算的结果恢复排序前的顺序的话,
    # 只需要对 indices 再次排序(升序),会得到 [0, 1, 2],
    # desorted_indices 的结果就是 [1, 0, 2]
    # 使用 desorted_indices 对计算结果进行索引就可以了.
    # _, desorted_indices = torch.sort(indices, descending=False)

    # 对原始序列进行排序
    # if batch_first:
    #     inputs = inputs[indices]
    # else:
    #     inputs = inputs[:, indices]
    print("no packed result is : ")
    print(inputs)
    print(inputs.size())
    packed_inputs = nn.utils.rnn.pack_padded_sequence(inputs,
                                                      seq_lengths,
                                                      batch_first=batch_first, enforce_sorted=enforce_sorted)
    print("packed result is : ")
    print(packed_inputs)
    print(packed_inputs.data.size())
    res, state = rnn(packed_inputs)

    padded_res, _ = nn.utils.rnn.pad_packed_sequence(res, batch_first=batch_first)

    # # 恢复排序前的样本顺序
    # if batch_first:
    #     desorted_res = padded_res[desorted_indices]
    # else:
    #     desorted_res = padded_res[:, desorted_indices]
    # return desorted_res
    return padded_res


def version_1():
    """
    该种情形会还原顺序
    """
    bs = 3
    max_time_step = 5
    feat_size = 15
    hidden_size = 2
    seq_lengths = torch.tensor([5, 3, 2], dtype=torch.long)

    rnn = nn.GRU(input_size=feat_size,
                 hidden_size=hidden_size, batch_first=True, bidirectional=True)
    x = torch.randn([bs, max_time_step, feat_size])

    using_packed_res = rnn_forwarder(rnn, x, seq_lengths)
    print("没有混淆长度")
    print(using_packed_res)

    mix_index = [0, 2, 1]
    print("输入序列长度")
    print(seq_lengths[mix_index])
    using_packed_res = rnn_forwarder(rnn, x[mix_index], seq_lengths[mix_index], enforce_sorted=False)
    print("输出的就是我们输入的长度，乱序的，也是我们需要的")
    print(using_packed_res)
    # print("还原回原长度，注意这里与混淆长度后的rnn输入的不同")
    # print(using_packed_res[mix_index])

    # 不使用 pack_paded, 用来和上面的结果对比一下.
    not_packed_res, _ = rnn(x)
    print(not_packed_res)


def version_2():
    import torch
    import numpy as np

    input = torch.from_numpy(np.array([[1, 2, 3, 4], [5, 6, 7, 0], [9, 3, 0, 0]]))
    length = [4, 3, 2]  # lengths array has to be sorted in decreasing order
    result = torch.nn.utils.rnn.pack_padded_sequence(input, lengths=length, batch_first=True)

    print("==============二维输出=============")
    print(result)

    # input = torch.randn(8,10,300)
    # length = [10,10,10,10,10,10,10,10]
    # 注意，这里length代表每一个batch里面数据的长度，length的数量是8个，因为对应batch_first=True，也就是input的第一维是8个，也就是有8个batch
    # perm = torch.LongTensor(range(8))
    # result = torch.nn.utils.rnn.pack_padded_sequence(input[perm],lengths=length,batch_first=True)
    # print(result)

    input = torch.randn(2, 3, 4)  # bsz,seq_len,hidden_dim
    print("===========三维原始向量================")
    print(input)
    length = [3, 2]  # 只有两个句子
    perm = torch.LongTensor(range(2))  # 这里是表达转置，不用转置了
    result = torch.nn.utils.rnn.pack_padded_sequence(input[perm], lengths=length, batch_first=True)
    print("=============三维原始向量==batchsize变换============")
    print(result)

    # input = torch.randn(2, 3, 4)  # bsz,seq_len,hidden_dim
    input = input.permute([1, 0, 2])  # time first  shape: 3, 2, 4
    print("===========三维原始向量================")
    print(input)
    length = [3, 2]  # 原先已经将时间步放到最前面了，所以有三个句子
    result = torch.nn.utils.rnn.pack_padded_sequence(input, lengths=length)
    print("=============三维原始向量==batchsize 不等于true变换============")
    print(result)


def version_3():
    import torch

    rnn = nn.GRU(input_size=4,
                 hidden_size=4, batch_first=True, bidirectional=True)

    input = torch.randn(6, 5, 4)  # bsz,seq_len,hidden_dim
    print("===========三维原始向量================")
    print(input)
    length = [5, 4, 3, 2, 2, 2]  # 句子长度
    result = torch.nn.utils.rnn.pack_padded_sequence(input, lengths=length, batch_first=True, enforce_sorted=True)
    print("=============三维原始向量==batch_first=True, enforce_sorted=True变换============")
    print(result)
    print(result.data.size())

    rnn(result)

    length = [3, 4, 5, 2, 2, 2]  # 句子长度
    result = torch.nn.utils.rnn.pack_padded_sequence(input, lengths=length, batch_first=True, enforce_sorted=False)
    print("=============三维原始向量==batch_first=True, enforce_sorted=False变换============")
    print(result)
    print(result.data.size())

    # input = torch.randn(2, 3, 4)  # bsz,seq_len,hidden_dim
    input = input.permute([1, 0, 2])  # time first  shape: 3, 2, 4
    print("===========三维原始向量================")
    print(input)
    length = [5, 4, 3, 2, 2, 2]  # 原先已经将时间步放到最前面了，所以有三个句子
    result = torch.nn.utils.rnn.pack_padded_sequence(input, lengths=length)
    print("=============三维原始向量==batchsize 不等于true变换============")
    print(result)


def correct_yanshi():
    """
    正确使用方法
    """
    import random
    feat_size = 100
    hidden_size = 100
    bsz = 500
    max_length = 200
    rnn = nn.GRU(input_size=feat_size,
                 hidden_size=hidden_size, batch_first=True, bidirectional=True)
    embedding = torch.randn(bsz, max_length, feat_size)
    lengths = list(sorted([random.randint(1, max_length) for i in range(bsz)], reverse=True))
    packed_inputs = nn.utils.rnn.pack_padded_sequence(embedding,
                                                      lengths,
                                                      batch_first=True, enforce_sorted=True)
    print(packed_inputs)
    res, state = rnn(packed_inputs)
    print(res)

    padded_res, _ = nn.utils.rnn.pad_packed_sequence(res, batch_first=True)
    print(padded_res)


def correct_yanshi2():
    """
    正确使用方法,不需要有序
    """
    import random
    feat_size = 100
    hidden_size = 100
    bsz = 500
    max_length = 200
    rnn = nn.GRU(input_size=feat_size,
                 hidden_size=hidden_size, batch_first=True, bidirectional=True)
    embedding = torch.randn(bsz, max_length, feat_size)
    lengths = [random.randint(1, max_length) for i in range(bsz)]  # 可以无序
    packed_inputs = nn.utils.rnn.pack_padded_sequence(embedding,
                                                      lengths,
                                                      batch_first=True, enforce_sorted=False)
    print(packed_inputs)
    res, state = rnn(packed_inputs)
    print(res)

    padded_res, _ = nn.utils.rnn.pad_packed_sequence(res, batch_first=True, total_length=max_length)
    # total_length 由于输入数据中可能每个数据都被padding了，所以这里如果想要补全，需要提供补全到的长度
    print(padded_res)


if __name__ == "__main__":
    correct_yanshi()
