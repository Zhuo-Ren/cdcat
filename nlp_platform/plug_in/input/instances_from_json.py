import json
import os
from nlp_platform.center.instancepool import InstancePool

def instances_from_json(file_dir, corpus):
    # param check: corpus
    from nlp_platform.center.corpus import Corpus
    if not isinstance(corpus, Corpus):
        raise TypeError
    #
    with open(os.path.join(file_dir, f'instances.json'), 'r', encoding='utf-8') as f:
        ip_info = json.load(f)
        corpus.ip = InstancePool(corpus=corpus, info=ip_info)