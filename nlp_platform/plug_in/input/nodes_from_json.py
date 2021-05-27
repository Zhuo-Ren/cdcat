import json
import os
import re

def nodes_from_json(file_dir: str, corpus):
    # param check: file_dir
    if not isinstance(file_dir, str):
        raise TypeError
    # param check: corpus
    from nlp_platform.center.corpus import Corpus
    if not isinstance(corpus, Corpus):
        raise TypeError
    #
    from_multiple_files(file_dir=file_dir, corpus=corpus, raw=corpus.raw)


def from_multiple_files(file_dir: str, corpus, raw):
    from nlp_platform.center.node import Node
    for key, value in raw.items():
        if re.search("raw.txt", key, flags=0): # 成功定位到需要读取的xx.nodes.json
            try:
                with open(os.path.join(file_dir, f'{key[:-8]}.nodes.json'), 'r', encoding='utf-8') as f:
                    nodes_info = json.load(f)
                    for node_info in nodes_info.values():
                        node = Node(info=node_info)
                        corpus.np.add(node)
            except IOError:
                pass
        elif os.path.isdir(os.path.join(file_dir, key)): # 碰到的是一个文件夹
            from_multiple_files(os.path.join(file_dir, key), corpus=corpus, raw=raw[key])