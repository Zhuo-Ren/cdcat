from typing import Dict, List, Tuple, Union  # for type hinting
import platform

class Instance(dict):
    """
    属性:
     - Instance.config
     - instance.pool
     - node["标签"]
    """

    # static
    from nlp_platform.center.config import Config
    config = Config.get_config()["center_config"]["Instance"]
    """
        for example::
        config = {
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

    def __init__(self, info: Dict = None, pool=None):
        super().__init__()

        # param check: info
        if info is None:
            info = {}  # 防止默认值为可变元素
        if not isinstance(info, dict):
            raise TypeError("param label_dict should be None or a dict.")

        # public: pool
        self._pool = None

        # labels初始化
        from nlp_platform.center.labeltypes import label_types
        for label_key, label_config in self.config["LABELS"].items():
            label_config["key"] = label_key
            label_config["PRELIMINARY_CODE"] = self.config["PRELIMINARY_CODE"]
            self[label_key] = label_types[label_config["type"]](config=label_config, owner=self)

        # self["id"]赋值
        if "id" in info:
            self["id"]["value"] = info["id"]

        # self.pool赋值
        from nlp_platform.center.instancepool import InstancePool
        if isinstance(pool, InstancePool):
            if "id" not in info:
                raise RuntimeError("如果要指定pool，必须先指定id")
            else:
                pool.add(self)

        # labels的赋值(非id)
        for key, value in info.items():
            if key != "id":
                self[key]["value"] = value

    @property
    def pool(self):
        return self._pool

    @pool.setter
    def pool(self, value):
        from nlp_platform.center.instancepool import InstancePool
        if (value is not None) & (not isinstance(value, InstancePool)):
            raise TypeError
        self._pool = value

    def to_info(self):
        r = {}
        for label_key in self:
            r.update(self[label_key].to_info())
        return r
