# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Dict, List, Tuple, Union
from typing import TYPE_CHECKING
from copy import deepcopy
import os
import re
from nlp_platform.plug_in.input.corpus_from_ecbpxml import info_from_ecbpxml
if TYPE_CHECKING:
    from nlp_platform.center.corpus import Corpus


def info_to_corpus(token_tree: Dict, mention_list: List) -> Corpus:
    from nlp_platform.center.raw import Raw
    from nlp_platform.center.node import Node
    from nlp_platform.center.nodepool import NodePool
    from nlp_platform.center.instance import Instance
    from nlp_platform.center.instancepool import InstancePool
    from nlp_platform.center.corpus import Corpus
    # 对每个token，基于句级index，生成文档级index
    for topic_id in token_tree.keys():
        for doc_id in token_tree[topic_id].keys():
            last = -1
            for sentence_id in token_tree[topic_id][doc_id].keys():
                cur_sentence = token_tree[topic_id][doc_id][sentence_id]
                for t_id in cur_sentence.keys():
                    cur_token = cur_sentence[t_id]
                    cur_token["doc_level_index"] = [
                        last+1,  # 第一个1是空格，第二个1是开头
                        last+1+cur_token["token_len"]
                    ]
                    last = last+1+cur_token["token_len"]
                    del cur_token
                    del t_id
                del cur_sentence
            del sentence_id
            del last
        del doc_id
    del topic_id
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
            for sentence_id in token_tree[topic_id][doc_id].keys():
                cur_sentence = token_tree[topic_id][doc_id][sentence_id]
                cur_sentence_tokens = []
                for t_id in cur_sentence.keys():
                    cur_token = cur_sentence[t_id]
                    cur_sentence_tokens.append(cur_token["token_text"])
                    del cur_token
                    del t_id
                doc_text.append(" ".join(cur_sentence_tokens))
                del cur_sentence, cur_sentence_tokens
                del sentence_id
            raw[topic_id][doc_id_raw_txt] = "\n".join(doc_text)
            del doc_text
            del doc_id, doc_id_raw_txt
        del topic_id
    raw = Raw(raw)
    c.raw = raw
    # 生成node（mention）
    node_list = []
    for cur_mention in mention_list:
        # mention的topic_id
        topic_id = re.match("^[0-9]*", cur_mention.doc_id).group()
        # mention的doc_id
        doc_id = cur_mention.doc_id
        # mention的sentence_index
        if doc_id[-4:] == "plus":
            sentence_index = cur_mention.sent_id + 2
        else:
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
            del start, end
        token_index_str = ";".join(token_index_str)
        del token_id_group, token_id_list, cur_group
        if ";" in token_index_str:  # 简化离散指称（就是对3-5;7-8仅保留第一个组3-5）
            token_index_str = re.match("^[^;]*(?=;)", token_index_str).group()
        # node
        n_id = f"n:{topic_id}/{doc_id}:{token_index_str}"  ###  n_id = f"n:{topic_id}/{doc_id+'.raw.txt'}:{token_index_str}"
        cur_node = Node(info={"id": n_id})
        if raw[n_id] != cur_mention.tokens_str:
            pass  # value error是因为n_id支持了离散指称，但是node.__get_item__()还不支持。
        c.np.add(cur_node)
        del topic_id, doc_id, sentence_index, cur_node, token_index_str
        # instance
        if cur_mention.coref_chain[:9] != "Singleton":
            cur_instance = Instance(info={"id": "i:"+cur_mention.coref_chain}, pool=c.ip)
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
                    zh_token_list = zh_sentence.split("|")
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
    for cur_topic_id, cur_topic in token_tree.items():
        for cur_doc_id, cur_doc in cur_topic.items():
            cur_doc_new = {}
            file_path = os.path.join(path_to_corpus, cur_topic_id, cur_doc_id)
            for cur_sentence_id, cur_sentence in cur_doc.items():
                cur_doc_new[cur_sentence_id*2] = cur_sentence  # 创建英文句
                cur_doc_new[cur_sentence_id*2+1] = {}  # 创建中文句
                del cur_sentence_id, cur_sentence
            cur_topic[cur_doc_id] = cur_doc_new
            del cur_doc, cur_doc_id, cur_doc_new
        del cur_topic
    #
    add_zh_sentence(
        ecbp_token_tree=token_tree, path=path_to_corpus,
        suffix=suffix_of_en2zh_file
    )
    #
    for cur_mention in mention_list:
        cur_mention.sent_id *= 2
    #
    return [token_tree, mention_list]


def corpus_from_ecbp_en2zh(
        ecbp_en2zh_path: str = r"data\raw\ECBplus",
        csv_path: str = r"data\raw\ECBplus_coreference_sentences.csv",
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
    # info
    [token_tree, mention_list] = info_from_ecbpxml(
        ecbp_path=ecbp_en2zh_path, csv_path=csv_path
    )
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




