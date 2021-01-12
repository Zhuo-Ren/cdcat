from typing import Dict, List, Tuple, Union, Optional  # for type hinting
from nlp_plantform.center.instance import Instance
from nlp_plantform.center.nodetree import NodeTree
from nlp_plantform.center.labels import Labels
import copy

#读取配置文件，并将配置信息放入Nodelabels和InstanceLabels的config中。  比我的代码更先进，我是都取出来然后各取所需
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

def read_config() -> Dict:
    from nlp_plantform.plug_in.manual_annotation_tool.cdcat.config import label_sys_dict_path
    import json
    with open(label_sys_dict_path) as json_file:
        config = json.load(json_file)
    return config

class AutoSyncList(list):

    def __init__(self, owner, init_value=None, type_limit: Union[Tuple, None] = None):
        # public: owner
        self.owner = owner

        # public: type_limit
        self.type_limit = type_limit

        # init
        if init_value is None:
            init_value = []
        if isinstance(init_value, (AutoSyncList, list)):
            for i in init_value:
                self.append(i)  # self.append will sync the linked label
        else:
            if self.type_limit is not None:
                if not isinstance(init_value, self.type_limit):
                    raise TypeError
            self.append(init_value)  # self.append will sync the linked label

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

    def append(self, icon) -> None:
        stock = self  # stock砧木; icon接穗
        # append一个AutoSyncList
        if isinstance(icon, AutoSyncList):
            # sync new value
            "同步工作将由新AutoSyncList对象的构造函数完成。"
            # append
            super().append(AutoSyncList(owner=stock, init_value=icon, type_limit=stock.type_limit))
        # append一个对象
        else:
            if stock.type_limit is not None:
                if not isinstance(icon, stock.type_limit):
                    raise TypeError
            # sync new value
            stock_label = stock.owner_label
            icon_label_key = stock_label.config["linkto"]
            if icon_label_key not in icon.labels:
                # 如果前台修改的这个标签，在接穗中还没有创建，要先创建空标签
                from nlp_plantform.center.labeltypes import labeltypes
                cur_label_class = labeltypes[icon.labels.config[icon_label_key]["value_type"]]
                icon.labels[icon_label_key] = cur_label_class(owner=icon.labels, key=icon_label_key, value=None)
            icon_label = icon.labels[icon_label_key]
            icon_label.sync_add(stock.owner_obj)
            # append
            super().append(icon)

    def insert(self, index: int, object) -> None:
        if isinstance(object, AutoSyncList, list):
            # sync new value
            "同步工作将由新AutoSyncList对象的构造函数完成。"
            # append
            super().insert(index, AutoSyncList(owner=self, init_value=object, type_limit=self.type_limit))
        else:
            if self.type_limit is not None:
                if not isinstance(object, self.type_limit):
                    raise TypeError
            # sync new value
            linked_label = object._value.labels[self.config["linkto"]]
            linked_label.sync_add(self.owner_obj)
            # append
            super().insert(index, object)

    def clear(self):
        # sync old value
        for i in self:
            if isinstance(i, AutoSyncList):
                i.clear()
            else:
                linked_label = i.labels[self.owner_label.config["linkto"]]
                linked_label.sync_del(self.owner_obj)
        #
        super().clear()

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
        success_flag = False
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
        owner: an object of labels
        key: key of label
        config: information of label's config
        value: value of label
    """
    config = {}
    from nlp_plantform.center.labels import InstanceLabels, NodeLabels
    owner_type_class = (NodeLabels, InstanceLabels)

    def __init__(self, info: Optional[dict] = None, objs_dict: Optional[dict] = None, sync: bool = False):
        """
        A method of init label object
        Args:
            info: 简单的初始化信息，value是简单的描述
            objs_dict: 复杂的初始化信息，value可能有嵌套，比如value存放了若干个label
            sync: 是否同步
        """
        if info is None and objs_dict is None:
            # 防止默认值为可变元素
            info = {}

        # param check: info
        if not isinstance(info, dict):
            raise TypeError

        # param check: objs_dict
        if objs_dict is not None:
            if not isinstance(objs_dict, dict):
                raise TypeError


        # param check: owner
        self.owner = None
        if "owner" in info.keys():
            if not isinstance(info["owner"], self.owner_type_class):
                raise TypeError("param 'owner' should be InstanceLabels obj or NodeLabels obj")
        # param check: key
        if "key" in info.keys():
            if not isinstance(info["key"], str):
                raise TypeError("param 'key' should be a string.")

        # param check: value
        pass  # in child class

        #检查这个label是否是一个定制的label
        """
        此处还未修改。准备直接使用学长的读取配置文件方法。
        先读取NodeLabels和InstanceLabels的配置文件，根据该label的拥有者进一步访问配置文件
        例如，现在访问的是InstanceLabels的配置文件，在配置文件中寻找该"key"，
        若能找到则说明该label一个定制的label（但还需要验证label类型），
        进一步对比该label的类型和配置文件中的value_type，若符合，则确定这是一个定制的label；若不符合，则引发TypeError
        
        若配置文件中有"key"则该label做为一个定制的label创建出来，若没有则作为FreeLabel创建出来。
        进一步，调用init方法应在子类中进行。因为我们并不需要创建一个Labels类。
        """

        """
        如果是一个定制的label的话，它的value可能存在一些要求：比如，性别"男"或"女"或"未知"，这些是否也需要检验？
        还是说从前端输入的时候已经限制死了，保证不会出现错误？
        
        网络传输造成的信息不一致，如何检验？
        """
        if "key" in info.keys():
            #读取label的配置文件
            sys_config = read_config()
            find_flag = False
            #遍历配置文件，匹配key和value的取值，如果没有对应key则当作FreeLabel创建
            for labels_owner in sys_config:
                for label_config in sys_config[labels_owner]:
                    if info["key"] == label_config["key"]:
                        self.key = info["key"]
                        label_desc = label_config
                        find_flag = True
                        break
                if find_flag is True:
                    if not info["value"] == label_desc["value_type"]:
                        raise ValueError
                    else:
                        #此时已确定，label是一个定制的标签。
                        self.value = info["value"]
                        self.config = label_desc
            #该label是一个普通的Label
            if find_flag is False:
                self.key = info["key"]
                self.value = info["value"]
                if "config" in info:
                    self.config = info["config"]

        #public : owner_obj
        self.owner_obj = self.owner.owner

        #同步操作
        if sync is False:
            """
            与所属labels创建单向联系（如果该label有owner的话）
            只在该label中定义他所在的labels
            """
            pass
        else:
            """
            与所属labels创建双向联系（如果该label有owner的话）
            不仅需要在该labels中定义他所在的labels
            还需要更新labels中的该label(若没有则添加)
            """
            pass

        # private: value，为什么要存一个私有的value
        # self._value = copy.copy(self.empty_value)
        # if value is not None:
        #     self.value = value
        #     "这里将调用子类中定义的value的setter，将包含同步功能如果需要的话。"

    #同instance的疑问，不需要比较type了吗？下面我写的代码等同于不比较type...
    def __eq__(self, other):
        if isinstance(LabelType, other):
            if type(other) == type(self) and other.config == self.config and other.owner == self.owner \
                    and other.key == self.key and other.value == self.value:
                return True
            else:
                return False
        elif isinstance(dict, other):
            if other["config"] == self.config and other["owner"] == self.owner and other["key"] == self.key \
                    and other["value"] == self.value:
                return True
            else:
                return False
        else:
            raise TypeError

    # public: config

    """
    这样的话，label必须得有owner，如果是一个新创建的Freelabel呢？
    """
    @property
    def config(self) -> Dict:
        """
        The config dict of this label according to config_label_sys.json.

        :return: The config dict of this label according to config_label_sys.json.
        """
        return self.owner_labels.config[self.key]

    # public: owner_labels
    @property
    def owner_labels(self) -> Labels:
        return self.owner

    #这个指向的是某个instance对象
    # public: owner_obj
    @property
    def owner_obj(self) -> Union[Instance, NodeTree]:
        return self.owner.owner

    # public: value
    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, value):
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

    """
    导出info
    """
    def to_info(self) -> Dict:
        info = {}
        info["config"] = self.config
        info["owner"] = self.owner
        info["key"] = self.key
        info["value"] = self.value
        return info

    def clear(self, sync=False) -> object:
        if sync is False:
            self.config = {}
            self.owner = None
            self.key = None
            self.value = None
            return self
        else:
            #同步修改Labels中的该label
            pass

    def set_value(self, value, info, sync=False) -> object:
        if value is not None:
            #简单情况，value是自定义列表对象。理解为这种：
            """
            "value_option": [["yes", "true"], ["no", "false"]]
            """
            self.value = value
        if info is not None:
            #复杂情况，info是python原生列表对象。理解为这种：
            """
            "value_default": {
                "id": "",
                "desc": ""
             }
            """
            pass
        return self

    @classmethod
    def from_info(cls, key, value_info, root_node, instance_pool):
        return cls(owner=None, key=key, value=value_info)

    def ajax_process(self, ajax_param, root_node, instance_pool):
        pass

# FreeLabel类
class LabelTypeFree(LabelType):

    def __init__(self, info, objs_dict: Optional[dict] = None, sync: bool = False):
        # public
        self.empty_value = None
        #FreeLabel无需检验配置文件
        self._value = info["value"]
        #
        super().__init__(info, objs_dict=None, sync=False)

    #这两个方法 如果每个子类都要的话可否放入TypeLabel父类中？
    def set_link_require(self, from_labels, key):
        """

        Args:
            from_labels: 建立联系的labels对象
            key: 指向标签

        Returns: True or False

        """
        pass

    def del_link_require(self, from_labels, key):
        """

        Args:
            from_labels: 删除联系的labels对象
            key: 指向标签

        Returns: True or False

        """
        pass

#暂时只改了一个LabelTypeRadio类，如果没问题，其他类也采用类似方法
class LabelTypeRadio(LabelType):
    #这里的info含value
    def __init__(self, info, objs_dict=None, sync: bool = False):
        # public
        self.empty_value = None
        #子类中检验value类型
        if not isinstance(info["value"], self.config[self.key]["value_type"]):
            raise TypeError
        self._value = info["value"]
        #
        super().__init__(info, objs_dict=None, sync=None)

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
        super().__init__(owner, key, value)

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
        # public: empty_value
        self.empty_value = None
        #
        super().__init__(owner, key, value)

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
        # public: empty_value
        self.empty_value = []
        #
        super().__init__(owner, key, value)

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
        # public: empty_value
        self.empty_value = None
        #
        super().__init__(owner, key, value)


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
        # public: empty_value
        self.empty_value = None
        #
        super().__init__(owner, key, value)


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
        super().__init__(owner, key, value)

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
            new_value = copy.copy(self.empty_value)
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
        self._value = copy.copy(self.empty_value)

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

    @classmethod
    def from_info(cls, key, value_info, root_node, instance_pool):
        return cls(owner=None, key=key, value=root_node[value_info])

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
        if (not isinstance(value, Instance)) and (value is not None):
            raise TypeError
        # public: empty_value
        self.empty_value = None
        #
        super().__init__(owner, key, value)

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
            new_value = copy.copy(self.empty_value)
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
            linked_obj = self._value
            linked_label_key = self.config["linkto"]
            # 如果linked_label还没创建，那要先初始化一个空label给他
            if linked_label_key not in linked_obj.labels:
                from nlp_plantform.center.labeltypes import labeltypes
                linked_label_class = labeltypes[linked_obj.labels.config[linked_label_key]["value_type"]]
                linked_label_value = linked_label_class(owner=linked_obj.labels, key=linked_label_key, value=None)
                self._value.labels[self.config["linkto"]] = linked_label_value
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
        self._value = copy.copy(self.empty_value)

    def sync_add(self, value: Instance) -> None:
        # param check
        from nlp_plantform.center.instance import Instance
        if not isinstance(value, Instance):
            raise TypeError("param 'value' should be a Instance obj")
        #
        self._value = value

    def readable(self):
        if self.value == self.empty_value:
            return None
        else:
            return  self.value.readable(nolink=True)

    @classmethod
    def from_info(cls, key, value_info, root_node, instance_pool):
        return cls(owner=None, key=key, value=instance_pool.get_instance({"id": value_info}))

    from nlp_plantform.center.nodetree import NodeTree
    from nlp_plantform.center.instancepool import InstancePool

    def ajax_process(self,
                     ajax_param: str,
                     root_node: NodeTree = None,
                     instance_pool: InstancePool = None):
        """
        This function process ajax require which try to change the label value.

        :param ajax_param: The relative params in ajax require. There are 2 kinds of param supported:
            1. String "": means this label is to be delete( because null and undefined in js convert into "" in python).
            2. String "32": A integer string means the new label value is a instance with id of this integer.
        :param root_node: root node of all the node.
        :param instance_pool: instance pool that manages all the instance.
        :return: True if process is success, a string describe the error if process is failed
        """
        #param check
        if not isinstance(ajax_param, str):
            raise TypeError
        #
        if ajax_param is "":
            self.value_empty()
            del self.owner_labels[self.config["key"]]
            return True
        elif ajax_param.isdigit():
            new_instance = instance_pool.get_instance({"id": ajax_param})[0]
            self.value = new_instance
            return True
        else:
            raise TypeError


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
        # public: empty_value
        from nlp_plantform.center.nodetree import NodeTree
        self.empty_value = AutoSyncList(owner=self, init_value=[], type_limit=NodeTree)
        #
        super().__init__(owner, key, value)

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
            new_value = copy.copy(self.empty_value)
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
        return self._value.readable()

    def ajax_process(self, ajax_param, root_node, instance_pool):
        ajax_param = eval(ajax_param)
        action = ajax_param["action"]
        target_obj_index = ajax_param["targetObjIndex"]
        target_obj = self.value
        for i in target_obj_index:
            target_obj = target_obj[i]
        # append操作
        if action == 'append':
            child = ajax_param["child"]
            # append一个空list
            if child == "newList":
                target_obj.append(AutoSyncList(owner=target_obj))
            # append一个node
            else:
                from nlp_plantform.center.nodetree import NodeTree
                child_node_position =  NodeTree.str_to_position(child)
                child_node = root_node[child_node_position]
                # 如果node已经在label的value中了，那么不让重复添加
                def flat(l):
                    for k in l:
                        if not isinstance(k, AutoSyncList):
                            yield k
                        else:
                            yield from flat(k)
                flatted = list(flat(self.value))
                if child_node in flatted:
                    return "can not append a obj which already in label value."
                else:
                    target_obj.append(child_node)
        # del操作
        elif action == 'del':
            # 获得target_obj是它父亲的第几个孩子
            childe_index = target_obj_index[-1]
            # 获得target_obj的父亲
            parent_obj = self.value
            for i in target_obj_index[:-1]:
                parent_obj = parent_obj[i]
            # del一个AutoSyncList
            if isinstance(target_obj, AutoSyncList):
                target_obj.clear()  # 通过clear提供同步功能
                del parent_obj[childe_index]
            # del一个node
            else:
                linked_obj = target_obj
                linked_key = self.config["linkto"]
                linked_obj.labels[linked_key].sync_del(self.owner_obj)
                del parent_obj[childe_index]


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
