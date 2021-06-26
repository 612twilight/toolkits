# -*- coding:utf-8 -*-
"""
-------------------------------------------------
Project Name: toolkits
File Name: utils.py
Author: gaoyw
Create Date: 2021/6/26
Description: 
-------------------------------------------------
"""


def parser_conll(conll_path):
    """
    解析conll文件，将其转变成实体
    :param conll_path:
    :return:
    """
    samples = []
    with open(conll_path, 'r', encoding="utf8") as reader:
        words = []
        tags = []
        entity_sents = []
        entities = []
        entity_sent = ""
        entity = "O"
        index = 0
        lines = reader.readlines()
        for line in lines:
            index += 1
            if line.strip():
                word, tag = line.strip().split(" ")
                if tag[:2] == "B-":
                    if entity_sent:
                        entity_sents.append(entity_sent)
                        entities.append(entity)
                        entity_sent = ""
                        entity = "O"
                    entity_sent += word
                    entity = "O" if tag == "O" else tag[2:]
                else:
                    entity_sent += word
                    entity = "O" if tag == "O" else tag[2:]
                words.append(word)
                tags.append(tag)
            else:
                if entity_sent:
                    entity_sents.append(entity_sent)
                    entities.append(entity)
                    entity_sent = ""
                    entity = "O"
                samples.append(
                    {"id": index, "words": words, "tags": tags, "entity_sents": entity_sents, "entities": entities})
                words = []
                tags = []
                entity_sents = []
                entities = []

        if words:
            if entity_sent:
                entity_sents.append(entity_sent)
                entities.append(entity)
            samples.append(
                {"id": index, "words": words, "tags": tags, "entity_sents": entity_sents, "entities": entities})
    return samples


def parse_conll_infos(conll_infos):
    """
    example:
    conll_info [(words,tags),]
    words = ['观', '沙', '岭', '阳', '光', '丽', '城', '小', '区', '00', '栋']
    tags = ['B-town', 'I-town', 'I-town', 'B-poi', 'I-poi', 'I-poi', 'I-poi', 'I-poi', 'I-poi', 'B-houseno',
            'I-houseno', 'I-houseno']
    """
    entity_sents = []
    entities = []
    entity_sent = ""
    entity = "O"
    parsed_infos = []
    for words, tags in conll_infos:
        for word, tag in zip(words, tags):
            if tag[:2] == "B-":
                if entity_sent:
                    entity_sents.append(entity_sent)
                    entities.append(entity)
                    entity_sent = ""
                entity_sent += word
                entity = "O" if tag == "O" else tag[2:]
            else:
                entity_sent += word
                entity = "O" if tag == "O" else tag[2:]
        if entity_sent:
            entity_sents.append(entity_sent)
            entities.append(entity)
        parsed_infos.append((entity_sents, entities))
    return parsed_infos


def convert_parsed_info2bieo(parsed_infos):
    """

    :params parsed_infos  like [(['观沙岭', '阳光丽城小区', '00栋'], ['town', 'poi', 'houseno'])]
    """
    bieo_infos = []
    for entity_sents, entities in parsed_infos:
        words = []
        tags = []
        for entity_index, entity_sent in enumerate(entity_sents):
            last_index = len(entity_sent) - 1
            for index, word in enumerate(entity_sent):
                words.append(word)
                tag = entities[entity_index]
                if tag == "O":
                    tags.append("O")
                    continue
                if index == 0:
                    tags.append("B-" + entities[entity_index])
                elif index == last_index:
                    tags.append("E-" + entities[entity_index])
                else:
                    tags.append("I-" + entities[entity_index])
        bieo_infos.append((words, tags))
    return bieo_infos


def test_parse_conll_info():
    words = ['观', '沙', '岭', '阳', '光', '丽', '城', '小', '区', '00', '栋']
    tags = ['B-town', 'I-town', 'I-town', 'B-poi', 'I-poi', 'I-poi', 'I-poi', 'I-poi', 'I-poi', 'B-houseno',
            'I-houseno', 'I-houseno']
    result = parse_conll_infos([(words, tags)])
    print(result)
    result = convert_parsed_info2bieo(result)
    print(result)


def task_transposebieo2bieo():
    from tqdm import tqdm
    file_path = "C:/Users\FH\Downloads/随时准备合并_addr_parsing_runid_bert_2021626729.txt"
    with open(file_path, "r", encoding='utf8') as reader:
        lines = reader.readlines()
    writer = open("C:/Users\FH\Downloads/随时准备合并_addr_parsing_runid.txt", "w",
                  encoding="utf8")
    for line in tqdm(lines):
        idx, words, tags = line.strip().split("\u0001")
        words = [word for word in words]
        tags = tags.split(" ")
        conll_infos = [(words, tags)]
        parsed_infos = parse_conll_infos(conll_infos)
        bieo_infos = convert_parsed_info2bieo(parsed_infos)
        bieo_tags = bieo_infos[0][1]
        line = idx + "\u0001" + "".join(words) + "\u0001" + " ".join(bieo_tags) + "\n"
        writer.write(line)


if __name__ == '__main__':
    task_transposebieo2bieo()
