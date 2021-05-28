import json
import os
from nlp_platform.center.instancepool import InstancePool
from nlp_platform.center.instance import Instance
import re

def instances_from_json(dir: str, corpus):
    # param check: corpus
    from nlp_platform.center.corpus import Corpus
    if not isinstance(corpus, Corpus):
        raise TypeError
    #
    from_multiple_files(dir=dir, corpus=corpus)



def from_multiple_files(dir: str, corpus):
    # param check: file_dir
    if not isinstance(dir, str):
        raise TypeError
    # param check: corpus
    from nlp_platform.center.corpus import Corpus
    if not isinstance(corpus, Corpus):
        raise TypeError

    folders_and_files_name = os.listdir(dir)  # 得到该文件夹下的最高层的文件夹名和文件名（str格式）
    for folder_or_file_name in folders_and_files_name:
        folder_or_file_path = os.path.join(dir, folder_or_file_name)  # 路径拼接成相对路径
        if os.path.isfile(folder_or_file_path):
            if re.search("instances.json", folder_or_file_name, flags=0):
                with open(folder_or_file_path, 'r', encoding='utf8') as f:
                    instances_info = json.load(f)
                    for instance_info in instances_info.values():
                        Instance(info=instance_info, pool=corpus.ip)
        elif os.path.isdir(folder_or_file_path):
            from_multiple_files(dir=folder_or_file_path, corpus=corpus)

