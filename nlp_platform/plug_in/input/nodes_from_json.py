import json
import os
from nlp_platform.center.nodepool import NodePool

def nodes_from_json(file_dir, corpus=None):
    if corpus is None:
        raise Exception("corpus can not be None")
    with open(os.path.join(file_dir, f'xx.nodes.json'), 'r', encoding='utf-8') as f:
        np_info = json.load(f)
        corpus.np = NodePool(corpus=corpus, info=np_info)
    return corpus