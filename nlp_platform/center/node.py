from typing import Dict, List, Tuple, Union  # for type hinting


class Node(dict):
    # static
    config = {}

    def __init__(self, instance_pool=None, info: Dict = None):
        # param check: instance_pool
        from nlp_platform.center.instancepool import InstancePool
        if (instance_pool is not None) & (not isinstance(instance_pool, InstancePool)):
            raise TypeError

        # param check: info
        if info is None:
            info = {}  # 防止默认值为可变元素
        if not isinstance(info, dict):
            raise TypeError("param label_dict should be None or a dict.")

        # public: instance_pool
        self.instance_pool = instance_pool

        # labels
        from nlp_platform.center.labeltypes import labeltypes
        for key in self.config:
            label_config = self.config[key]
            self[key] = labeltypes[label_config[key]["type"]](label_config)

    def to_info(self, include_id_label=True, include_fixed_label=True):
        r = {}
        if self._labels is not None:
            r.update(self.labels.to_info())
        if include_id_label is False:
            del r["id"]
        if include_fixed_label is False:
            del r["desc"]
        return r


# 加载配置
import json

with open('./label_config.json', 'r', encoding='utf8') as f:
    label_config = json.load(f)
Node.config = label_config["None"]
