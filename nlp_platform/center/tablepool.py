from typing import Dict, List, Tuple, Union  # for type hinting
from nlp_platform.center.table import DirectedRelationTable as Drt
from nlp_platform.center.table import UndirectedRelationTable as Urt
import os
import platform

def SearchFile(filename, pathname):
    for root, dirs, files in os.walk(pathname, False):
        for name in files:
            if filename == name:
                return os.path.join(root, name)
    return None

class TablePool(dict):
    def __init__(self, corpus=None):
        """
        不必传owner，因为corpus对象会处理。

        """
        # public
        self.corpus = corpus
        """指向Corpus对象"""

        # 加载配置
        import json
        import sys
        import os
        cur_file_path = os.path.abspath(__file__)
        if platform.platform()[0: 6] == "Darwin":  # 增加了操作系统的区分
            rootPath = cur_file_path[:cur_file_path.find("cdcat/") + len("cdcat/")]
        elif platform.platform()[0: 7] == "Windows":
            rootPath = cur_file_path[:cur_file_path.find("cdcat\\") + len("cdcat\\")]
        json_folder = os.path.join(rootPath, "test_unit")
        target_file_path = SearchFile('config_label.json', json_folder)
        with open(target_file_path, 'r', encoding='utf8') as f:
            config = json.load(f)
        self.config = config["Relation"]
        for cur_table_name, cur_table_config in self.config.items():
            if cur_table_config["type"] == "DRT":
                self[cur_table_name] = Drt(
                    max_o_degree=eval(self.config[cur_table_name]["max_o_degree"]),
                    max_i_degree=eval(self.config[cur_table_name]["max_i_degree"]),
                )
            elif cur_table_config["type"] == "URT":
                self[cur_table_name] = Urt(
                    max_degree=eval(self.config["max_degree"]),
                )

    # def add(self, node):
    #     # param check
    #     pass
    #     # 如果key重复，就报错
    #     pass
    #     #
    #     self[node["id"]] = node
    #     node.pool = self