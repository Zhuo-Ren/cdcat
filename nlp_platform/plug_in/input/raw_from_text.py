import json
import os

def raw_from_text(file_dir, corpus=None):
    if corpus is None:
        raise Exception("corpus can not be None")
    with open(os.path.join(file_dir, f'xx.raw.json'), 'r', encoding='utf-8') as f:
        corpus.raw = json.load(f)
    return corpus