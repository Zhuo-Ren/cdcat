from typing import Dict, List, Tuple, Union  # for type hinting


class Node(dict):
    """
    属性:
     - Node.config
     - node.node_pool
     - node["标签"]
    """
    # static
    config = {}
    """
        for example::
        {
            "PRELIMINARY_CODE": "from random import randint \n ",
            "LABELS": {
                "id": {
                    "type": "SimpleLabel",
                    "value_type_hint": "str",
                    "value_init": "'%03d' % randint(0, 999)",
                },
                "desc": {
                    "type": "SimpleLabel",
                    "value_type_hint": "str",
                    "value_init": "self['id']"
                },
                "type": {
                    "type": "SimpleLabel",
                    "value_type_hint": "str",
                    "value_init": "none",
                    "value_optional": ["none", "entity", "event"]
                }
            }
        }
    """

    def __init__(self, pool=None, info: Dict = None):
        super().__init__()

        # param check: instance_pool
        from nlp_platform.center.nodepool import NodePool
        if (pool is not None) & (not isinstance(pool, NodePool)):
            raise TypeError

        # param check: info
        if info is None:
            info = {}  # 防止默认值为可变元素
        if not isinstance(info, dict):
            raise TypeError("param label_dict should be None or a dict.")

        # public: instance_pool
        self.node_pool = pool

        # labels
        from nlp_platform.center.labeltypes import label_types
        for label_key, label_config in self.config["LABELS"].items():
            self[label_key] = label_types[label_config["type"]](label_config)

    def to_info(self):
        r = {}
        for label_key in self:
            r.update(self[label_key].to_info())
        return r


# 加载配置
import json
with open('./label_config.json', 'r', encoding='utf8') as f:
    config = json.load(f)
Node.config = config["Node"]
