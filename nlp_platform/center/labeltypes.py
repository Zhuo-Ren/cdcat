from typing import Dict, List, Tuple, Union  # for type hinting
import copy


class Label(dict):
    """
    A base class of label type.

    Attributes:
        owner: AAA
        key: AAA
        value: AAA
    """
    def __init__(self, owner, config):
        """
        XXX

        :param owner:
        :type owner: Union[
            nlp_platform.center.node.Node,
            nlp_platform.center.instance.Instance
          ]
        :param config: Configuration of this label. {"key": "XXXX"}
        :type config: dict
        """
        # param check: owner
        from nlp_platform.center.node import Node
        from nlp_platform.center.instance import Instance
        if not isinstance(owner, (Node, Instance)):
            raise TypeError("param 'owner' should be Instance obj or Node obj.")
        # param check: config
        if not isinstance(config, dict):
            raise TypeError("param 'config' should be a dict.")
        if "key" not in config:
            raise RuntimeError("A 'key' is required in param 'config'")

        # public: ["owner"]
        self["owner"] = owner

        # public: ["key"]
        self["key"] = config["key"]


class SimpleLabel(Label):
    def __init__(self, owner, config):
        """
        init.

        :param owner:
        :type owner: Union[
            nlp_platform.center.node.Node,
            nlp_platform.center.instance.Instance
          ]
        :param config: Configuration of this label. {"key": "XXXX"}
        :type config: dict
        """
        # 父类的初始化
        super().__init__(owner, config)

        # PRELIMINARY_CODE
        if "PRELIMINARY_CODE" in config:
            eval(config["PRELIMINARY_CODE"])

        # public;["value_init"]
        self["value_init"] = config["value_init"]

        # public: ["value_type_hint"]
        if "value_type_hint" in config:
            self["value_type_hint"] = config["value_type_hint"]

        # public: ["value_optional"]
        if "value_optional" in config:
            self["value_optional"] = config["value_optional"]

        # public: ["value"]
        value = eval(" t = " + self["value_init"])
        if "value_type_hint" in self:
            if not isinstance(value, eval(self["value_type_hint"])):
                raise TypeError("Value of this label do not match the type hint.")
        if "value_optional" in self:
            if value not in self["value_optional"] :
                raise TypeError("Value of this label do not match the options.")
        self["value"] = value


class ListLabel(Label):
    def __init__(self, owner, config):
        """
        init.

        :param owner:
        :type owner: Union[
            nlp_platform.center.node.Node,
            nlp_platform.center.instance.Instance
          ]
        :param config: Configuration of this label. {"key": "XXXX"}
        :type config: dict
        """
        # 父类的初始化
        super().__init__(owner, config)

        # PRELIMINARY_CODE
        if "PRELIMINARY_CODE" in config:
            eval(config["PRELIMINARY_CODE"])

        # public;["value_init"]
        self["value_init"] = config["value_init"]

        # public: ["value_type_hint"]
        if "value_type_hint" in config:
            self["value_type_hint"] = config["value_type_hint"]

        # public: ["value_optional"]
        if "value_optional" in config:
            self["value_optional"] = config["value_optional"]

        # public: ["value"]
        value = eval(" t = " + self["value_init"])
        if "value_type_hint" in self:
            if not isinstance(value, eval(self["value_type_hint"])):
                raise TypeError("Value of this label do not match the type hint.")
        if "value_optional" in self:
            if value not in self["value_optional"] :
                raise TypeError("Value of this label do not match the options.")
        self["value"] = value


class RelationLabel(Label):
    def __init__(self, owner, config):
        """
        init.

        :param owner:
        :type owner: Union[
            nlp_platform.center.node.Node,
            nlp_platform.center.instance.Instance
          ]
        :param config: Configuration of this label. {"key": "XXXX"}
        :type config: dict
        """
        # 父类的初始化
        super().__init__(owner, config)

        # PRELIMINARY_CODE
        if "PRELIMINARY_CODE" in config:
            eval(config["PRELIMINARY_CODE"])

        # public;["value_init"]
        self["value_init"] = config["value_init"]

        # public: ["value_type_hint"]
        if "value_type_hint" in config:
            self["value_type_hint"] = config["value_type_hint"]

        # public: ["value_optional"]
        if "value_optional" in config:
            self["value_optional"] = config["value_optional"]

        # public: ["value"]
        value = eval(" t = " + self["value_init"])
        if "value_type_hint" in self:
            if not isinstance(value, eval(self["value_type_hint"])):
                raise TypeError("Value of this label do not match the type hint.")
        if "value_optional" in self:
            if value not in self["value_optional"] :
                raise TypeError("Value of this label do not match the options.")
        self["value"] = value


label_types = {
    "SimpleLabel": SimpleLabel,
    "ListLabel":   ListLabel,
    "RelationLabel": RelationLabel,
}