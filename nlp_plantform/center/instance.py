from typing import Dict, List, Tuple, Union  # for type hinting


class Instance(dict):
    def __init__(self, info=None, objs_dict=None, load_label=None, sync=None):  # 形参后面的冒号仅仅是一个注释作用
        # param check: info
        if info is None:     # 形参为空，则输出空字典
            info = {}  # 防止默认值为可变元素
        if not isinstance(info, dict):
            raise TypeError("param info should be None or a dict.")
        # public: instance_pool
        self.instance_pool = None
        """
        A instance must belong to, and only belong to, one instance pool. 
        The id of a new instance is given by the instance pool.
        """

        # public: id
        self["id"] = None
        """
        The id of this instance. Start from 0.
        """

        # public： desc
        self["desc"]: str = None
        if "desc" in info:
            self["desc"] = info["desc"]

        """
        The describe of this instance. Initial with "", not a None.
        """

        # private: _labels
        from nlp_plantform.center.labels import InstanceLabels
        if load_label is True:
            self._labels: InstanceLabels = InstanceLabels(owner=self, info=info["labels"], load_label=True)
        else:
            self._labels: InstanceLabels = InstanceLabels(owner=self)

        # instance能有什么需要同步的？如果instance对象加入了实例池，需要把instance_pool和id更新
        if sync is False:
            #建立单向关系
            if "instancepool" in info:
                #检验instancepool类型
                from nlp_plantform.center.instancepool import InstancePool
                if not isinstance(info["instancepool"], InstancePool):
                    raise TypeError
                if not isinstance(info["id"], int):
                    raise  TypeError
                #因为id是instancepool赋予的，在instancepool赋予id的过程中存在自增，
                #如何保证此时给的id是正确的，以及后续instancepool加入instance不出现冲突
                self.instance_pool = info["instancepool"]
                self.id = info["id"]
        else:
            #建立双向联系，
            #将instance加入instancepool，并保持一致。
            #将instance和他所拥有的labels同步
            pass


    #判断两个Instance是否完全一致。
    #self.to_info() == other.to_info()即可？如果这样的话不需要比较type了吗？
    def __eq__(self, other):
        if isinstance(other, Instance):
            if type(other) == type(self) and other["id"] == self["id"] and other.instance_pool == self.instance_pool \
                    and other["desc"] == self["desc"] and other.labels == self._labels:
                return True
            else:
                return False
        else:
            if other["id"] == self["id"] and other["desc"] == self["desc"]:
                return True
            else:
                return False

    # public: labels
    @property
    def labels(self):
        return self._labels

    # public: labels
    @labels.setter
    def labels(self, labels_value):
        from nlp_plantform.center.labels import InstanceLabels
        # 析构旧label
        self._labels.clear()
        # 添加新label
        self._labels = InstanceLabels(owner=self, info=labels_value, load_label=True)

    def readable(self, nolink=False) -> dict:
        """
        This function returns a readable info dict of this instance.

        The word "readable" here means: If you print(a_instance) and get <__main__.Instance object at 0x00002CF4E6>,
        this is unreadable; if you print(a_instance.readable()) and get {"id": 23, "desc": "埃航", "token": True}, this is
        readable.

        The readable info dict includes two parts: "id" and other labels.

        example::
            > a_instance.readable()
            {"id": 23, "desc": "埃航", "token": True}

        :return: readable info dict of this instance.
        """
        if nolink == True:
            r = self._labels.readable(nolink=True)
        else:
            r = self._labels.readable()
        r["id"] = str(self["id"])
        r["desc"] = self["desc"]
        return r

    #将instance转换成info
    def to_info(self):
        #info里有什么：desc，labels
        #如果已经加入了实例池 那么需不需要导出id和instancepool？？？
        info = {}
        info["id"] = self.id
        info["instancepool"] = self.instance_pool
        info["desc"] = self["desc"]
        info["labels"] = self.labels
        return info
