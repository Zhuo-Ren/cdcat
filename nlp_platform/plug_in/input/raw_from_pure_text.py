import os
import re
from nlp_platform.center.raw import Raw
from typing import Dict

def raw_from_pure_text(
        path: str,
        fname_regex: str = ".raw.txt$"
) -> Raw:
    """
        Extract pure text from a pure text corpus and return a Raw_obj which represent it.

        就是抽取指定文本。

        Example: <to20221230212011>

        :param path: Path to a corpus (a txt file or a folder that contains txt
        file, those txt file contain pure text).
        :param fname_regex: A regEx used to identify the tokenized en2zh text file.
        :return: A Raw_obj which contains pure text of the corpus. Tokenize info is removed.
    """
    return Raw(dict_from_pure_text(path=path, fname_regex=fname_regex))


def dict_from_pure_text(
        path: str,
        fname_regex: str = ".raw.txt$"
) -> Dict[str, str]:
    """
        Extract pure text from a pure text corpus and return a dict which represent it.

        Example: <to20221230211037>

        :param path: Path to a corpus (a txt file or a folder that contains txt
        file, those txt file contain pure text).
        :param fname_regex: A regEx used to identify the tokenized en2zh text file.
        :return: A dict which contains pure text of the corpus. Tokenize info is removed.
    """
    # param check: path
    if not isinstance(path, str):
        raise TypeError
    #
    raw = dict()
    # 迭代遍历path路径下的内容
    name_list = os.listdir(path)
    for cur_name in name_list:
        cur_path = os.path.join(path, cur_name)  # 路径拼接成相对路径
        # if file
        if os.path.isfile(cur_path):
            file_path = cur_path
            file_name = cur_name
            if re.search(fname_regex, file_name, flags=0):
                with open(file_path, 'r', encoding='utf8') as f:
                    text = f.read()
                    text = text.replace("|", "")
                    raw[file_name] = text
        # if dir
        elif os.path.isdir(cur_path):
            dir_path = cur_path
            dir_name = cur_name
            raw[dir_name] = dict_from_pure_text(path=dir_path, fname_regex=fname_regex)
    return raw
