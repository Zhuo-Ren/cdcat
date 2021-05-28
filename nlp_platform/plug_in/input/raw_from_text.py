import os
import re
from nlp_platform.center.raw import Raw


def raw_from_text(dir: str, corpus):
    # param check: corpus
    from nlp_platform.center.corpus import Corpus
    if not isinstance(corpus, Corpus):
        raise TypeError

    corpus.raw = Raw(from_multiple_files(dir=dir))



def from_multiple_files(dir: str):
    # param check: file_dir
    if not isinstance(dir, str):
        raise TypeError
    #
    raw = dict()

    folders_and_files_name = os.listdir(dir)  # 得到该文件夹下的最高层的文件夹名和文件名（str格式）
    for folder_or_file_name in folders_and_files_name:
        folder_or_file_path = os.path.join(dir, folder_or_file_name)  # 路径拼接成相对路径
        if os.path.isfile(folder_or_file_path):
            if re.search(".raw.txt", folder_or_file_name, flags=0):
                with open(folder_or_file_path, 'r', encoding='utf8') as f:
                    raw[folder_or_file_name] = f.read()
        elif os.path.isdir(folder_or_file_path):
            raw[folder_or_file_name] = from_multiple_files(dir=folder_or_file_path)

    return raw
