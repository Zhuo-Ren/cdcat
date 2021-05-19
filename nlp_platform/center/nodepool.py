from typing import Dict, List, Tuple, Union  # for type hinting
from nlp_platform.center.node import Node


class NodePool(dict):
    def __init__(self):
        """
        不必传owner，因为corpus对象会处理。

        """
        # public
        corpus = None
        """指向Corpus对象"""

    def add(self, node):
        # param check
        pass
        # 如果key重复，就报错
        pass
        #
        self[node["id"]["value"]] = node
        node.pool = self

    def __setitem__(self, key, value):
        # param check：
        pass
        # 如果key重复，就报错
        pass
        # 添加新值
        value.pool = self
        super().__setitem__(key, value)
