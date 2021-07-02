# -*- coding:utf-8 -*-
"""
-------------------------------------------------
Project Name: toolkits
File Name: tokenization_demo.py
Author: gaoyw
Create Date: 2021/3/8
transformers           3.1.0
-------------------------------------------------
"""
from transformers import AutoTokenizer, AutoModel


def transformers_tokenizer():
    tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path="E:\models/transformers/bert-base-chinese")
    model = AutoModel.from_pretrained(pretrained_model_name_or_path="E:\models/transformers/bert-base-chinese")
    clean_up_text = tokenizer.clean_up_tokenization("你好，世界！Hello world!")  # 清洗掉无用字符
    print(clean_up_text)  # 你好，世界！Hello world!
    tokens = tokenizer.tokenize(clean_up_text)  # 转成bert词表的字符,word piece 法
    print(tokens)  # ['你', '好', '，', '世', '界', '！', 'hello', 'world', '!']
    tokens_id = tokenizer.convert_tokens_to_ids(tokens)
    print(tokens_id)  # [872, 1962, 8024, 686, 4518, 8013, 8701, 8572, 106]
    result = tokenizer.encode(clean_up_text)
    print(result)  # [101, 872, 1962, 8024, 686, 4518, 8013, 8701, 8572, 106, 102]
    inputs = tokenizer(text="你好，世界！", text_pair="Hello world!", return_tensors="pt", padding=True)
    print(inputs)
    # {'input_ids': tensor([[ 101,  872, 1962, 8024,  686, 4518, 8013,  102, 8701, 8572,  106,  102]]), 'token_type_ids': tensor([[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]]), 'attention_mask': tensor([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])}
    inputs = tokenizer(text=["你好，世界！Hello world!"], return_tensors="pt")
    print(inputs)
    # {'input_ids': tensor([[ 101,  872, 1962, 8024,  686, 4518, 8013, 8701, 8572,  106,  102]]), 'token_type_ids': tensor([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]), 'attention_mask': tensor([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])}
    print(inputs.input_ids)
    # tensor([[ 101,  872, 1962, 8024,  686, 4518, 8013, 8701, 8572,  106,  102]])
    outputs = model(**inputs)  # 这里是bert-base，输出的是BaseModelOutputWithPooling
    """
    last_hidden_state (:obj:`torch.FloatTensor` of shape :obj:`(batch_size, sequence_length, hidden_size)`):
            Sequence of hidden-states at the output of the last layer of the model.
    pooler_output (:obj:`torch.FloatTensor` of shape :obj:`(batch_size, hidden_size)`):
        Last layer hidden-state of the first token of the sequence (classification token)
        further processed by a Linear layer and a Tanh activation function. The Linear
        layer weights are trained from the next sentence prediction (classification)
        objective during pretraining.
    """
    print(outputs[0].size())  # torch.Size([1, 11, 768])  last_hidden_state
    print(outputs[1].size())  # torch.Size([1, 768])  pooler_output  在第一个[CLS]上加入了全连接激活，作为句子特征


def transformers_tokenizer_multi_input():
    tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path="E:\models/transformers/bert-base-chinese")
    inputs = tokenizer(text=["你好，世界！Hello world!"], return_tensors="pt")
    print(inputs)
    print(inputs.input_ids.size())
    print(type(inputs.input_ids))
    print(type(inputs.token_type_ids))
    print(type(inputs.attention_mask))

    inputs = tokenizer(text=["你好，世界！Hello world!", "你好，世世世世世世！Hello world!"], return_tensors="pt", padding=True)
    print("2" * 100)
    print(inputs)
    print(inputs.input_ids.size())
    print(inputs.token_type_ids.size())

    inputs = tokenizer(
        text=[["你好，世界！Hello world!", "你好，世世！Hello world!"], ["你好，世界2！Hello world!", "你好，世世世世世世世世！Hello world!"]],
        return_tensors="pt", padding=True)
    print(inputs)
    print(inputs.input_ids.size())


def transformers_convert_to_id():
    tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path="E:\models/transformers/bert-base-chinese")

    inputs = tokenizer(
        text=[["你好，世界！Hello world!", "你好，世世！Hello world!"], ["你好，世界2！Hello world!", "你好，世世世世世世世世！Hello world!"]],
        return_tensors="pt", padding=True)
    print(inputs)
    tokens_id = inputs.input_ids[0]
    tokens = tokenizer.convert_ids_to_tokens(tokens_id)
    print(tokens)
    # ['[CLS]', '你', '好', '，', '世', '界', '！', 'hello', 'world', '!', '[SEP]', '你', '好', '，', '世', '世', '！', 'hello', 'world', '!', '[SEP]', '[PAD]', '[PAD]', '[PAD]', '[PAD]', '[PAD]', '[PAD]', '[PAD]']
    tokens_id = inputs.input_ids[1]
    tokens = tokenizer.convert_ids_to_tokens(tokens_id)
    print(tokens)
    # ['[CLS]', '你', '好', '，', '世', '界', '2', '！', 'hello', 'world', '!', '[SEP]', '你', '好', '，', '世', '世', '世', '世', '世', '世', '世', '世', '！', 'hello', 'world', '!', '[SEP]']


def transformer_tokenizer_max_len():
    tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path="E:\models/transformers/bert-base-chinese")
    inputs = tokenizer(text="你好，世界！Hello world!" * 500, return_tensors="pt", padding="max_length", max_length=10,
                       truncation=True)
    print(inputs)
    print(inputs.input_ids.size())
    print(inputs.token_type_ids.size())
    print(inputs.attention_mask.size())

    inputs = tokenizer(text=["你好，世界！Hello world!", "你好，世界！Hello world!", "你好，世界！Hello world!"], return_tensors="pt",
                       padding="max_length", max_length=512,
                       truncation=True)

    print(inputs)
    print(inputs.input_ids.size())
    print(inputs.token_type_ids.size())
    print(inputs.attention_mask.size())

    text = "你好，世界！Hello world!"
    inputs = tokenizer.encode(text, max_length=5, truncation=True)
    print(inputs)

    inputs = tokenizer.encode(text)
    print(inputs)


def token_classification_align():
    tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path="E:\models/transformers/bert-base-chinese")
    model = AutoModel.from_pretrained(pretrained_model_name_or_path="E:\models/transformers/bert-base-chinese")
    inputs = tokenizer(text="你好，世界！", text_pair="Hello world!", return_tensors="pt", padding="max_length",
                       max_length=512)
    print(inputs)

    outputs = model(**inputs)  # 这里是bert-base，输出的是BaseModelOutputWithPooling
    """
    last_hidden_state (:obj:`torch.FloatTensor` of shape :obj:`(batch_size, sequence_length, hidden_size)`):
            Sequence of hidden-states at the output of the last layer of the model.
    pooler_output (:obj:`torch.FloatTensor` of shape :obj:`(batch_size, hidden_size)`):
        Last layer hidden-state of the first token of the sequence (classification token)
        further processed by a Linear layer and a Tanh activation function. The Linear
        layer weights are trained from the next sentence prediction (classification)
        objective during pretraining.
    """
    print(outputs[0].size())  # torch.Size([1, 11, 768])  last_hidden_state
    print(outputs[1].size())  # torch.Size([1, 768])  pooler_output  在第一个[CLS]上加入了全连接激活，作为句子特征


def special_input():
    tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path="E:\models/transformers/bert-base-chinese")
    model = AutoModel.from_pretrained(pretrained_model_name_or_path="E:\models/transformers/bert-base-chinese")
    inputs = tokenizer(text="北京市朝阳区广渠路00号院甲000(珠江帝景东北角底商)", return_tensors="pt", padding="max_length", max_length=512)
    print(inputs)

    def model_input(**x):
        print(x)
        outputs = model(**x)  # 这里是bert-base，输出的是BaseModelOutputWithPooling
        """
        last_hidden_state (:obj:`torch.FloatTensor` of shape :obj:`(batch_size, sequence_length, hidden_size)`):
                Sequence of hidden-states at the output of the last layer of the model.
        pooler_output (:obj:`torch.FloatTensor` of shape :obj:`(batch_size, hidden_size)`):
            Last layer hidden-state of the first token of the sequence (classification token)
            further processed by a Linear layer and a Tanh activation function. The Linear
            layer weights are trained from the next sentence prediction (classification)
            objective during pretraining.
        """
        print(outputs[0].size())  # torch.Size([1, 11, 768])  last_hidden_state
        print(outputs[1].size())  # torch.Size([1, 768])  pooler_output  在第一个[CLS]上加入了全连接激活，作为句子特征

    model_input(**inputs)


def convert_inputs():
    tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path="E:\models/transformers/bert-base-chinese")
    # inputs = tokenizer(text="北京市朝阳区广渠路00号院甲000(珠江帝景东北角底商)", return_tensors="pt", padding="max_length", max_length=512)
    inputs = "北京市朝阳区广渠路00号院甲0000(珠江帝景东北角底商)"
    inputs = " ".join("北京市朝阳区广渠路00号院甲0000(珠江帝景东北角底商)")
    reslt = tokenizer.clean_up_tokenization(inputs)
    print(reslt)
    bert_out = tokenizer(text=inputs, return_tensors="pt", padding="max_length", max_length=512)
    print(bert_out)
    result = tokenizer.convert_tokens_to_ids([word for word in inputs])
    print(result)
    print(tokenizer.convert_ids_to_tokens(result))
    result = tokenizer.convert_ids_to_tokens(bert_out["input_ids"][0])
    print(result)

    tokens = [word for word in inputs]
    if len(tokens) > 510:
        tokens = tokens[:510]
    tokens = ["[CLS]"] + tokens + ["[SEP]"]
    token_ids = tokenizer.convert_tokens_to_ids(tokens)
    print(token_ids)
    len_tokens = len(token_ids)
    input_ids = token_ids + [tokenizer.pad_token_id] * (512 - len_tokens)
    token_type_ids = [0] * 512
    attention_mask = [1] * len_tokens + [0] * (512 - len_tokens)
    print("==========================")
    print(input_ids)
    print(bert_out["input_ids"][0].numpy().tolist())
    assert input_ids == bert_out["input_ids"][0].numpy().tolist()
    assert token_type_ids == bert_out["token_type_ids"][0].numpy().tolist()
    assert attention_mask == bert_out["attention_mask"][0].numpy().tolist()
    print(input_ids)
    print(token_type_ids)
    print(attention_mask)


def less_length_bert():
    """
    bert 可以输入低于512的字符串
    """
    tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path="E:\models/transformers/bert-base-chinese")
    model = AutoModel.from_pretrained(pretrained_model_name_or_path="E:\models/transformers/bert-base-chinese")
    inputs = tokenizer(text="北京市朝阳区广渠路00号院甲000(珠江帝景东北角底商)", return_tensors="pt", padding=True)
    print(inputs)
    result = model(**inputs)
    print(result[0])
    print(result[1])

    inputs = tokenizer(text="北京市朝阳区广渠路00号院甲000(珠江帝景东北角底商)", return_tensors="pt", padding="max_length", max_length=512)
    result = model(**inputs)
    print(result[0])
    print(result[1])


if __name__ == '__main__':
    less_length_bert()
