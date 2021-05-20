from typing import Dict, List, Tuple, Union, Optional  # for type hinting
import copy


class Label(dict):
    """
    A base class of label type.

    Attributes:
        self["owner"]: AAA
        self["key"]: label name
        self["value"]: label value
        self["required"]: this label is mandatory(True) or optional(False)
    """
    def __init__(self, config, owner=None):
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
        # param check: owner
        from nlp_platform.center.node import Node
        from nlp_platform.center.instance import Instance
        if (owner is not None) and (not isinstance(owner, (Node, Instance))):
            raise TypeError("param 'owner' should be Instance obj or Node obj.")
        # param check: config
        if not isinstance(config, dict):
            raise TypeError("param 'config' should be a dict.")
        if "key" not in config:
            raise RuntimeError("A 'key' is required in param 'config'")

        # public: owner
        self["owner"] = owner

        # public: key
        self["key"] = config["key"]

        # public: value
        pass

        # public: required
        if "required" in config:
            self.required = True
        else:
            self.required = False

    # def to_info(self):
    #     if self["key"] == "id":
    #         return {"id": self["value"]}
    #     else:
    #         pass
    #         # return {"test": "test"}

class SimpleLabel(Label):
    """
    Attributes:
        self["owner"]: AAA
        self["key"]: label name
        self["value"]: label value
        self["required"]: this label is mandatory(True) or optional(False)
        self["value_init"]: init value of this label
        self["value_type_hint"]: 可选 type hint of label value
        self["value_optional"]: 可选 options of label value
    """
    def __init__(self, config, owner=None):
        """
        init.

        example::

            >>> c = {
                    "required": "True",  # 是否必选。值是什么都无所谓，只要有required这项，一律认为是必选标签
                    "value_type_hint": "str",  # 类型限定。值必须是python中的简单类型。
                    "value_init": "'%03d' % randint(0, 999)"  # 初始值。值由eval()执行，需要的前导代码写在配置的"PRELIMINARY_CODE"中。
                    "value_optional": ["none", "entity", "event"]  # 可选值。本例中，初始值就不在可选范围内，所以是会报错的。
                    "可以有别的项": "但不会被读取"
                }
            >>> SimpleLabel(owner = a_table_pool, config = c)

        :param owner:
        :type owner: Union[
            nlp_platform.center.node.Node,
            nlp_platform.center.instance.Instance
          ]
        :param config: Configuration of this label. {"key": "XXXX"}
        :type config: dict
        """
        # 父类的初始化
        super().__init__(owner=owner, config=config)

        # PRELIMINARY_CODE
        if "PRELIMINARY_CODE" in config:
            exec(config["PRELIMINARY_CODE"])

        # public;["value_init"]
        self["value_init"] = config["value_init"]

        # public: ["value_type_hint"]
        if "value_type_hint" in config:
            self["value_type_hint"] = config["value_type_hint"]

        # public: ["value_optional"]
        if "value_optional" in config:
            self["value_optional"] = config["value_optional"]

        # public: ["value"]
        value = eval(self["value_init"])
        if "value_type_hint" in self:
            if not eval(self["value_type_hint"]):
                raise TypeError("Value of this label do not match the type hint.")
        if "value_optional" in self:
            if value not in self["value_optional"]:
                raise TypeError("Value of this label do not match the options.")
        self["value"] = value

    def __setitem__(self, key, value):
        if key == "value":
            if "value_type_hint" in self:
                if not eval(self["value_type_hint"]):
                    raise TypeError("Value of this label do not match the type hint.")
            if "value_optional" in self:
                if value not in self["value_optional"]:
                    raise TypeError("Value of this label do not match the options.")
            super().__setitem__(key, value)
        else:
            super().__setitem__(key, value)

    def to_info(self):
        return {self["key"]: self["value"]}

class ListLabel(Label):
    pass
#     """
#     Attributes:
#         self["owner"]: AAA
#         self["key"]: label name
#         self["value"]: label value
#         self["required"]: this label is mandatory(True) or optional(False)
#         self["value_init"]: init value of this label
#         self["value_type_hint"]: 可选 type hint of label value
#         self["value_optional"]: 可选 options of label value
#     """
#     def __init__(self, owner, config):
#         """
#         init.
#
#         :param owner:
#         :type owner: Union[
#             nlp_platform.center.node.Node,
#             nlp_platform.center.instance.Instance
#           ]
#         :param config: Configuration of this label. {"key": "XXXX"}
#         :type config: dict
#         """
#         # 父类的初始化
#         super().__init__(owner, config)
#
#         # PRELIMINARY_CODE
#         if "PRELIMINARY_CODE" in config:
#             eval(config["PRELIMINARY_CODE"])
#
#         # public;["value_init"]
#         self["value_init"] = config["value_init"]
#
#         # public: ["value_type_hint"]
#         if "value_type_hint" in config:
#             self["value_type_hint"] = config["value_type_hint"]
#
#         # public: ["value_optional"]
#         if "value_optional" in config:
#             self["value_optional"] = config["value_optional"]
#
#         # public: ["value"]
#         value = eval(" t = " + self["value_init"])
#         if "value_type_hint" in self:
#             if not eval(self["value_type_hint"]):
#                 raise TypeError("Value of this label do not match the type hint.")
#         if "value_optional" in self:
#             if value not in self["value_optional"] :
#                 raise TypeError("Value of this label do not match the options.")
#         self["value"] = value


class RelationLabel(Label):
    """
    Attributes:
        self["owner"]: AAA
        self["key"]: label name
        self["value"]: label value
        self["required"]: this label is mandatory(True) or optional(False)
        self["table_name"]: this label refer to which table
        self["index_self"]: 这个label的owner是表中的第0列还是第1列. 如果对应的table是无向的，则不写这项。
        self["index_value"]: 这个label的value是表中的第0列还是第1列. 如果对应的table是无向的，则不写这项。
        self["value_init"]: init value of this label
    """
    def __init__(self, config, owner=None):
        """
        init.

        example::

            >>> c = {
                    "relation_name": "mention_to_instance",
                    "index_self": "1",
                    "index_value": "0"
                }
            >>> RelationLabel(owner = a_table_pool, config = c)

        :param owner:
        :type owner: Union[
            nlp_platform.center.node.Node,
            nlp_platform.center.instance.Instance
          ]
        :param config: Configuration of this label.
        :type config: dict
        """
        # 父类的初始化
        super().__init__(owner=owner, config=config)

        # PRELIMINARY_CODE
        if "PRELIMINARY_CODE" in config:
            exec(config["PRELIMINARY_CODE"])

        # public;["table_name"]
        self["table_name"] = config["table_name"]

        # public;["index_self"]
        self["index_self"] = config["index_self"]

        # public: ["index_value"]
        self["index_value"] = config["index_value"]

        # public: ["value"]
        pass

    def __getitem__(self, key):
        if key == "value":
            c = self["owner"].pool.corpus
            t = c.tp[self["table_name"]]
            self_id = self["owner"]["id"]

            # 获取对应的relations
            if 1:
                # 有向图
                if "index_self" in self:
                    try:
                        if self["index_self"] == "0":
                            r = t[self_id["value"], None]
                        elif self["index_self"] == "1":
                            r = t[None, self_id["value"]]
                    except KeyError:
                        return None
                # 无向图
                else:
                    try:
                        r = t[self_id]
                    except KeyError:
                        return None
            r_relations = r.to_dict()

            # 把relation转成对应的node或instance
            r_obj_list = []
            for cur_relation in r_relations:
                # 有向图
                if "index_self" in self:
                    # 识别哪个节点是自己，哪个节点是值
                    other_id = cur_relation[self["index_value"]]
                    # 把id转成节点对象
                    if other_id[0:2] == "i:":
                        other_obj = c.ip[other_id]
                    elif other_id[0:2] == "n:":
                        other_obj = c.np[other_id]
                    #
                    r_obj_list.append(other_obj)
                # 无向图
                else:
                    # 识别哪个节点是自己，哪个节点是值
                    if cur_relation[0] == self_id:
                        other_id = cur_relation[1]
                    else:
                        other_id = cur_relation[0]
                    # 把id转成节点对象
                    if other_id[0:2] == "i:":
                        other_obj = c.ip[other_id]
                    elif other_id[0:2] == "n:":
                        other_obj = c.np[other_id]
                    #
                    r_obj_list.append(other_obj)

            return r_obj_list
        else:
            return super().__getitem__(key)

    def __setitem__(self, key, value):
        if key == "value":
            if "value_type_hint" in self:
                if not eval(self["value_type_hint"]):
                    raise TypeError("Value of this label do not match the type hint.")
            if "value_optional" in self:
                if value not in self["value_optional"]:
                    raise TypeError("Value of this label do not match the options.")
        else:
            super().__setitem__(key, value)

    def to_info(self):
        return {self["key"]: self["value"]}


label_types = {
    "SimpleLabel": SimpleLabel,
    "ListLabel":   ListLabel,
    "RelationLabel": RelationLabel,
}