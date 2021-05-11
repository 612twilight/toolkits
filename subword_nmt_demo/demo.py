# -*- coding:utf-8 -*-
"""
-------------------------------------------------
Project Name: toolkits
File Name: demo.py
Author: gaoyw
Create Date: 2021/5/11
-------------------------------------------------
"""

import codecs
import re

import jieba
import nltk
from subword_nmt import learn_bpe, apply_bpe, get_vocab
from tqdm import tqdm


def learn_bpe_function(raw_train_file, bpe_codes_file):
    parser = learn_bpe.create_parser()
    args = parser.parse_args([
        "--input", raw_train_file,
        "--output", bpe_codes_file
    ])
    args.output = codecs.open(args.output.name, 'w', encoding='utf-8')
    args.input = codecs.open(args.input.name, encoding='utf-8')
    learn_bpe.learn_bpe(args.input, args.output, args.symbols, args.min_frequency, args.verbose,
                        is_dict=args.dict_input,
                        total_symbols=args.total_symbols)


def apply_bpe_function(codes_file, train_file, apply_out, vocabulary=None):
    parser = apply_bpe.create_parser()
    args = parser.parse_args([
        "--codes", codes_file,
        "--input", train_file,
        "--output", apply_out,
        # "--vocabulary", vocabulary
    ])

    if vocabulary:
        args.vocabulary = codecs.open(vocabulary, encoding='utf-8')

    if vocabulary:
        vocabulary = apply_bpe.read_vocabulary(args.vocabulary, args.vocabulary_threshold)
    else:
        vocabulary = None

    args.codes = codecs.open(args.codes.name, encoding='utf-8')
    bpe = apply_bpe.BPE(args.codes, args.merges, args.separator, vocabulary, args.glossaries)
    args.input = codecs.open(args.input.name, encoding='utf-8')
    args.output = codecs.open(args.output.name, 'w', encoding='utf-8')
    for line in args.input:
        args.output.write(bpe.process_line(line, args.dropout))


def get_vocab_function(codes_train_file, vocab_file):
    parser = get_vocab.create_parser()
    args = parser.parse_args([
        "--input", codes_train_file,
        "--output", vocab_file
    ])
    args.input = codecs.open(args.input.name, encoding='utf-8')
    args.output = codecs.open(args.output.name, 'w', encoding='utf-8')
    get_vocab.get_vocab(args.input, args.output)


def subword_all():
    source_raw_train_file = "train.en"  # 分词过得结果
    source_bpe_codes_file = "train.en.codes"  # 输出的中间结果
    learn_bpe_function(source_raw_train_file, source_bpe_codes_file)
    apply_source_train_file = "train.en.bpe"
    apply_bpe_function(source_bpe_codes_file, source_raw_train_file, apply_source_train_file)
    source_vocab_file = "train.en.vocab"
    get_vocab_function(apply_source_train_file, source_vocab_file)
    source_raw_valid_file = "valid.en"
    apply_source_valid_file = "valid.en.bpe"
    apply_bpe_function(source_bpe_codes_file, source_raw_valid_file, apply_source_valid_file, source_vocab_file)
    source_raw_test_file = "test.en"
    apply_source_test_file = "test.en.bpe"
    apply_bpe_function(source_bpe_codes_file, source_raw_test_file, apply_source_test_file, source_vocab_file)

    target_raw_train_file = "train.zh"
    target_bpe_codes_file = "train.zh.codes"
    learn_bpe_function(target_raw_train_file, target_bpe_codes_file)
    apply_target_train_file = "train.zh.bpe"
    apply_bpe_function(target_bpe_codes_file, target_raw_train_file, apply_target_train_file)
    target_vocab_file = "train.zh.vocab"
    get_vocab_function(apply_target_train_file, target_vocab_file)
    target_raw_valid_file = "valid.zh"
    apply_target_valid_file = "valid.zh.bpe"
    apply_bpe_function(target_bpe_codes_file, target_raw_valid_file, apply_target_valid_file, target_vocab_file)
    target_raw_test_file = "test.zh"
    apply_target_test_file = "test.zh.bpe"
    apply_bpe_function(target_bpe_codes_file, target_raw_test_file, apply_target_test_file, target_vocab_file)


def seg_process():
    with open("News_Commentary_v15/corpus.zh", 'r', encoding='utf8') as reader:
        zh_lines = reader.readlines()
    with open("News_Commentary_v15/corpus.en", 'r', encoding='utf8') as reader:
        en_lines = reader.readlines()
    import os
    os.makedirs("clean_dir", exist_ok=True)
    seg_zh_writer = open("clean_dir/corpus.zh", "w", encoding='utf8')
    seg_en_writer = open("clean_dir/corpus.en", "w", encoding='utf8')
    control_chars = ''.join(map(chr, list(range(0, 32)) + list(range(127, 160))))
    control_char_re = re.compile('[%s]' % re.escape(control_chars))

    def remove_control_chars(s):
        return control_char_re.sub('', s)

    def replace_nonbreaking_whitespace(s):
        return s.replace("\xa0", " ").strip()

    for zh_line, en_line in tqdm(zip(zh_lines, en_lines), total=len(zh_lines)):
        en_line = remove_control_chars(en_line)
        zh_line = remove_control_chars(zh_line)
        en_line = replace_nonbreaking_whitespace(en_line)
        zh_line = replace_nonbreaking_whitespace(zh_line)
        zh_seg = filter(lambda x: x and x != ' ', jieba.lcut(zh_line))
        en_seg = filter(lambda x: x and x != ' ', nltk.word_tokenize(en_line))
        seg_zh_writer.write(" ".join(zh_seg) + "\n")
        seg_en_writer.write(" ".join(en_seg) + "\n")


def subword_one():
    source_raw_train_file = "clean_dir/corpus.en"  # 分词过得结果
    source_bpe_codes_file = "clean_dir/corpus.en.codes"  # 输出的中间结果
    learn_bpe_function(source_raw_train_file, source_bpe_codes_file)
    apply_source_train_file = "clean_dir/corpus.en.codes.bpe"
    apply_bpe_function(source_bpe_codes_file, source_raw_train_file, apply_source_train_file)
    source_vocab_file = "clean_dir/corpus.en.vocab"
    get_vocab_function(apply_source_train_file, source_vocab_file)

    # target_raw_train_file = ""
    # target_bpe_codes_file = ""
    # learn_bpe_function(target_raw_train_file, target_bpe_codes_file)
    # apply_target_train_file = ""
    # apply_bpe_function(target_bpe_codes_file, target_raw_train_file, apply_target_train_file)
    # target_vocab_file = ""
    # get_vocab_function(target_bpe_codes_file, target_vocab_file)


if __name__ == '__main__':
    # seg_process()
    subword_one()
