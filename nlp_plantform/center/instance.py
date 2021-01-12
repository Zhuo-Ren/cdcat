from typing import Dict, List, Tuple, Union, Optional  # for type hinting

class Instance(object):
    def __init__(self,
                 info: Optional[dict] = None, objs_dict: Optional[dict] = None,
                 load_label: bool = None, sync: bool = None):
        """

        :param info: the information of initialize instance object, and its labels param is simple describe
        :param objs_dict: the information of initialize instance object, and its labels param is labels object
        :param load_label: whether to load labels
        :param sync: whether to synchronize
        """
        # param check: info
        """
        查一下为什么{}不可变。
        默认值在函数默认定义时计算（通常是加载模块的时候），因此默认值成了函数的属性，
        所以，初始化类对象的时候，只要默认值是可变对象，并且未传入这个参数，这个类的这个参数，就会指向函数给默认值开辟的空间
        比如：函数的功能是在列表中添加一个"1"，不传入参数，直接调用会在默认空间中的对应列表添加"1"，
        但是当我们指定一个新的列表【11，12，】时，它会直接指向这个列表，再添加"1"，此时参数指向的列表发生了变化！！
        
        为了防止这种情况发生：
        
        如果定义函数接受可变参数时，应该考虑是否期望修改传入的参数
        
        对于可变参数，确认未传入时，要为对象新建参数（例如，{},[]），如果希望修改传入的参数，则直接赋值(self.a = a)
        否则，赋值为参数的副本（self.a = list(a)）。
        
        当没有传入可变参数时，每次都新创建一个dict对象{}就可以防止可变参数了。
        """

        if info is None and objs_dict is None:
            info = {}  # 防止默认值为可变元素

        # param check: info and objs_dict can't be gave at the same time
        if (info is not None) and (objs_dict is not None):
            raise TypeError

        # param check: info
        if not isinstance(info, dict):
            raise TypeError

        # param check: objs_dict
        if not isinstance(objs_dict, dict):
            raise TypeError
        else:
            from nlp_plantform.center.labels import InstanceLabels
            if not isinstance(objs_dict["labels"], InstanceLabels):
                raise TypeError

        # param check: load_label
        if not isinstance(load_label, bool):
            raise TypeError

        # param sync
        if not isinstance(load_label, bool):
            raise TypeError

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
        初始化为None.
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
            else:
                raise TypeError

        # 2.
        if not load_label:
            self.labels = InstanceLabels(owner=self)

        # 3.sync直接在InstanceLabels中使用，有这个类的初始化完成
        else:
            # 多态1：没有传入info，但是传入了objs_dict
            if (info is None) and (isinstance(objs_dict, dict)):
                self.labels = InstanceLabels(owner=self, objs_dict=objs_dict["labels"], sync=sync)
            # 多态2:传入了info，没有传入objs_dict
            elif (isinstance(info, dict)) and (objs_dict is None):
                self.labels = InstanceLabels(owner=self, info=info["labels"], sync=sync)
            # 多态3:没有传入info也没有传入objs_dict
            else:
                self.labels = InstanceLabels(owner=self)

    def __eq__(self, other) -> bool:
        """
        Determine whether the info carried by the two Instance objects is consistent.
        Args:
            other: Compare object

        Returns: Whether the two objects are the same.

        """

        if not isinstance(other, Instance):
            raise TypeError
        else:
            return self.to_info() == other.to_info()

    def to_info(self, style: str = "value") -> Dict:
        """
        Convert Instance to info.
        Args:
            style: Flags that return information. If style is "value", it will return info of value;
                   if style is "id", it will return info of identity

        Returns: info of the instance

        """

        info = {}
        # info of identity
        if style == "id":
            info["id"] = self.id
        # info of value
        elif style == "value":
            info["id"] = self.id
            #原来为什么要注释掉下行,采用self.instance_pool.to_info()是否可行？
            info["instancepool"] = self.instance_pool
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
