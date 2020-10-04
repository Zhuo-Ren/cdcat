from typing import Dict, List, Tuple, Union  # for type hinting

def regiest_cofigured_label_types():
    from nlp_plantform.plug_in.manual_annotation_tool.cdcat import config as cdcat_config
    from nlp_plantform.center.labels import NodeLabels, InstanceLabels
    import json
    with open(cdcat_config.label_sys_dict_path, 'r', encoding='utf8') as labelf:
        label_sys_dict = json.load(labelf)
    for cur_label in label_sys_dict["node"]:
        NodeLabels.config.update({
            cur_label["key"]: cur_label
        })
    for cur_label in label_sys_dict["instance"]:
        InstanceLabels.config.update({
            cur_label["key"]: cur_label
        })


class AutoSyncList(list):

    def __init__(self, owner, init_value, type_limit: Union[Tuple, None] = None):
        # public: owner
        self.owner = owner

        # public: type_limit
        self.type_limit = type_limit

        # init
        if isinstance(init_value, AutoSyncList,list):
            for i in init_value:
                self.append(i)  # self.append will sync the linked label
        else:
            if self.type_limit is not None:
                if not isinstance(init_value, self.type_limit):
                    raise TypeError
            self.append(init_value) # self.append will sync the linked label

    # public: owner_label
    @property
    def owner_label(self):
        o = self.owner
        while not isinstance(o, LabelType):
            o = o.owner
        return o

    # public: owner_labels
    @property
    def owner_labels(self):
        return self.owner_label.owner

    # public: owner_obj
    @property
    def owner_obj(self):
        return self.owner_labels.owner

    def append(self, object) -> None:
        if isinstance(object, AutoSyncList, list):
            # sync new value
            "同步工作将由新AutoSyncList对象的构造函数完成。"
            # append
            super().append(self, AutoSyncList(owner=self, init_value=object, type_limit=self.type_limit))
        else:
            if self.type_limit is not None:
                if not isinstance(object, self.type_limit):
                    raise TypeError
            # sync new value
            linked_label = object._value.labels[self.config["linkto"]]
            linked_label.sync_add(self.owner_obj)
            # append
            super().append(self, object)

    def insert(self, index: int, object) -> None:
        if isinstance(object, AutoSyncList, list):
            # sync new value
            "同步工作将由新AutoSyncList对象的构造函数完成。"
            # append
            super().insert(self, index, AutoSyncList(owner=self, init_value=object, type_limit=self.type_limit))
        else:
            if self.type_limit is not None:
                if not isinstance(object, self.type_limit):
                    raise TypeError
            # sync new value
            linked_label = object._value.labels[self.config["linkto"]]
            linked_label.sync_add(self.owner_obj)
            # append
            super().insert(self, index, object)

    def clear(self):
        # sync old value
        for i in self:
            if isinstance(i, AutoSyncList):
                i.clear()
            else:
                linked_label = i.labels[self.owner_label.config["linkto"]]
                linked_label.sync_del(self.owner_obj)
        #
        super().clear(self)

    def sync_add(self, value) -> bool:
        # param check
        if not isinstance(value, (AutoSyncList, self.type_limit)):
            raise TypeError
        #
        list.append(self, value)
        return True

    def sync_del(self, value)-> bool:
        # param check
        if not isinstance(value, self.type_limit):
            raise TypeError
        #
        for item_index in range(len(self)):
            # 如果item是list
            if isinstance(self[item_index], AutoSyncList):
                success_flag = success_flag and self[item_index].sync_del(value)
            # 如果item是node或instances
            else:
                if self[item_index] == value:
                    del self[item_index]
                    success_flag = True
        if success_flag == False:
            raise RuntimeError
        else:
            return True

    def readable(self):
        r = []
        for i in self:
            if isinstance(i, AutoSyncList):
                r.append(i.readable())
            else:
                r.append(i.readable(nolink=True))
        return r


class LabelType(object):
    """
    A base class of label type

    Attributes:
        owner: AAA
        key: AAA
        config: AAA
        value: AAA
    """

    from nlp_plantform.center.labels import InstanceLabels, NodeLabels

    def __init__(self, owner: Union[NodeLabels,InstanceLabels], key, value=None):
        # param check: owner
        from nlp_plantform.center.labels import InstanceLabels, NodeLabels
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
        self._value = self.empty_value
        if value is None:
            self._value = self.empty_value
        else:
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
        self.value = self.empty_value

    def sync_add(self, value):
        self.value = value

    def sync_del(self, value):
        # sync check
        if self.value != value:
            raise RuntimeError
        #
        self.value = self.empty_value

    def readable(self):
        return self.value

    def ajax_process(self, ajax_param):
        pass


class LabelTypeRadio(LabelType):
    def __init__(self, owner, key, value: Union[None, str] = None):
        # public
        self.empty_value = None
        #
        super().__init__(owner=owner, key=key, value=value)

    from nlp_plantform.center.nodetree import NodeTree
    from nlp_plantform.center.instancepool import InstancePool

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


class LabelTypeCheckbox(LabelType):
    def __init__(self, owner, key, value: Union[None, List[str]]=None):
        # public
        self.empty_value = []
        #
        super().__init__(self, owner, key, value)

    from nlp_plantform.center.nodetree import NodeTree
    from nlp_plantform.center.instancepool import InstancePool

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


class LabelTypeMenuOne(LabelType):
    def __init__(self, owner, key, value: Union[None, str]=None):
        super().__init__(self, owner, key, value)
        # public
        self.empty_value = None

    from nlp_plantform.center.nodetree import NodeTree
    from nlp_plantform.center.instancepool import InstancePool

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


class LabelTypeMenuMulti(LabelType):
    def __init__(self, owner, key, value: Union[None, List[str]]=None):
        super().__init__(self, owner, key, value)
        # public
        self.empty_value = []

    from nlp_plantform.center.nodetree import NodeTree
    from nlp_plantform.center.instancepool import InstancePool

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


class LabelTypeTextReadonly(LabelType):
    def __init__(self, owner, key, value: Union[None, str]=None):
        super().__init__(self, owner, key, value)
        # public
        self.empty_value = None

    from nlp_plantform.center.nodetree import NodeTree
    from nlp_plantform.center.instancepool import InstancePool

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
        raise RuntimeError("A TextReadonly label receive a edit ajax quire.")


class LabelTypeTextInput(LabelType):
    def __init__(self, owner, key, value: Union[None, str]=None):
        super().__init__(self, owner, key, value)
        # public
        self.empty_value = None

    from nlp_plantform.center.nodetree import NodeTree
    from nlp_plantform.center.instancepool import InstancePool

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


class LabelTypeNode(LabelType):
    from nlp_plantform.center.nodetree import NodeTree
    def __init__(self, owner, key, value: Union[None, NodeTree] =None):
        # param check
        from nlp_plantform.center.nodetree import NodeTree
        if isinstance(value, NodeTree)or (value is None):
            raise TypeError
        # public
        self.empty_value = None
        #
        super().__init__(self, owner, key, value)

    # public: value
    from nlp_plantform.center.nodetree import NodeTree
    @property
    def value(self) -> Union[None, NodeTree]:
        """
        Value of the InstanceLabel. It can be None or a Instance obj.

        :return: Value of the InstanceLabel.
        """
        return self._value
    @value.setter
    def value(self, value: Union[None, NodeTree]) -> None:
        """
        Set the label a new value. **And the linked label of this label will be changed synchronously.**

        :param value: A obj that represent the new value of the label. It can be None, Instance obj, or instance info dict.
        """
        from nlp_plantform.center.instance import Instance
        # get the real_value
        if value in [None, self.empty_value]:
            new_value = self.empty_value
        elif isinstance(value, Instance):
            new_value = value
        else:
            raise TypeError
        # sync old value
        if self._value != self.empty_value:
            linked_label = self._value.labels[self.config["linkto"]]
            linked_label.sync_del(self.owner_obj)
        #
        self._value = new_value
        # sync new value
        if self._value != self.empty_value:
            linked_label = self._value.labels[self.config["linkto"]]
            linked_label.sync_add(self.owner_obj)

    def sync_del(self, value: NodeTree) -> None:
        # param check
        from nlp_plantform.center.nodetree import NodeTree
        if not isinstance(value, NodeTree):
            raise TypeError("param 'value' should be a Instance obj")
        # sync check
        if self.value != value:
            raise RuntimeError
        #
        self.value = self.empty_value

    def sync_add(self, value: NodeTree) -> None:
        # param check
        from nlp_plantform.center.nodetree import NodeTree
        if not isinstance(value, NodeTree):
            raise TypeError("param 'value' should be a Instance obj")
        #
        self.value = value

    def readable(self):
        if self.value == self.empty_value:
            return None
        else:
            return  self.value.readable(nolink=True)

    from nlp_plantform.center.nodetree import NodeTree
    from nlp_plantform.center.instancepool import InstancePool

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
        if ajax_param is None:
            self.value_empty()
            del self.owner_labels[self.config["key"]]
        else:
            # get node
            start_position = ajax_param["start"]
            end_position = ajax_param["end"]
            node = root_node.is_annotated(root_node, start_position, end_position)
            if node is None:
                return "no such node."
            #
            self.value = node
            return True


class LabelTypeInstance(LabelType):
    from nlp_plantform.center.instance import Instance
    def __init__(self, owner, key, value: Union[None, Dict, Instance]=None):
        # param check
        from nlp_plantform.center.instance import Instance
        if isinstance(value, Instance)or (value is None):
            raise TypeError
        # public
        self.empty_value = None
        #
        super().__init__(self, owner, key, value)

    # public: value
    from nlp_plantform.center.instance import Instance
    @property
    def value(self) -> Union[None, Instance]:
        """
        Value of the InstanceLabel. It can be None or a Instance obj.

        :return: Value of the InstanceLabel.
        """
        return self._value
    @value.setter
    def value(self, value: Union[None, Instance]) -> None:
        """
        Set the label a new value. **And the linked label of this label will be changed synchronously.**

        :param value: A obj that represent the new value of the label. It can be None, Instance obj, or instance info dict.
        """
        from nlp_plantform.center.instance import Instance
        # get the real_value
        if value in [None, self.empty_value]:
            new_value = self.empty_value
        elif isinstance(value, Instance):
            new_value = value
        else:
            raise TypeError
        # sync old value
        if self._value != self.empty_value:
            linked_label = self._value.labels[self.config["linkto"]]
            linked_label.sync_del(self.owner_obj)
        #
        self._value = new_value
        # sync new value
        if self._value != self.empty_value:
            linked_label = self._value.labels[self.config["linkto"]]
            linked_label.sync_add(self.owner_obj)

    def sync_del(self, value: Instance) -> None:
        # param check
        from nlp_plantform.center.instance import Instance
        if not isinstance(value, Instance):
            raise TypeError("param 'value' should be a Instance obj")
        # sync check
        if self.value != value:
            raise RuntimeError
        #
        self.value = self.empty_value

    def sync_add(self, value: Instance) -> None:
        # param check
        from nlp_plantform.center.instance import Instance
        if not isinstance(value, Instance):
            raise TypeError("param 'value' should be a Instance obj")
        #
        self.value = value

    def readable(self):
        if self.value == self.empty_value:
            return None
        else:
            return  self.value.readable(nolink=True)

    from nlp_plantform.center.nodetree import NodeTree
    from nlp_plantform.center.instancepool import InstancePool

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
        if ajax_param is None:
            self.value_empty()
            del self.owner_labels[self.config["key"]]
        else:
            # get instance
            new_instance = instance_pool.get_instance({"id": ajax_param["instance"]})[0]
            self.value = new_instance
            return True


class LabelTypeNodeList(LabelType):
    def __init__(self, owner, key, value=None):
        """
        - If param *value* is None, the label value is None.
        - If param *value* is a info dict that describe somen Node obj, this function search for nodes that match
          the info dict, and returns a nodesLabel based on the nodes.

        :param owner: A label should belongs to a InstanceLabels obj or a NodeLabels obj which is called 'owner of a label'.
        :param key: The key of this label in config_label_sys.json
        :param value: A obj that represent the label value.
        """
        super().__init__(self, owner, key, value)
        # public
        from nlp_plantform.center.nodetree import NodeTree
        self.empty_value = AutoSyncList(owner=self, init_value=[], type_limit=NodeTree)

    # public: value
    @property
    def value(self) -> AutoSyncList:
        """
        Value of the InstanceLabel. It can be None or a Instance obj.

        :return: Value of the InstanceLabel.
        """
        return self._value
    @value.setter
    def value(self, value: Union[None, list]) -> None:
        """
        Set the label a new value. **And the linked label of this label will be changed synchronously.**

        :param value: A obj that represent the new value of the label. It can be None, Instance obj, or instance info dict.
        """
        from nlp_plantform.center.nodetree import NodeTree
        # get the real_value
        if value in [None, self.empty_value]:
            new_value = self.empty_value
        else:
            if isinstance(value, list, AutoSyncList):
                new_value = AutoSyncList(owner=self, init_value=value, type_limit=NodeTree)
        # sync old value
        if self._value != self.empty_value:
            if not isinstance(self._value, AutoSyncList):
                raise TypeError
            for i in self._value:
                if isinstance(i, AutoSyncList):
                    i.clear()
                elif isinstance(i, NodeTree):
                    linked_label = i.labels[self.config["linkto"]]
                    linked_label.sync_del(self.owner_obj)
        #
        self._value = new_value
        # sync new value
        "无需再同步新值，因为在new_value=AutoSyncList()时，构造函数已经实现了同步。"

    def sync_add(self, value):
        # param check
        from nlp_plantform.center.nodetree import NodeTree
        if not isinstance(value, NodeTree):
            raise TypeError
        #
        self._value.sync_add(value)

    def sync_del(self, value):
        # param check
        from nlp_plantform.center.nodetree import NodeTree
        if not isinstance(value, NodeTree):
            raise TypeError
        #
        self._value.sync_del(value)


    def readable(self):
        return  self._value.readable()


labeltypes = {
    "radio":        LabelTypeRadio,
    "checkbox":     LabelTypeCheckbox,
    "menuone":      LabelTypeMenuOne,
    "menumulti":    LabelTypeMenuMulti,
    "textreadonly": LabelTypeTextReadonly,
    "textinput":    LabelTypeTextInput,
    "instance":     LabelTypeInstance,
    "node":         LabelTypeNode,
    "nodelist":     LabelTypeNodeList
}