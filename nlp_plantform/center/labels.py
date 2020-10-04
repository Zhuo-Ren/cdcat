from typing import Dict, List, Tuple, Union  # for type hinting


class Labels(dict):
    # statistic: config
    config = {}

    # statistic: type
    owner_type_str = ""

    # statistic: type_class
    owner_type_class = None

    def __init__(self, owner: owner_type_class, labels_dict: Dict = {}):
        """
        Init a labels obj.

        :param owner: The node is the owner of the labels.
          The labels obj need knows it owner when edit a linked label such as a_node.labels["instance"] ---
          a_instance.labels["mentionList"]

        :param labels_dict: Value of labels.
          Only the one who follows the config in config_label_sys.json will be accept, or the default value will be
          used.
        """
        # param check: owner
        if not isinstance(owner, self.owner_type_class):
            raise TypeError

        # param check: labels_dict
        if not isinstance(labels_dict, dict):
            raise TypeError

        # private: owner
        self.owner = owner

        # private: owner_obj
        self.owner_obj = owner

        # add label
        for cur_label_key, cur_label_value in labels_dict.items():
            self[cur_label_key] = cur_label_value

    def __setitem__(self, key, value):
        # param check (如果这个label是定制label，那么需要验证一下)
        from nlp_plantform.center.labeltypes import labeltypes
        if key in labeltypes:
            # 这是一个订制类型的的label
            if isinstance(value, labeltypes[self.config[key]["value_type"]]):
                raise TypeError
            if value.owner != self:
                raise RuntimeError
            if value.key != key:
                raise RuntimeError
        # destruct old value
        if key in self:
            del self[key]  # this command call self.__delitem__(self, key) which will sync the old value.
        # add new value
        dict.__setitem__(self, key, value)  # sync of new value is done by the __init__ of the value.

    def __delitem__(self, key):
        from nlp_plantform.center.labeltypes import labeltypes
        if key in labeltypes:
            self[key].value_empty()
        super().__delitem__(key)

    def clear(self):
        for cur_label_key, cur_label_value in self:
            del self[cur_label_key]  # 触发__delitem__()，实现同步

    def update(self, new_labels_dict: Dict):
        # param check: new_labels_dict
        if not isinstance(new_labels_dict, dict):
            raise TypeError
        #
        for new_label_key, new_label_value in new_labels_dict.items():
            self[new_label_key] = new_label_value

    def pop(self, key):
        old_label_value = self[key]
        del self[key]
        return old_label_value

    def popitem(self) -> Tuple:
        raise RuntimeError("这个方法不让用了。")

    def readable(self, nolink=False):
        info_dict = {}
        if nolink == False:
            for (label_key, label_config) in self.config.items():
                if label_key in self:
                    info_dict.update({label_key: self[label_key].readable()})
        else:
            for (label_key, label_config) in self.config.items():
                if "linkto" not in label_config:
                    info_dict.update({label_key: self[label_key].readable()})
        return info_dict

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
    config = {}

