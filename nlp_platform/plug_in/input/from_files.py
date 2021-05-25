import json
import os
from nlp_platform.center.corpus import Corpus
from nlp_platform.center.instance import Instance
from nlp_platform.center.node import Node
from nlp_platform.center.instancepool import InstancePool
from nlp_platform.center.nodepool import NodePool


def file_to_corpus(file_dir, corpus=None, desc=None):
    if corpus is None:
        corpus = Corpus()
    with open(os.path.join(file_dir, f'xx.{desc}.json'), 'r', encoding='utf-8') as f:
        if desc == "raw":
            corpus.raw = json.load(f)
        elif desc == "instances":
            ip_info = json.load(f)
            corpus.ip = InstancePool(corpus=corpus, info=ip_info)
        elif desc == "nodes":
            np_info = json.load(f)
            corpus.np = NodePool(corpus=corpus, info=np_info)
    return corpus

def create_relation_by_file(file_dir, corpus, desc=None):

    # param check: corpus
    if corpus is None:
        raise Exception("corpus shouldn't be None")
    else:
        if not isinstance(corpus, object):
            raise TypeError("corpus must be a object")

    with open(os.path.join(file_dir, f'xx.{desc}.json'), 'r', encoding='utf-8') as f:
        if desc == "instances":
            ip_info = json.load(f)
            for key in ip_info.keys():
                if key in corpus.ip.keys():
                    if len(ip_info[key]["mentions"]) > 1:
                        for value in ip_info[key]["mentions"]:
                            corpus.ip[key]["mentions"]["value"] = value
                    else:
                        corpus.ip[key]["mentions"]["value"] = ip_info[key]["mentions"][0]

        elif desc == "nodes":
            np_info = json.load(f)
            for key in np_info.keys():
                if key in corpus.np.keys():
                    if len(np_info[key]["refer"]) > 1:
                        for value in np_info[key]["refer"]:
                            corpus.ip[key]["refer"]["value"] = value
                    else:
                        corpus.np[key]["refer"]["value"] = np_info[key]["refer"][0]
            print(1)

    return corpus