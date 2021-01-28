from typing import Dict, List, Tuple, Union, Optional  # for type hinting
from nlp_platform.center.instance import Instance
from nlp_platform.center.nodetree import NodeTree

#from nlp_plantform.center.labeltypes import regiest_cofigured_label_types


def read_config() -> Dict:
    """
    如果要使用cdcat，那么需要读取用户为cdcat所定制的label配置。
    :return: Return config dict.
    """
    from nlp_platform.plug_in.manual_annotation_tool.cdcat.config import label_sys_dict_path
    import json
    with open(label_sys_dict_path) as json_file:
        config = json.load(json_file)
    return config


class Labels(dict):
    # statistic: config
    config = {}

    # statistic: type
    owner_type_str = ""

    # statistic: owner_type_class
    owner_type_class = Instance, NodeTree

    #info : {'key1': xxx, 'key2':xxx, 'key3':qqq}
    # info value是python原生，简单类型；objs_dict是复杂类型
    #
    def __init__(self, info: Optional[dict] = None, objs_dict: Optional[dict] = None,
                 sync: bool = False):
        """
        Init a labels obj
        Args:
            info: the information of labels' init, and its label just is simple describe;
                  info includes owner and label
            objs_dict: the information of labels' init, and its label is label object
            sync: whether to synchronize
        """

        if info is None and objs_dict is None:
            # 防止默认值为可变元素
            info = {}

        # param check: info
        if not isinstance(info, dict):
            raise TypeError
        else:
            for cur_label_key, cur_label_value in info.items():
                if cur_label_key is "owner":
                    if not isinstance(cur_label_value, self.owner_type_class):
                        raise TypeError
                else:
                    if not isinstance(cur_label_value, dict):
                        raise TypeError

        # param check: objs_dict
        if objs_dict is not None:
            if not isinstance(objs_dict, dict):
                raise TypeError
            else:
                from nlp_platform.center.labeltypes import LabelType
                for cur_label_key, cur_label_value in objs_dict.items():
                    if cur_label_key is "owner":
                        if not isinstance(cur_label_value, self.owner_type_class):
                            raise TypeError
                    else:
                        if not isinstance(cur_label_value, LabelType):
                            raise TypeError

        # param check: sync
        if not isinstance(sync, bool):
            raise TypeError

        # public: config
        self.config = read_config()

        # public: owner, owner_obj
        self.owner = None
        self.owner_obj = None

        # public: label
        # 多态1: 传入info，没有传入objs_dict
        if info is not None and objs_dict is None:
            # public: owner and owner_obj
            if "owner" in info.keys():
                self.owner = info["owner"]
                self.owner_obj = info["owner"]
                del info["owner"]

            # public: label
            for cur_label_key, cur_label_value in info.items():
                if cur_label_key in self.config:# 这个地方有待考究
                    from nlp_platform.center.labeltypes import labeltypes
                    new_label = labeltypes[cur_label_key].__init__(info=cur_label_value,
                                                                   objs_dict=None, sync=sync)
                    self[cur_label_key] = new_label
                else:
                    from nlp_platform.center.labeltypes import LabelTypeFree
                    new_label = LabelTypeFree(info=cur_label_value, objs_dict=None, sync=sync)
                    self[cur_label_key] = new_label

        # 多态2: 没有传入info，传入objs_dict
        elif info is None and objs_dict is not None:
            if "owner" in objs_dict.keys():
                self.owner = objs_dict["owner"]
                self.owner_obj = objs_dict["owner"]
                del objs_dict["owner"]
            for cur_label_key, cur_label_value in objs_dict.items():
                self[cur_label_key] = cur_label_value
        # 多态3：既没有传入info，也没有传入obj_dict,此时info={}，不为空直接在多态1中实现 这个多态3还可以用来干嘛？预留。
        else:
            pass




    def __setitem__(self, key, value):
        # param check: key
        if not isinstance(key, str):
            raise TypeError

        # param check: value
        from nlp_platform.center.labeltypes import LabelType
        if not isinstance(value, LabelType):
            raise TypeError

        # param check (如果这个label是定制label，那么需要验证一下)
        # 查询配置文件中有没有这个key对应的配置信息
        find_flag = False
        if isinstance(self.owner, Instance):
            str_owner = "instance"
        else:
            str_owner = "node"
        label_config = self.config[str_owner]
        for label_info in label_config:
            if label_info["key"] is key.to_info(style="name"):
                find_flag = True
                break
        if find_flag is True:
            #若查到了则对比该key对应的类型是否与labeltypes中存储的类型一致，若一致则是定制的label；若不一致，则报错
            from nlp_platform.center.labeltypes import labeltypes
            if not isinstance(value, labeltypes[label_info["value_type"]]):
                raise Exception("key和value不对应配置文件")
            if value.owner != self:
                raise RuntimeError
            if value.key != key:
                raise RuntimeError
        else:
            #这是一个FreeLabel
            from nlp_platform.center.labeltypes import LabelTypeFree
            if not isinstance(value, LabelTypeFree):
                raise TypeError

        # destruct old value
        if key in self:
            del self[key]  # this command call self.__delitem__(self, key) which will sync the old value.
        # add new value
        dict.__setitem__(self, key, value)  # sync of new value is done by the __init__ of the value.

    def __delitem__(self, key):
        from nlp_platform.center.labeltypes import labeltypes
        if key in self.config:
            self[key].value_empty() # 同步要显式实现
        super().__delitem__(key)

# labels的sync的区别

    def clear(self, sync=False) -> Dict:
        if sync is True: # 实现同步需要一个含有sync的函数来实现
            for cur_label_key in list(self.keys()):
                del self[cur_label_key]
                # 触发__delitem__()，实现同步 不仅在labels中删除了该label，
                # 并且还调用了label中的方法，将该label的value置空
        else:
            for cur_label_key in list(self.keys()):
                # cur_label_key.own_obj = None
                super().pop(cur_label_key) # 使用父类的pop方法，不同步
            return self

    def update(self, v, sync=False) -> Dict:
        '''
        更新labels中的一些label
        Args:
            v: Label information that needs to be updated
            sync: whether to synchronize
        '''
        # param check: v
        if not isinstance(v, dict):
            raise TypeError
        # param check: sync
        if not isinstance(sync, bool):
            raise TypeError
        # update the label of labels
        # sync需要显式传递
        if sync is False:
            for new_label_key, new_label_value in v.items():
                self[new_label_key] = new_label_value
        else:
            for new_label_key, new_label_value in v.items():
                # 在此处调用label的子类更新方法，传sync=True把label也更新
                self[new_label_key] = new_label_value

    def pop(self, key) -> str:
        old_label_value = self[key]
        del self[key]
        return old_label_value

    def popitem(self) -> Tuple:
        raise RuntimeError("这个方法不让用了。")

    def readable(self, nolink=False) -> Dict:
        info_dict = {}
        for (cur_label_key, cur_label_value) in self.items():
            # 定制标签
            if cur_label_key in self.config.keys():
                if nolink == False:
                    info_dict.update({cur_label_key: cur_label_value.readable()})
                elif nolink == True:
                    if "linkto" not in self.config[cur_label_key]:
                        info_dict.update({cur_label_key: cur_label_value.readable()})
            # 非定制标签
            else:
                info_dict.update({cur_label_key: cur_label_value})
        return info_dict

# dict 可能会报错 测试一下
    def to_info(self) -> Dict:
        """

        Returns: info of the labels

        """
        info_dict = {}
        #owner不需要比较吗？
        for (cur_label_key, cur_label_value) in self.items():
            # 定制标签
            if cur_label_key in self.config.keys():
                info_dict.update({cur_label_key: cur_label_value.to_info()})
            # 非定制标签
            else:
                info_dict.update({cur_label_key: cur_label_value})
        return info_dict

# 信息转成对象
    def from_info(self, info_dict, root_node=None, instance_pool=None):
        for (cur_label_key, cur_label_value) in info_dict.items():
            # 定制标签
            if cur_label_key in self.config.keys():
                info_dict.update({cur_label_key: cur_label_value.from_info()})
            # 非定制标签
            else:
                info_dict.update({cur_label_key: cur_label_value})

    # def __str__(self) -> str:
    #     output_dict = {}
    #     for cur_label_key in self.keys():
    #         output_dict.update({cur_label_key: self[cur_label_key].readable()})
    #     return str(output_dict)


class InstanceLabels(Labels):
    # static
    owner_type_str = "instance"

    # static
    from nlp_platform.center.instance import Instance
    owner_type_class = Instance

    # static: config
    config = {}

    def __init__(self, info: Optional[dict] = None, objs_dict: Optional[dict] = None,
                 sync: bool = False):
        super().__init__(info, objs_dict)

        #sync


class NodeLabels(Labels):
    # static: type
    owner_type_str = "node"

    # static
    from nlp_platform.center.nodetree import NodeTree
    owner_type_class = NodeTree

    # static: config
    #
    config = {}

    def __init__(self, info: Optional[dict] = None, objs_dict: Optional[dict] = None,
                 sync: bool = False):
        super().__init__(info, objs_dict)

        # sync