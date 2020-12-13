from typing import Dict, List, Tuple, Union, Optional  # for type hinting

class Instance(object):
    def __init__(self,
                 info: Optional[dict] = None, objs_dict: Optional[dict] = None,
                 load_label: bool = None, sync: bool = None):
        """

        :param info:
        :param objs_dict:
        :param load_label:
        :param sync:
        """
        # param check: info
        if info is None and objs_dict is None:
            info = {}  # 防止默认值为可变元素

        # param check: objs_dict
        pass

        # param check: load_label
        pass

        # param sync
        pass

        # public: id
        self.id: Optional[int] = None
        """ 
        The id of this instance. 
        初始化为None，
        当instance被添加到pool后获得此值。id自增，从0开始。
        """

        # public: instance_pool
        from nlp_plantform.center.instancepool import InstancePool
        self.instance_pool: Optional[InstancePool] = None
        """
        A instance must belong to, and only belong to, one instance pool. 
        初始化为0.
        当instance被添加到pool后获得此值。
        """

        # public： desc
        self.desc: str = ""
        """
        The description of this instance. 
        Initial with ""
        """

        # public: labels
        from nlp_plantform.center.labels import InstanceLabels
        self.labels: InstancePool = None
        """
        Labels of the instance.
        """

        # 1.
        if "desc" in info:
            if isinstance(info["desc"], str):
                self["desc"] = info["desc"]

        # 2.
        if not load_label:
            self.labels = InstanceLabels(owner=self)

        # 3.
        if 1:
            # 多态1
            if (info is None) and (isinstance(objs_dict, dict)):
                self.labels  = InstanceLabels(owner=self, objs_dict=objs_dict["labels"], load_label=True, sync=sync)
            # 多态2
            elif (isinstance(objs_dict, dict)) and (info is None):
                self.labels  = InstanceLabels(owner=self, info=info["labels"], load_label=True, sync=sync)
            # 多态3
            else:
                pass

    def __eq__(self, other):
        """
        判断两个Instance对象所承载的信息是否一致。
        """
        if not isinstance(other, Instance):
            pass  # 报错
        else:
            return self.to_info() == other.to_info()

    def to_info(self, style: str = "value") -> Dict :
        """
        将instance转换成info
        """
        info = {}
        if style == "id":
            info["id"] = self.id
        elif style == "value":
            info["id"] = self.id
            # info["instancepool"] = self.instance_pool
            info["desc"] = self["desc"]
            info["labels"] = self.labels.to_info()
        else:
            pass
        return info

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
