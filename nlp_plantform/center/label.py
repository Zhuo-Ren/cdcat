from typing import Dict, List, Tuple, Union  # for type hinting
from nlp_plantform.center.labels import read_config

class Label(object):
    config = {}
    from nlp_plantform.center.labels import Labels
    owner = Labels

    def __init__(self, info: Dict = {}, objs_dict=None, sync=None):
        if "owner" in info.keys():
            from nlp_plantform.center.labels import Labels
            if not isinstance(info["owner"], Labels):
                raise TypeError
            else:
                self.owner = info["owner"]
        #如果info中含有key信息
        if "key" in info.keys():
            #读取label的配置文件
            sys_config = read_config()
            find_flag = False
            #遍历配置文件 匹配key,value的取值，如果没有对应key则当作自定义label创建
            for labels_owner in sys_config:#labels_owner:node, instance
                for label_config in sys_config[labels_owner]:# i = 0,1,2···
                    if info["key"] == label_config["key"]:
                        self.key = info["key"]
                        label_desc = label_config
                        find_flag = True
                        break
                if find_flag is True:
                    if not info["value"] == label_desc["value_type"]:
                        raise Exception("Value is wrong")
                    else:
                        self.value = info["value"]
                        self.config = label_desc
            if find_flag is False:
                self.key = info["key"]
                self.value = info["value"]
                if "config" in info:
                    self.config = info["config"]

        if sync is True:
            pass

    #此处self与dict的比较 没有考虑dict中没有某标签的情况。后续完善
    def __eq__(self, other):
        if isinstance(Label, other):
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

    #这地方有bug，如果新建的Label未指定owner，会指向Labels类：<class 'nlp_plantform.center.labels.Labels'>
    def to_info(self):
        info = {}
        info["config"] = self.config
        info["owner"] = self.owner
        info["key"] = self.key
        info["value"] = self.value
        return info

    def clear(self, sync=False):
        if sync is False:
            self.config = {}
            self.owner = None
            self.key = None
            self.value = None
            return self
        else:
            #同步修改Labels中的该label
            pass

    def set_value(self, value, info, sync=False):
        if value is not None:
            self.value = value
        if info is not None:
            #此处如何用info来初始化value，初始化成什么样子？？？
            pass
        return self




class FreeLable(Label):
    #config = {}
    def set_link_require(self, from_labels, key):
        pass
    def del_link_require(self, from_labels, key):
        pass

class RadioLabel(Label):
    #config
    def set_link_require(self, from_labels, key):
        pass
    def del_link_require(self, from_labels, key):
        pass

class CheckboxLabel(Label):
    #config
    def set_link_require(self, from_labels, key):
        pass
    def del_link_require(self, from_labels, key):
        pass

class TextinputLabel(Label):
    def set_link_require(self, from_labels, key):
        pass
    def del_link_require(self, from_labels, key):
        pass
