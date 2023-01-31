# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Dict, List, Tuple, Union
from typing import TYPE_CHECKING
from copy import deepcopy
import _pickle as cPickle
import os
import re
from nlp_platform.plug_in.input.corpus_from_ecbpxml import info_from_ecbpxml, MentionData
if TYPE_CHECKING:
    from nlp_platform.center.corpus import Corpus


def info_to_corpus(token_tree: Dict, mention_list: List) -> Corpus:
    from nlp_platform.center.raw import Raw
    from nlp_platform.center.node import Node
    from nlp_platform.center.nodepool import NodePool
    from nlp_platform.center.instance import Instance
    from nlp_platform.center.instancepool import InstancePool
    from nlp_platform.center.corpus import Corpus

    # 生成corpus
    c = Corpus()

    # 生成raw
    raw = {}
    for topic_id in token_tree.keys():
        if topic_id not in raw:
            raw[topic_id] = {}
        for doc_id in token_tree[topic_id].keys():
            doc_id_raw_txt = doc_id  ### + ".raw.txt"
            if doc_id not in raw[topic_id]:
                raw[topic_id][doc_id_raw_txt] = ""
            doc_text = []
            for cur_sentence in token_tree[topic_id][doc_id].values():
                cur_sentence_tokens = [cur_token["token_text"] for cur_token in cur_sentence.values()]
                doc_text.append("".join(cur_sentence_tokens))
                del cur_sentence, cur_sentence_tokens
            raw[topic_id][doc_id_raw_txt] = "\n".join(doc_text)
            del doc_text
            del doc_id, doc_id_raw_txt
        del topic_id
    raw = Raw(raw)
    c.raw = raw

    # 对每个token，基于句级index，生成文档级index
    for topic_id in token_tree.keys():
        for doc_id in token_tree[topic_id].keys():
            last = 0
            for sentence_id, cur_sentence in token_tree[topic_id][doc_id].items():
                for cur_token_id, cur_token in cur_sentence.items():
                    start = last
                    last += cur_token["token_len"]
                    end = last
                    cur_token["doc_level_index"] = [start, end]
                    # check
                    """ 为了运行速度暂时封印
                    if cur_token["token_text"] != raw[topic_id][doc_id][start:end]:
                        raise RuntimeError
                    """
                    #
                    del cur_token
                    del cur_token_id
                last += 1  # 句末换行符
                del cur_sentence
            del sentence_id
            del last
        del doc_id
    del topic_id

    # 生成node（mention）
    node_list = []
    for cur_mention in mention_list:
        # mention的topic_id
        topic_id = re.match("^[0-9]*", cur_mention.doc_id).group()
        # mention的doc_id
        doc_id = cur_mention.doc_id
        # mention的sentence_index
        sentence_index = cur_mention.sent_id
        # mention的index_str
        token_id_list = cur_mention.tokens_number
        token_id_group = []
        i = 0
        while True:
            if i >= len(token_id_list):
                break
            # find start
            start = token_id_list[i]
            # find end
            while True:
                if i+1 >= len(token_id_list):
                    break
                elif (token_id_list[i]+1 != token_id_list[i+1]):
                    break
                i += 1
            end = token_id_list[i]
            token_id_group.append([start, end])
            i += 1
            del start, end
        del i
        token_index_str = []
        for cur_group in token_id_group:
            start = token_tree[topic_id][doc_id][sentence_index][cur_group[0]]['doc_level_index'][0]
            end = token_tree[topic_id][doc_id][sentence_index][cur_group[1]]['doc_level_index'][1]
            token_index_str.append(f"{start}-{end}")
            del start, end, cur_group
        token_index_str = "-".join(token_index_str)
        del token_id_group, token_id_list
        # node
        n_id = f"n:{topic_id}/{doc_id}:{token_index_str}"  ###  n_id = f"n:{topic_id}/{doc_id+'.raw.txt'}:{token_index_str}"
        cur_node = Node(info={"id": n_id})
        if raw[n_id] != cur_mention.tokens_str:
            print(f"离散指称：{raw[n_id]}")  # value error是因为n_id支持了离散指称，但是node.__getitem__()还不支持。
        c.np.add(cur_node)
        del topic_id, doc_id, sentence_index, cur_node, token_index_str
        # instance
        if cur_mention.coref_chain[:9] != "Singleton":
            cur_instance = Instance(info={"id": "i:"+cur_mention.coref_chain}, pool=c.ip)
            cur_instance["desc"]["value"] = cur_instance["id"]["value"]
            t = list(cur_instance["mentions"]["value"])  # Relation Label的value是ReportList类型，此类型不支持修改。所以这里先给搞成一般List。
            t.append(n_id)
            cur_instance["mentions"]["value"] = t
            del cur_instance
        del cur_mention, n_id
    return c


def add_zh_sentence(
        ecbp_token_tree: Dict,
        path: str,
        suffix: str = ".xml.EN-ZH.txt"
):
    for cur_topic_id, cur_topic in ecbp_token_tree.items():
        for cur_doc_id, cur_doc in cur_topic.items():
            cur_doc_path = os.path.join(path, cur_topic_id, cur_doc_id)
            cur_doc_path += suffix
            f = open(cur_doc_path, 'r', encoding='utf8')
            sentence_text_list = f.readlines()
            f.close()
            for cur_sentence_id, cur_sentence in cur_doc.items():
                if (
                        (
                            (cur_sentence_id % 2 == 1)
                            and
                            ("ecbplus" not in cur_doc_id)
                        )
                        or
                        (
                            (cur_sentence_id % 2 == 1)
                            and
                            ("ecbplus" in cur_doc_id)
                            and
                            (cur_sentence_id != 1)
                        )
                ):
                    zh_sentence = sentence_text_list[cur_sentence_id]
                    # zh_token_list = zh_sentence.split("|")
                    zh_token_list = re.findall("([^|]+|\|)\|", zh_sentence)
                    zh_token_list = [i for i in zh_token_list] ###
                    sentence_level_index = 0
                    for cur_zh_token_id in range(len(zh_token_list)):
                        cur_zh_token = zh_token_list[cur_zh_token_id]
                        cur_sentence[cur_zh_token_id] = {
                            "token_text": cur_zh_token,
                            "token_len": len(cur_zh_token),
                            "sentence_level_index": [
                                sentence_level_index,
                                sentence_level_index+len(cur_zh_token)
                            ]
                        }
                        sentence_level_index += len(cur_zh_token)


def add_zh_mention(path_to_corpus: str, token_tree: Dict, mention_list: List
):
    # 按照topic和doc把mention分类
    mention_dict = {}
    for cur_mention in mention_list:
        if cur_mention.doc_id not in mention_dict:
            mention_dict[cur_mention.doc_id] = {}
        if cur_mention.sent_id not in mention_dict[cur_mention.doc_id]:
            mention_dict[cur_mention.doc_id][cur_mention.sent_id] = []
        mention_dict[cur_mention.doc_id][cur_mention.sent_id].append(cur_mention)
        del cur_mention
    #
    for cur_topic_id, cur_topic in token_tree.items():
        # 遍历doc
        for cur_doc_id, cur_doc in cur_topic.items():
            # 对每个doc，读取mapping.pkl文件
            path_of_cur_doc = os.path.join(path_to_corpus, cur_topic_id, cur_doc_id)
            with open(path_of_cur_doc+".xml.mapping.pkl", mode="rb") as f:
                mapping_list = cPickle.load(f)
            cur_doc_mention = mention_dict[cur_doc_id]
            # 遍历sent
            for cur_sent_id, cur_sent_mention in cur_doc_mention.items():
                # 建立当前句中token的映射索引
                cur_sent_mapping = mapping_list[cur_sent_id//2]
                cur_sent_mapping_dict = {}
                for cur_mapping in cur_sent_mapping:
                    # id转换
                    cur_mapping["en_id_from_1_no_space"] = cur_mapping["en_id"]
                    """当前mention的英文token的id，从1开始，不计算空格"""
                    cur_mapping["en_id_from_0_with_space"] = (cur_mapping["en_id"] - 1)*2
                    """当前mention的英文token的id，从0开始，算上空格"""
                    cur_mapping["zh_id_from_1"] = cur_mapping["zh_id"]
                    """当前mention的中文token的id，从1开始"""
                    cur_mapping["zh_id_from_0"] = cur_mapping["zh_id"] - 1
                    """当前mention的中文token的id，从0开始"""
                    del cur_mapping["en_id"]
                    del cur_mapping["zh_id"]
                    # 通过str验证id转换是否正确
                    truth_str = "1"
                    calced_str = "1"
                    if truth_str == calced_str:
                        cur_sent_mapping_dict[cur_mapping["en_id_from_0_with_space"]] = cur_mapping
                    else:
                        raise RuntimeError
                # 遍历英文指称：对每个英文mention，找对应的中文mention
                for cur_en_mention in cur_sent_mention:
                    # 找到英文指称的token的id
                    en_token_id_list = cur_en_mention.tokens_number
                    """当前英文mention包含的所有英文token的id"""
                    # 找到中文指称的token的id和str(初始)
                    zh_token_id_list = []
                    zh_token_str_dict = {}
                    for cur_en_id in en_token_id_list:
                        if cur_en_id in cur_sent_mapping_dict:
                            zh_token_id_list.append(cur_sent_mapping_dict[cur_en_id]["zh_id_from_0"])
                            zh_token_str_dict[cur_sent_mapping_dict[cur_en_id]["zh_id_from_0"]] = cur_sent_mapping_dict[cur_en_id]["zh_str"]
                    zh_token_id_list = sorted(zh_token_id_list)
                    if zh_token_id_list == []:
                        continue
                    # 找到中文指称的token的id和str(中文离散指称的连续化)
                    flag_seq = True
                    for i in range(len(zh_token_id_list)-1):
                        # 判断是否离散
                        cur_id = zh_token_id_list[i]
                        next_id = zh_token_id_list[i+1]
                        if cur_id+1 != next_id:
                            # 如果离散指称属于"林赛*罗汉"中星号打断指称的类型。
                            middle_id = cur_id + 1
                            if cur_id+2 == next_id:
                                middle_str = token_tree[cur_topic_id][cur_doc_id][cur_en_mention.sent_id+1][cur_id+1]["token_text"]
                                if middle_str in r".-_/\· |":
                                    zh_token_id_list.append(middle_id)
                                    zh_token_str_dict[middle_id] = middle_str
                                else:
                                    flag_seq = False
                            else:
                                flag_seq = False
                        else:
                            flag_seq = False
                    zh_token_id_list = sorted(zh_token_id_list)
                    # 新建zh mention
                    mention_obj = MentionData(cur_en_mention.doc_id,
                                              cur_en_mention.sent_id+1,
                                              zh_token_id_list,
                                              "".join([zh_token_str_dict[i] for i in zh_token_id_list]),
                                              cur_en_mention.coref_chain,
                                              cur_en_mention.mention_type,
                                              is_continuous=flag_seq,
                                              is_singleton=cur_en_mention.is_singleton,
                                              score=float(-1))
                    mention_obj.is_person = cur_en_mention.is_person
                    mention_list.append(mention_obj)

                    # #
                    # zh_token_dict = {}
                    # """对应中文mention包含的所有中文token的id:str"""
                    # # 遍历当前句中的所有mapping，找到涉及当前en mention的mapping
                    # for cur_mapping in cur_sent_mapping:
                    #     # 验证cur_mapping是否涉及当前en mention
                    #     if cur_mapping["en_id"]-1 not in en_token_id_list:
                    #         continue
                    #     # 检验zh str是否正确
                    #     if "ecbplus" in cur_doc_id and cur_sent_id==0:
                    #         pass
                    #     elif token_tree[cur_topic_id][cur_doc_id][cur_sent_id+1][cur_mapping["zh_id"]-1]["token_text"] != cur_mapping["zh_str"]:
                    #         i = 0
                    #         while i <= cur_mapping["zh_id"]-1:
                    #             if (token_tree[cur_topic_id][cur_doc_id][cur_sent_id+1][i]["token_text"] == " ") or (token_tree[cur_topic_id][cur_doc_id][cur_sent_id+1][i]["token_text"] =="|"):
                    #                 cur_mapping["zh_id"] += 1
                    #             i += 1
                    #         del i
                    #         if token_tree[cur_topic_id][cur_doc_id][cur_sent_id + 1][
                    #             cur_mapping["zh_id"] - 1]["token_text"] != cur_mapping[
                    #             "zh_str"]:
                    #             raise RuntimeError
                    #     # 记录涉及当前en mention的mapping
                    #     zh_token_dict[cur_mapping["zh_id"]-1] = cur_mapping["zh_str"]


def ecbp_to_en2zh(
        token_tree: Dict,
        mention_list: List,
        path_to_corpus: str,
        suffix_of_en2zh_file: str
) -> List[Dict, List]:
    """
    把ecb+的info改成双语的info
    :return:
    """
    # 创建中文空句子
    for cur_topic_id, cur_topic in token_tree.items():
        for cur_doc_id, cur_doc in cur_topic.items():
            cur_doc_new = {}
            for cur_sentence_id, cur_sentence in cur_doc.items():
                cur_doc_new[cur_sentence_id*2] = cur_sentence  # 创建英文句
                cur_doc_new[cur_sentence_id*2+1] = {}  # 创建中文句
                del cur_sentence_id, cur_sentence
            cur_topic[cur_doc_id] = cur_doc_new
            del cur_doc, cur_doc_id, cur_doc_new
        del cur_topic
    # 添加中文句子内容
    add_zh_sentence(
        ecbp_token_tree=token_tree, path=path_to_corpus,
        suffix=suffix_of_en2zh_file
    )
    # 修改英文mention
    for cur_mention in mention_list:
        cur_mention.sent_id *= 2
    # 添加中文mention
    add_zh_mention(
        path_to_corpus=path_to_corpus,
        token_tree=token_tree, mention_list=mention_list)

    return [token_tree, mention_list]


def add_space_token(token_tree, mention_list):
    """
    给英文token_tree中添加空格token，因此对应mention的tokens_number也乘2。

    :param token_tree:
    :param mention_list:
    :return: 没有返回值。token_tree被修改了。
    """
    for cur_topic_id, cur_topic in token_tree.items():
        for cur_doc_id, cur_doc in cur_topic.items():
            for cur_sent_id, cur_sent in cur_doc.items():
                cur_sent_new = {}
                for i in range(len(cur_sent)*2-1):
                    if i % 2 == 0:
                        cur_sent_new[i] = cur_sent[i//2]
                    elif i % 2 == 1:
                        cur_sent_new[i] = {}
                        cur_sent_new[i]["token_text"] = " "
                        cur_sent_new[i]["token_len"] = 1
                        cur_sent_new[i]["sentence_level_index"] = [
                            cur_sent[(i-1)//2]["sentence_level_index"][1],
                            cur_sent[(i+1)//2]["sentence_level_index"][0],
                        ]
                        # check
                        if cur_sent[(i-1)//2]["sentence_level_index"][1] + 1 != cur_sent[(i + 1) // 2]["sentence_level_index"][0]:
                            raise RuntimeError
                        del i
                cur_doc[cur_sent_id] = cur_sent_new
                del cur_sent_id, cur_sent, cur_sent_new
            del cur_doc_id, cur_doc
        del cur_topic_id, cur_topic
    for cur_mention in mention_list:
        t = []
        for i in range(len(cur_mention.tokens_number)):
            """
            例如输入的tokens_number = [1,5,6,12,13],则输出的tokens_number = [2,10,11,12,24,25,26]
            """
            # 当前token的id乘2（因为加了空格）
            t.append(2*cur_mention.tokens_number[i])
            # 如果多个token是连续的，额外再补充空格对应的token id
            if i+1 < len(cur_mention.tokens_number):
                if cur_mention.tokens_number[i] + 1 == cur_mention.tokens_number[i+1]:  # 如果连续
                    t.append(2*cur_mention.tokens_number[i]+1)  # 补充空格对应的token id
        cur_mention.tokens_number = t



def correct_sent_id_in_ecbplus(mention_list):
    """
    ecbplus中的sent_id没有算上最初的网址行，这里修正一下.

    :param mention_list:
    :return: 没有返回值，mention_list被修改了。
    """
    for cur_mention in mention_list:
        if "ecbplus" in cur_mention.doc_id:
            cur_mention.sent_id += 1


def corpus_from_ecbp_en2zh(
        ecbp_en2zh_path: str = r"data\raw\ECBplus",
        csv_path: str = r"data\raw\ECBplus_coreference_sentences.csv",
        mapping_pkl_path: str = r"data\raw\ECBplus\mapping.pkl",
        suffix_of_en2zh_file: str = r".xml.EN-ZH.txt"
) -> Corpus:
    """
    读取ecb+语料库，生成Corpus对象。

    ecb+语料库中涉及离散指称。
    例如“turn it off”中的“turn off”被标注为一个mention。
    但是Corpus对象暂时还不支持（主要是Raw.__getitem__不支持）。
    所以在把ecb+语料存到Corpus对象时，进行了简化。
    即对离散指称，只保留其第一个连续部分，即“turn”。

    本方法涉及后缀转换，例如ecb+中的1_ecb.xml对应1_ecb.raw.txt。

    :param ecbp_en2zh_path: ecb+语料根文件夹路径。
    :param csv_path: ecb+语料中ECBplus_coreference_sentences.csv文件的路径。
    :return: 基于ecb+语料库构建的Corpus obj。
    """
    # ecb+
    [token_tree, mention_list] = info_from_ecbpxml(
        ecbp_path=ecbp_en2zh_path, csv_path=csv_path
    )
    correct_sent_id_in_ecbplus(mention_list)
    add_space_token(token_tree, mention_list)
    # en2zh
    [token_tree, mention_list] = ecbp_to_en2zh(
        token_tree=token_tree,
        mention_list=mention_list,
        path_to_corpus=ecbp_en2zh_path,
        suffix_of_en2zh_file=suffix_of_en2zh_file
    )
    # corpus
    c = info_to_corpus(token_tree, mention_list)
    #
    return c




