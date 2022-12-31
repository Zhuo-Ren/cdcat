import os
import re
from nlp_platform.center.raw import Raw
from typing import Dict


def raw_from_tokenized_en2zh_text(
        path: str,
        fname_regex: str = ".xml.EN-ZH.txt$"
) -> Raw:
    """
    Extract pure text from a tokenized en2zh corpus and return a Raw_obj represent it.

    Example: <ref20221230213431>

    :param path: Path to a corpus (a txt file or a folder that contains txt
    file, those txt file contain tokenized en2zh text).
    :param fname_regex: A regEx used to identify the tokenized en2zh text file.
    :return: A Raw_obj which contains pure text of the corpus. Tokenize info is removed.
    """
    # param check: path
    if not isinstance(path, str):
        raise TypeError
    if not os.path.exists(path):
        raise TypeError
    #
    return Raw(dict_from_tokenized_en2zh_text(path=path, fname_regex=fname_regex))


def dict_from_tokenized_en2zh_text(
        path: str,
        fname_regex: str = ".xml.EN-ZH.txt$"
) -> Dict[str, str]:
    """
    Extract pure text from a tokenized en2zh corpus and return a dict represent it.

    Example: <to20221230210752>

    :param path: Path to a corpus (a txt file or a folder that contains txt
    file, those txt file contain tokenized en2zh text).
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
            raw[dir_name] = dict_from_tokenized_en2zh_text(path=dir_path, fname_regex=fname_regex)
    return raw
