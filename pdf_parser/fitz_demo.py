# -*- coding:utf-8 -*-
"""
-------------------------------------------------
Project Name: toolkits
File Name: fitz_demo.py
Author: gaoyw
Create Date: 2021/6/17
Description:
PyMuPDF                1.18.14
-------------------------------------------------
"""
import fitz


def read_pdf():
    type_read = "raw_dict"
    pdf_path = "pdf_parser/中华行两全保险.pdf"
    doc = fitz.open(pdf_path)
    nums = doc.page_count
    for i in range(nums):
        page = doc[i]
        if type_read == "dict":
            dict_word = page.get_textpage().extractDICT()
            """
            解析出
            width
            height
            blocks
            其中blocks里面的每个元素是左->右,上->下,最基础元素依然是一句话,一个span
            """
            for key in dict_word:
                value = dict_word[key]
                # print(value)
                if isinstance(value, list):
                    for block in dict_word[key]:
                        print("=================big block=============")
                        lines = block["lines"]
                        for line in lines:
                            print("=================line=============")
                            for span in line["spans"]:
                                print(span)
                                print("<<{}>>".format(span["text"]))
        if type_read == "words":
            words = page.get_textpage().extractWORDS()  # 最基础元素是一句话，左->右,上->下，类似上面
            print(words)
            for word in words:
                print(word)
        if type_read == "raw_dict":
            raw_dict = page.get_textpage().extractRAWDICT()  # 获取每一个字符以及他的位置
            for word_block in raw_dict["blocks"]:
                print(word_block)
                lines = word_block["lines"]
                for line in lines:
                    spans = line["spans"]
                    for span in spans:
                        font = span["font"]
                        size = span["size"]
                        chars = span["chars"]
                        for char in chars:
                            print("bbox:{}\tword:{}\tfont:{}\tsize:{}".format(char["bbox"], char["c"], font, size))


if __name__ == '__main__':
    read_pdf()
