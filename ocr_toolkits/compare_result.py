# -*- coding:utf-8 -*-
"""
-------------------------------------------------
Project Name: toolkits
File Name: compare_result.py
Author: gaoyw
Create Date: 2020/12/30
-------------------------------------------------
"""


def compare_result_stags_3():
    old_result = "C:/Users/FH/Desktop/ocrtupianjieya/icpr_mtwi_task1/sample_result.txt"
    new_result_rec = "C:/Users/FH/Desktop/ocrtupianjieya/icpr_mtwi_task1/result2.txt"
    new_result_not_rec = "C:/Users/FH/Desktop/ocrtupianjieya/icpr_mtwi_task1/no_rec_result2.txt"
    with open(old_result, 'r', encoding='utf8') as reader:
        old_result_dict = dict(
            [(line.strip().split(" ")[0], line.strip().split(" ")[1] if len(line.strip().split(" ")) == 2 else "") for
             line in reader.readlines()])
    with open(new_result_rec, 'r', encoding='utf8') as reader:
        new_result_dict = dict(
            [(line.strip().split(" ")[0], line.strip().split(" ")[1]) for line in reader.readlines()])
    with open(new_result_not_rec, 'r', encoding='utf8') as reader:
        for line in reader.readlines():
            new_result_dict[line.strip().split(" ")[0]] = ""
    print(list(old_result_dict.items())[:10])
    print()
    print(list(new_result_dict.items())[:10])
    with open("confirm.txt", 'w', encoding='utf8') as writer, open("not_recog.txt", 'w', encoding='utf8') as writer2:
        for file_name in old_result_dict:
            if file_name in new_result_dict:
                if new_result_dict[file_name] and old_result_dict[file_name]:
                    tmp = new_result_dict[file_name] if len(new_result_dict[file_name]) > len(
                        old_result_dict[file_name]) else old_result_dict[file_name]
                    writer.write(file_name + " " + tmp + "\n")
                elif new_result_dict[file_name]:
                    writer.write(file_name + " " + new_result_dict[file_name] + "\n")
                elif old_result_dict[file_name]:
                    writer.write(file_name + " " + old_result_dict[file_name] + "\n")
                else:
                    writer2.write(file_name + "\n")


if __name__ == '__main__':
    compare_result_stags_3()
