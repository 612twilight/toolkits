# -*- coding:utf-8 -*-
"""
-------------------------------------------------
Project Name: toolkits
File Name: args_demo.py
Author: gaoyw
Create Date: 2021/6/28
Description: 
-------------------------------------------------
"""


def accept_param(input_ids):
    print(input_ids)


def accept_param_kwargs(input_ids, input_ids2=None, **kwargs):
    print(input_ids)
    print(input_ids2)
    print(kwargs)


def accept_args_kwargs(input_ids, input_ids2=None, *args, **kwargs):
    print(input_ids)
    print(input_ids2)
    print(kwargs)
    print(args)


def test_args_kwargs():
    input_ids = 1
    other_input = 2
    accept_param_kwargs(*[input_ids], **{"input_ids2": input_ids, "other_input": other_input})  # allow
    accept_param_kwargs(**{"input_ids": input_ids, "input_ids2": input_ids, "other_input": other_input})  # allow
    accept_param_kwargs(**{"input_ids": input_ids, "other_input": other_input})  # allow
    accept_param_kwargs(input_ids, **{"input_ids2": input_ids, "other_input": other_input})  # allow
    accept_param_kwargs(input_ids, input_ids, **{"other_input": other_input})  # allow
    accept_args_kwargs(input_ids, input_ids, *[2, 3, 4],
                       **{"other_input": other_input, "other_input2": other_input})  # allow

    accept_args_kwargs(input_ids, input_ids, 15, *[2, 3, 4],
                       **{"other_input": other_input, "other_input2": other_input}, extra_input=6)  # allow 将没有命名的自动组织


if __name__ == '__main__':
    test_args_kwargs()
