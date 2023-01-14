import os
import re
from nlp_platform.center.raw import Raw
from typing import Dict


def raw_from_tokenized_en2zh_text(
        path: str,
        file_suffix: str = ".xml.EN-ZH.txt$",
        file_suffix_new: str = ""
) -> Raw:
    """
    Extract pure text from a tokenized en2zh corpus and return a Raw_obj represent it.

    迭代遍历path下的所有文件，对使用后缀file_suffix的文件，判定为tokenized en2zh file(简称en2zh文件)。
    对en2zh文件，读取文本，并删除所有“|”（分词标记）。
    按照path下的文件树结构，把读取结果保存为dict。
    （注意对en2zh文件支持后缀修改，即原本以file_suffix为后缀，在输出的dict中可以改为以file_suffix_new为后缀）

    Example: <ref20221230213431>

    :param path: Path to a corpus (a txt file or a folder that contains txt
    file, those txt file contain tokenized en2zh text).
    :param file_suffix: Suffix of the tokenized en2zh text file.
    :param file_suffix_new: In the returned Raw_obj, suffix of the tokenized en2zh file will be changed into this new suffix.
    :return: A Raw_obj which contains pure text of the corpus. Tokenize info is removed.
    """
    # param check: path
    if not isinstance(path, str):
        raise TypeError
    if not os.path.exists(path):
        raise TypeError
    #
    return Raw(dict_from_tokenized_en2zh_text(path=path, file_suffix=file_suffix))


def dict_from_tokenized_en2zh_text(
        path: str,
        file_suffix: str = ".xml.EN-ZH.txt",
        file_suffix_new: str = ""
) -> Dict[str, str]:
    """
    Extract pure text from a tokenized en2zh corpus and return a dict represent it.

    迭代遍历path下的所有文件，对使用后缀file_suffix的文件，判定为tokenized en2zh file(简称en2zh文件)。
    对en2zh文件，读取文本，并删除所有“|”（分词标记）。
    按照path下的文件树结构，把读取结果保存为dict。
    （注意对en2zh文件支持后缀修改，即原本以file_suffix为后缀，在输出的dict中可以改为以file_suffix_new为后缀）

    Example: <to20221230210752>

    :param path: Path to a corpus (a txt file or a folder that contains txt
    file, those txt file contain tokenized en2zh text).
    :param file_suffix: Suffix of the tokenized en2zh text file.
    :param file_suffix_new: In the returned dict_obj, suffix of the tokenized en2zh file will be changed into this new suffix.
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
            if re.search(file_suffix+"$", file_name, flags=0):
                with open(file_path, 'r', encoding='utf8') as f:
                    text = f.read()
                    text = text.replace("|", "")
                    file_name_with_new_suffix = file_name[:(-1*len(file_suffix))] + file_suffix_new
                    raw[file_name_with_new_suffix] = text
        # if dir
        elif os.path.isdir(cur_path):
            dir_path = cur_path
            dir_name = cur_name
            raw[dir_name] = dict_from_tokenized_en2zh_text(path=dir_path, file_suffix=file_suffix)
    return raw
