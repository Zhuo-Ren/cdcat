from nlp_platform.plug_in.output.raw_to_text import raw_to_text
from nlp_platform.plug_in.output.instances_to_json import instances_to_json
from nlp_platform.plug_in.output.nodes_to_json import nodes_to_json


def save(dir, corpus=None):
    """
    将数据（dict或str）转存为json格式
    :param data_dir: info文件存储目录
    :param data: 数据
    :param desc: 可选项："raw" "instances" "nodes"
    :return:
    """
    if corpus is None:
        raise Exception("corpus can not be None")
    raw_to_text(dir=dir, corpus=corpus)
    instances_to_json(dir=dir, corpus=corpus)
    nodes_to_json(dir=dir, corpus=corpus)
