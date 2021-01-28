from typing import Dict,Optional, List, Tuple, Union  # for type hinting


class Instance(dict):
    def __init__(self, info, objs_dict, load_label=None, sync=None):
        """
        Init of Instance obj.

        objs_dict优先级高于info.
        如果给了objs_dict,那么就不管info了。
        如果没给objs_dict，那么根据info来构造。
        如果俩都没给，就相当于不赋值。

        example::
            info = {
                "instance_pool_id": 9,  # pool没id，先不管
                "id": 9
                "desc": "apple"
                "labels": {
                    "freelabel1": info of this label,
                    "freelabel2": info of this label,
                    "token": info of this label,
                    "type": info of this label
                }
            }

        :param info: the information of initialize instance object, and its labels
            param is simple describe
        :type info: dict or None

        :param objs_dict: the information of initialize instance object,
            and its labels param is labels object
        :type objs_dict: dict or None

        :param load_label: whether to load labels
        :type load_label: bool

        :param sync: whether to synchronize
        :type sync: bool
        """
        # 防止默认值为可变元素
        if info is None and objs_dict is None:
            info = {}

        # param check: info
        if objs_dict is None and not isinstance(info, dict):
            raise TypeError("param info should be None or a dict.")

        # param check: objs_dict
        if objs_dict is not None and not isinstance(objs_dict, dict):
            raise TypeError
        if isinstance(objs_dict, dict) and "labels" in objs_dict:
            from nlp_platform.center.labels import InstanceLabels
            if not isinstance(objs_dict["labels"], InstanceLabels):
                raise TypeError

        # param check: sync
        if not isinstance(sync, bool):
            raise TypeError

        # public: instance_pool
        self.instance_pool = None
        """ 
        The instance pool that this instance belong to.
        
        A instance must belong to, and only belong to, one instance pool.
        初始化为None.
        当instance被添加到pool后获得此值。
        
        :type instance_pool: nlp_platform.center.instancepool.InstancePool
        """

        # public: id
        self.id = None
        """
        The id of this instance. Start from 0.
        
        The id of a new instance is given by the instance pool.
        
        :type id: int or None
        """

        # public: desc
        self.desc: Optional[str] = None
        """
        The describe of this instance. Initial with "", not a None.
        """

        # private: labels
        self.labels = None
        """加注释"""

        # 多态1: 只要传入objs_dict，就是用objs_dict,不管info
        if objs_dict is not None:
            pass

        # 多态2: 没有传入objs_dict，则使用info，
        if info is not None and objs_dict is None:
            pass

        """下面那些逻辑没有整合啊"""
        if "desc" in info:
            if isinstance(info["desc"], str):
                self.desc = info["desc"]
            else:
                raise TypeError

        # 2
        if not load_label:
            self.labels = InstanceLabels(owner=self)

        # 3.sync直接在InstanceLabels中使用，有这个类的初始化完成
        else:
            # 多态1：没有传入info，但是传入了objs_dict
            if (info is None) and (isinstance(objs_dict, dict)):
                self.labels = InstanceLabels(owner=self, objs_dict=objs_dict["labels"],
                                             sync=sync)
            # 多态2:传入了info，没有传入objs_dict
            elif (isinstance(info, dict)) and (objs_dict is None):
                self.labels = InstanceLabels(owner=self, info=info["labels"], sync=sync)
            # 多态3：同时传入了info和objs_dict，objs_dict优先
            elif (isinstance(info, dict)) and (isinstance(objs_dict, dict)):
                self.labels = InstanceLabels(owner=self, objs_dict=objs_dict["labels"],
                                             sync=sync)
            # 多态4:没有传入info也没有传入objs_dict
            else:
                self.labels = InstanceLabels(owner=self)

    # 判断两个Instance是否完全一致。
    def __eq__(self, other):
        """
        Determine whether the info carried by the two Instance objects is consistent.

        :param other: the other Instance to check
        :type other: nlp_platform.center.instance.Instance
        :return: whether a equal to b.
        :rtype: bool
        """
        if type(other) == type(self):
            if self.to_info() == other.to_info():
                return True
        return False

    def to_info(self):
        """
        returns info of this instance.

        example::
            >>> a_instance.to_info()
            参见__init__()中的注释

        :return: info
        :rtype: dict
        """
        info = {}
        info["desc"] = self["desc"]
        info["labels"] = self.labels
        return info

