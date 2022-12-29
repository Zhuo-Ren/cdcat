from nlp_platform.center.corpus import Corpus
from nlp_platform.plug_in.input.raw_from_text import raw_from_text
from nlp_platform.plug_in.input.instances_from_json import instances_from_json
from nlp_platform.plug_in.input.nodes_from_json import nodes_from_json


def corpus_from_json(dir: str):
    # param check: file_dir
    if not isinstance(dir, str):
        raise TypeError
    #
    corpus = Corpus()
    #
    raw_from_text(dir=dir, corpus=corpus)
    instances_from_json(dir=dir, corpus=corpus)
    nodes_from_json(dir=dir, corpus=corpus)
    #
    return corpus
