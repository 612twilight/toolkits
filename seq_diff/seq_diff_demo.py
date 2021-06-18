# -*- coding:utf-8 -*-
"""
-------------------------------------------------
Project Name: toolkits
File Name: seq_diff_demo.py
Author: gaoyw
Create Date: 2021/6/18
Description: 
-------------------------------------------------
"""
import difflib

a = "阿里巴巴达摩院"
b = "阿里巴巴"
score = difflib.SequenceMatcher(None, a, b).ratio()
print(score)
