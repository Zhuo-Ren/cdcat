from typing import Dict, List, Tuple, Union  # for type hinting
from nlp_plantform.center.instance import Instance
from nlp_plantform.center.nodetree import NodeTree
from nlp_plantform.center.labeltypes import regiest_cofigured_label_types


def read_config() -> Dict:
    """
    如果要使用cdcat，那么需要读取用户为cdcat所定制的label配置。
    :return: Return config dict.
    """
    from nlp_plantform.plug_in.manual_annotation_tool.cdcat.config import label_sys_dict_path
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
    def __init__(self, owner: Union[Instance, NodeTree],
                 info: Dict = {}, objs_dict=None,
                 sync=None):
        """
        Init a labels obj.

        :param owner: The node is the owner of the labels.
          The labels obj need knows it owner when edit a linked label such as
          a_node.labels["instance"] --- a_instance.labels["mentionList"]

        :param labels_dict: Value of labels.
          All kinds of labels are allowed. Labels that register to
          config_label_sys.json are called "configured label", others are "free
          label".
        """

        # param check: owner
        if not isinstance(owner, self.owner_type_class):
            raise TypeError

        # param check: info
        if not isinstance(info, dict):
            raise TypeError

        # param check: objs_dict
        pass

        # public: owner
        self.owner = owner

        # public: owner_obj
        self.owner_obj = owner

        # public: config
        self.config = read_config()

        # add label
        for cur_label_key, cur_label_value in info.items():
            #检查cur_label_value类型是否正确
            from nlp_plantform.center.labeltypes import LabelType
            if isinstance(cur_label_value, LabelType):
                self[cur_label_key] = cur_label_value
            else:
                raise TypeError
        # add relationship with label
        if sync is False:
            """
            建立labels与instance，labels和label的单向联系
            """
            pass
        else:
            """
            建立labels与instance，labels和label的双向联系
            """
            pass

    #a_node.labels[key] = sss
    def __setitem__(self, key, value):
        # param check (如果这个label是定制label，那么需要验证一下)
        #查询配置文件中有没有这个key对应的配置信息
        find_flag = False
        for label_config in self.config:
            if label_config["key"] == key:
                find_flag = True
                label_desc = label_config
        if find_flag is True:
            #若查到了则对比该key对应的类型是否与labeltypes中存储的类型一致，若一致则是定制的label；若不一致，则报错
            from nlp_plantform.center.labeltypes import labeltypes
            # 测试这里的时候报错，是因为label类没有细分好,但是用这种方法匹配的话，__name__返回的是类名不是value_type。
            print(labeltypes[label_desc["value_type"]])
            if not isinstance(value, labeltypes[label_desc["value_type"]]):
                raise Exception("key和value不对应配置文件")
            if value.owner != self:
                raise RuntimeError
            if value.key != key:
                raise RuntimeError
            #若都通过则是一个定制的label
            self[key] = value
        else:
            #这是一个FreeLabel
            self[key] = value
            pass

        # destruct old value
        if key in self:
            del self[key]  # this command call self.__delitem__(self, key) which will sync the old value.
        # add new value
        dict.__setitem__(self, key, value)  # sync of new value is done by the __init__ of the value.

    def __delitem__(self, key):
        from nlp_plantform.center.labeltypes import labeltypes
        if key in self.config:
            self[key].value_empty()
        super().__delitem__(key)

    def clear(self, sync=False):
        if sync is True:
            for cur_label_key in list(self.keys()):
                del self[cur_label_key]  # 触发__delitem__()，实现同步
        else:
            #只清空labels，不同步
            pass

    def update(self, v, sync=False):
        # param check: v
        if not isinstance(v, dict):
            raise TypeError
        #
        for new_label_key, new_label_value in v.items():
            self[new_label_key] = new_label_value

    def pop(self, key):
        old_label_value = self[key]
        del self[key]
        return old_label_value

    def popitem(self) -> Tuple:
        raise RuntimeError("这个方法不让用了。")

    def readable(self, nolink=False):
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

    def to_info(self) -> dict:
        info_dict = {}
        for (cur_label_key, cur_label_value) in self.items():
            # 定制标签
            if cur_label_key in self.config.keys():
                info_dict.update({cur_label_key: cur_label_value.to_info()})
            # 非定制标签
            else:
                info_dict.update({cur_label_key: cur_label_value})
        return info_dict

    def from_dict(self, info_dict, root_node=None, instance_pool=None):
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
    from nlp_plantform.center.instance import Instance
    owner_type_class = Instance

    # static: config
    config = {}


class NodeLabels(Labels):
    # static: type
    owner_type_str = "node"

    # static
    from nlp_plantform.center.nodetree import NodeTree
    owner_type_class = NodeTree

    # static: config
    #
    config = {}
