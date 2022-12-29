from __future__ import annotations
from typing import Dict, List, Tuple, Union, Optional  # for type hinting
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from nlp_platform.center.instancepool import InstancePool


class Instance(dict):
    """
    * Attribute: Instance.config
    * Attribute: instance_obj._pool
    * Property: instance_obj.pool
    * Key: instance_obj["name_of_a_label"]

    Note: Must load center config(readme.md for details) before import Instance, for example::

        Config.load_config(config_name="center_config", config_dir="Path_to_Config")
        from nlp_platform.center.instance import Instance
    """

    # static: Instance.config
    from nlp_platform.center.config import Config
    try:
        config = Config.get_config()["center_config"]["Instance"]
        """
        Config of Instance class. For example::
        
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
        raise ImportError("Must load center config before import Instance.")

    def __init__(self,
                 info: Optional[Dict] = None,
                 pool: Optional[InstancePool] = None):
        """
        Init function of Instance.

        :param info: Info of this instance obj.
        :param pool: Which instancepool obj does this instance obj belong to.
        """
        super().__init__()

        # Attribute
        self._pool: Optional['InstancePool'] = None

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
        from nlp_platform.center.instancepool import InstancePool
        if isinstance(pool, InstancePool):
            pool.add(self)

        # self[label] init
        "Must set self.pool before set self[label], because self.pool is needed when set self[label]."
        for key, value in info.items():
            if key != "id":
                self[key]["value"] = value

    @property
    def pool(self):
        """
        Which InstancePool obj does this Instance obj belong to.

        This is a property corresponding to the attribute self._pool.

        Setter of self.pool will check the type of value.

        Setter of self.pool will **not** automatically add this Instance obj into the InstancePool obj.
        """
        return self._pool

    @pool.setter
    def pool(self, value: InstancePool):
        from nlp_platform.center.instancepool import InstancePool
        if (value is not None) & (not isinstance(value, InstancePool)):
            raise TypeError
        self._pool = value

    def to_info(self):
        r = {}
        for label_key in self:
            r.update(self[label_key].to_info())
        return r
