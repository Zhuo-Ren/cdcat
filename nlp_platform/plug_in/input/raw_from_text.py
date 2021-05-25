import json
import os

def raw_from_text(file_dir, corpus):
    # param check: corpus
    from nlp_platform.center.corpus import Corpus
    if not isinstance(corpus, Corpus):
        raise TypeError
    #
    with open(os.path.join(file_dir, f'xx.raw.json'), 'r', encoding='utf-8') as f:
        corpus.raw = json.load(f)
