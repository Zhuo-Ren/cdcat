from typing import Dict, List, Tuple, Union  # for type hinting
import copy


class Label(object):
    """
    A base class of label type

    Attributes:
        owner: AAA
        key: AAA
        config: AAA
        value: AAA
    """

    from nlp_platform.center.labels import InstanceLabels, NodeLabels

    def __init__(self, owner: Union[NodeLabels,InstanceLabels], key, value=None):
        # param check: owner
        from nlp_platform.center.labels import InstanceLabels, NodeLabels
        if not isinstance(owner, (NodeLabels, InstanceLabels)):
            raise TypeError("param 'owner' should be InstanceLabels obj or NodeLabels obj.")
        # param check: key
        if not isinstance(key, str):
            raise TypeError("param 'key' should be a string.")
        # param check: value
        pass  # in child class

        # public: owner and owner_labels
        self.owner = owner

        # public: key
        self.key = key

        # private: value
        self._value = copy.copy(self.empty_value)
        if value is not None:
            self.value = value
            "这里将调用子类中定义的value的setter，将包含同步功能如果需要的话。"

    # public: config
    @property
    def config(self) -> Dict:
        """
        The config dict of this label according to config_label_sys.json.

        :return: The config dict of this label according to config_label_sys.json.
        """
        return self.owner_labels.config[self.key]

    # public: owner_labels
    @property
    def owner_labels(self):
        return self.owner

    # public: owner_obj
    @property
    def owner_obj(self):
        return self.owner.owner

    # public: value
    @property
    def value(self):
        return self._value
    @value.setter
    def value(self,value):
        self._value = value  # 如有需要，子类应该添加linkedLabel同步机制

    def value_empty(self) -> None:
        """
        Del the label value. **And the linked label of this label will be changed synchronously.**

        :return: None
        """
        self.value = copy.copy(self.empty_value)

    def sync_add(self, value):
        self.value = value

    def sync_del(self, value):
        # sync check
        if self.value != value:
            raise RuntimeError
        #
        self._value = copy.copy(self.empty_value)

    def readable(self):
        return self.value

    def ajax_process(self, ajax_param, root_node, instance_pool):
        pass

    def to_info(self):
        info_dict = []
        for v in self._value:
            info_dict.append(v.position())
        return info_dict


class SimpleLabel(LabelType):
    def __init__(self, owner, key, value: Union[None, str] = None):
        # public
        self.empty_value = None
        #
        super().__init__(owner=owner, key=key, value=value)

    from nlp_platform.center.nodetree import NodeTree
    from nlp_platform.center.instancepool import InstancePool

    def ajax_process(self,
                     ajax_param: str,
                     root_node: NodeTree = None,
                     instance_pool: InstancePool = None):
        """
        This function process ajax require which try to change the label value.

        :param ajax_param: The relative params in ajax require.
            String "" will be converted into None which means this label is to be
            delete( because null and undefined in js convert into "" in python).
        :param root_node: root node of all the node.
        :param instance_pool: instance pool that manages all the instance.
        :return: True if process is success, a string describe the error if process is failed
        """
        if str == "":
            self.value_empty()
            del self.owner_labels[self.config["key"]]
        else:
            self.value = ajax_param


class ListLabel(LabelType):
    def __init__(self, owner, key, value: Union[None, List[str]]=None):
        # public
        self.empty_value = []
        #
        super().__init__(owner, key, value)

    from nlp_platform.center.nodetree import NodeTree
    from nlp_platform.center.instancepool import InstancePool

    def ajax_process(self,
                     ajax_param: str,
                     root_node: NodeTree = None,
                     instance_pool: InstancePool = None):
        """
        This function process ajax require which try to change the label value.

        :param ajax_param: The relative params in ajax require.
            String "" will be converted into None which means this label is to be
            delete( because null and undefined in js convert into "" in python).
        :param root_node: root node of all the node.
        :param instance_pool: instance pool that manages all the instance.
        :return: True if process is success, a string describe the error if process is failed
        """
        if str == "":
            self.value_empty()
            del self.owner_labels[self.config["key"]]
        else:
            self.value = ajax_param


class RelationLabel(LabelType):
    def __init__(self, owner, key, value: Union[None, str]=None):
        # public: empty_value
        self.empty_value = None
        #
        super().__init__(owner, key, value)

    from nlp_platform.center.nodetree import NodeTree
    from nlp_platform.center.instancepool import InstancePool

    def ajax_process(self,
                     ajax_param: str,
                     root_node: NodeTree = None,
                     instance_pool: InstancePool = None):
        """
        This function process ajax require which try to change the label value.

        :param ajax_param: The relative params in ajax require.
            String "" will be converted into None which means this label is to be
            delete( because null and undefined in js convert into "" in python).
        :param root_node: root node of all the node.
        :param instance_pool: instance pool that manages all the instance.
        :return: True if process is success, a string describe the error if process is failed
        """
        if str == "":
            self.value_empty()
            del self.owner_labels[self.config["key"]]
        else:
            self.value = ajax_param


label_types = {
    "SimpleLabel": SimpleLabel,
    "ListLabel":   ListLabel,
    "RelationLabel": RelationLabel,
}