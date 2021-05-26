import json
import os
from nlp_platform.center.corpus import Corpus
from nlp_platform.plug_in.input.raw_from_text import raw_from_text
from nlp_platform.plug_in.input.instances_from_json import instances_from_json
from nlp_platform.plug_in.input.nodes_from_json import nodes_from_json


def from_files(file_dir):
    #
    corpus = Corpus()
    #
    raw_from_text(file_dir=file_dir, corpus=corpus)
    instances_from_json(file_dir=file_dir, corpus=corpus)
    nodes_from_json(file_dir=file_dir, corpus=corpus)
    #
    return corpus


def from_multiple_files(dir_path=str):
    folders_and_files_name = os.listdir(dir_path)  # 得到该文件夹下的最高层的文件夹名和文件名（str格式）
    config_file = dict()
    # config_file[dir_path[0: len(dir_path) - 1]] = None
    for folder_or_file_name in folders_and_files_name:
        folder_or_file_path = os.path.join(dir_path, folder_or_file_name) # 路径拼接成相对路径
        if os.path.isfile(folder_or_file_path):  # 如果是文件，就把该文件名设置成key 文件内容设置为value
            with open(folder_or_file_path, 'r') as f:
                config_file[folder_or_file_name] = f.read()
        elif os.path.isdir(folder_or_file_path):  # 如果是目录，就递归访问子目录。
            config_file[folder_or_file_name] = from_multiple_files(folder_or_file_path)
    return config_file