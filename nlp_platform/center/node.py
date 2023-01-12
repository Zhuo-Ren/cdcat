from __future__ import annotations
from typing import Dict, List, Tuple, Union, Optional  # for type hinting
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from nlp_platform.center.nodepool import NodePool


class Node(dict):
    """
    * Attribute: Node.config
    * Attribute: node_obj._pool
    * Property: node_obj.pool
    * Property: node_obj.text
    * Key: instance_obj["name_of_a_label"]

    Note: Must load center config(readme.md for details) before import Node, for example::

        Config.load_config(config_name="center_config", config_dir="Path_to_Config")
        from nlp_platform.center.node import Node
    """

    # static: Instance.config
    from nlp_platform.center.config import Config
    try:
        config: Optional[Dict] = Config.get_config()["center_config"]["Node"]
        """
        Config of Node class. For example::
        
            config = {
                "PRELIMINARY_CODE": "from random import randint",
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
    except Exception:
        raise ImportError("Must load center config before import Node.")

    def __init__(self,
                 info: Optional[Dict] = None,
                 pool: Optional[NodePool] = None):
        """
        Init function of Node.

        :param info: Info of this node obj.
        :param pool: Which nodepool obj does this instance obj belong to.
        """
        super().__init__()

        # Attribute
        self._pool: Optional['NodePool'] = None

        # param check: info
        if info is None:
            info = {}  # 防止默认值为可变元素
        if not isinstance(info, dict):
            raise TypeError("param label_dict should be None or a dict.")

        # self[label] init
        from nlp_platform.center.labeltypes import label_types
        for label_key, label_config in self.config["LABELS"].items():
            label_config["key"] = label_key
            label_config["PRELIMINARY_CODE"] = self.config["PRELIMINARY_CODE"]
            self[label_key] = label_types[label_config["type"]](config=label_config, owner=self)

        # self["id"] set
        "Must set self['id'] before set self.pool, because self['id'] is needed when set self.pool."
        if "id" in info:
            self["id"]["value"] = info["id"]

        # self.pool set
        from nlp_platform.center.nodepool import NodePool
        if isinstance(pool, NodePool):
            pool.add(self)

        # self[label] init
        "Must set self.pool before set self[label], because self.pool is needed when set self[label]."
        for key, value in info.items():
            if key != "id":
                self[key]["value"] = value

    @property
    def text(self):
        """
        What text does this Node obj corresponding to.

        Readonly. Cannot set the value of self.text directly. It is depends on self["id"]: `self.pool.corpus.raw[self["id"]["value"]]`.

        It is available only when self.pool.corpus.raw is existed.
        """
        return self.pool.corpus.raw[self["id"]["value"]]

    @property
    def pool(self):
        """
            Which NodePool obj does this Node obj belong to.

            This is a property corresponding to the attribute self._pool.

            Setter of self.pool will check the type of value.

            Setter of self.pool will **not** automatically add this Node obj into the NodePool obj.
            """
        return self._pool

    @pool.setter
    def pool(self, value):
        from nlp_platform.center.nodepool import NodePool
        if not isinstance(value, NodePool):
            if (value is not None) & (not isinstance(value, NodePool)):
                raise TypeError
        self._pool = value

    def to_info(self, text=False):
        r = {}
        for label_key in self:
            if label_key is not "text":
                r.update(self[label_key].to_info())
            else:
                pass
        if text:
            r.update({"text": self.text})
        return r
