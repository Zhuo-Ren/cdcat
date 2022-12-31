from nlp_platform.center.corpus import Corpus
from nlp_platform.plug_in.input.raw_from_pure_text import raw_from_pure_text
from nlp_platform.plug_in.input.instances_from_json import instances_from_json
from nlp_platform.plug_in.input.nodes_from_json import nodes_from_json


def corpus_from_json(path: str):
    # param check: file_dir
    if not isinstance(path, str):
        raise TypeError
    #
    corpus = Corpus()
    #
    corpus.raw = raw_from_pure_text(path=path)
    instances_from_json(dir=path, corpus=corpus)
    nodes_from_json(dir=path, corpus=corpus)
    #
    return corpus
