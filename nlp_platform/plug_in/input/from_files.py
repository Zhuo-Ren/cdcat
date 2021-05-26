from nlp_platform.center.corpus import Corpus
from nlp_platform.plug_in.input.raw_from_text import raw_from_text
from nlp_platform.plug_in.input.instances_from_json import instances_from_json
from nlp_platform.plug_in.input.nodes_from_json import nodes_from_json


def from_files(file_dir):
    # param check: file_dir
    if not isinstance(file_dir, str):
        raise TypeError
    #
    corpus = Corpus()
    #
    raw_from_text(file_dir=file_dir, corpus=corpus)
    instances_from_json(file_dir=file_dir, corpus=corpus)
    nodes_from_json(file_dir=file_dir, corpus=corpus)
    #
    return corpus
