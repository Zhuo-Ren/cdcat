import json
import os
from nlp_platform.center.instancepool import InstancePool

def instances_from_json(file_dir, corpus=None):
    if corpus is None:
        raise Exception("corpus can not be None")
    with open(os.path.join(file_dir, f'xx.instances.json'), 'r', encoding='utf-8') as f:
        ip_info = json.load(f)
        corpus.ip = InstancePool(corpus=corpus, info=ip_info)
    return corpus