from typing import Dict, List, Tuple, Union  # for type hinting


class Node(dict):
    """
    属性:
     - Node.config
     - node.pool
     - node["标签"]
    """
    # static
    # from nlp_platform.center.config import Config
    # config = Config.get_config()["center_config"]["Node"]
    import os
    import json
    from nlp_platform.center.tablepool import SearchFile
    cur_file_path = os.path.abspath(__file__)
    rootPath = cur_file_path[:cur_file_path.find("cdcat\\") + len("cdcat\\")]
    json_folder = os.path.join(rootPath, "test_unit")
    target_file_path = SearchFile('config_label.json', json_folder)
    with open(target_file_path, 'r', encoding='utf8') as f:
        config = json.load(f)["Node"]

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

    def __init__(self, info: Dict = None):
        super().__init__()

        # param check: info
        if info is None:
            info = {}  # 防止默认值为可变元素
        if not isinstance(info, dict):
            raise TypeError("param label_dict should be None or a dict.")

        # public: pool
        self._pool = None

        # labels
        from nlp_platform.center.labeltypes import label_types
        for label_key, label_config in self.config["LABELS"].items():
            label_config["key"] = label_key
            label_config["PRELIMINARY_CODE"] = self.config["PRELIMINARY_CODE"]
            self[label_key] = label_types[label_config["type"]](config=label_config, owner=self)


        for key, value in info.items():
            if key == "refer":
                pass
            else:
                self[key]["value"] = value

    @property
    def pool(self):
        return self._pool

    @pool.setter
    def pool(self, value):
        from nlp_platform.center.nodepool import NodePool
        if not isinstance(value, NodePool):
            if (value is not None) & (not isinstance(value, NodePool)):
                raise TypeError
        self._pool = value

    def to_info(self):
        r = {}
        for label_key in self:
            r.update(self[label_key].to_info())
        return r
