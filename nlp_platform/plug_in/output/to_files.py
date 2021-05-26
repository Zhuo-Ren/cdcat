from nlp_platform.plug_in.output.raw_to_text import raw_to_text
from nlp_platform.plug_in.output.instances_to_json import instances_to_json
from nlp_platform.plug_in.output.nodes_to_json import nodes_to_json
import os

def save(dir, corpus):
    """
    将数据（dict或str）转存为json格式
    :param data_dir: info文件存储目录
    :param data: 数据
    :param desc: 可选项："raw" "instances" "nodes"
    :return:
    """
    # param check: corpus
    from nlp_platform.center.corpus import Corpus
    if not isinstance(corpus, Corpus):
        raise TypeError

    raw_to_text(dir=dir, raw=corpus.raw)
    instances_to_json(dir=dir, ip=corpus.ip)
    nodes_to_json(dir=dir, np=corpus.np)






