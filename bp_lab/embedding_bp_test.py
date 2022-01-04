# -*- coding:utf-8 -*-
"""
-------------------------------------------------
Project Name: toolkits
File Name: embedding_bp_test.py
Author: gaoyw
Create Date: 2021/9/2
Description: 
-------------------------------------------------
"""

import torch
from torch import nn
import torch.nn.functional as F

class DemoEmbedding(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.embedding = torch.nn.Embedding(num_embeddings=10, embedding_dim=4)
        self.fc = torch.nn.Linear(in_features=4, out_features=5)
        self.loss_fun = nn.CrossEntropyLoss()


    def forward(self, x,y):
        embed = self.embedding(x)  # 1,2,4
        logits = self.fc(embed)  # 1,2,3
        prop = F.softmax(logits, dim=-1).view(-1,5)
        print(prop.size())
        loss = self.loss_fun(prop, y)
        return loss


if __name__ == '__main__':
    import numpy as np

    model = DemoEmbedding()
    print(model.embedding.weight)
    import random

    model.train()
    optimization = torch.optim.SGD(params=model.parameters(), lr=0.1)
    loss_fun = nn.CrossEntropyLoss()
    for i in range(100):
        optimization.zero_grad()
        x = torch.LongTensor(np.array([[random.randint(0, 1), random.randint(0, 1)]]))
        y = torch.tensor([[random.randint(0, 2), random.randint(0, 2)]])
        loss = model(x,y)
        loss.backward()
        optimization.step()
    print(model.embedding.weight)
