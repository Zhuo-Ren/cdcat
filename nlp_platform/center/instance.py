from typing import Dict, List, Tuple, Union  # for type hinting


class Instance(dict):
    """
    属性:
     - Instance.config
     - instance.instance_pool
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
        from nlp_platform.center.instancepool import InstancePool
        if (pool is not None) & (not isinstance(pool, InstancePool)):
            raise TypeError

        # param check: info
        if info is None:
            info = {}  # 防止默认值为可变元素
        if not isinstance(info, dict):
            raise TypeError("param label_dict should be None or a dict.")

        # public: instance_pool
        self.instance_pool = pool

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
import sys
import os
cur_file_path = os.path.abspath(sys.argv[0])
cur_folder_path = os.path.dirname(cur_file_path)
target_file_path = os.path.join(cur_folder_path, "config_label.json")
with open(target_file_path, 'r', encoding='utf8') as f:
    config = json.load(f)
Instance.config = config["Instance"]
