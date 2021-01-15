from typing import Dict,Optional, List, Tuple, Union  # for type hinting


class Instance(dict):
    def __init__(self, info: Optional[Dict] = None, objs_dict: Optional[Dict] = None,
                 load_label: bool = None, sync: bool = None):

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

                :param info: the information of initialize instance object,
                            and its labels param is simple describe

                :param objs_dict: the information of initialize instance object,
                                    and its labels param is labels object

                :param load_label: whether to load labels

                :param sync: whether to synchronize

                """

        # 防止默认值为可变元素
        if info is None and objs_dict is None:
            info = {}

        # param check: info
        if objs_dict is None and not isinstance(info, dict):
            raise TypeError("param info should be None or a dict.")

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

        # param check: objs_dict
        if not isinstance(objs_dict, dict):
            raise TypeError
        else:
            from nlp_plantform.center.labels import InstanceLabels
            if not isinstance(objs_dict["labels"], InstanceLabels):
                raise TypeError

        # param check: sync
        if not isinstance(sync, bool):
            raise TypeError

        # public: instance_pool
        from nlp_plantform.center.instancepool import InstancePool
        self.instance_pool: Optional[InstancePool] = None

        """
        A instance must belong to, and only belong to, one instance pool. 

        The id of a new instance is given by the instance pool.

        初始化为None.

        当instance被添加到pool后获得此值。
        """

        # public: id
        self.id = None
        """
        The id of this instance. Start from 0.
        """

        # public： desc
        self.desc: Optional[str] = None
        """
        The describe of this instance. Initial with "", not a None.
        """

        # private: _labels
        from nlp_plantform.center.labels import InstanceLabels
        self._labels: Optional[InstanceLabels] = None

        # 多态1: 只要传入objs_dict，就是用objs_dict,不管info
        if objs_dict is not None:
            pass

        # 多态2: 没有传入objs_dict，则使用info，
        if info is not None and objs_dict is None:
            pass

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
        self._labels = InstanceLabels(owner=self, labels_value=labels_value)

    # 判断两个Instance是否完全一致。
    def __eq__(self, other) -> bool:

        """
        Determine whether the info carried by the two Instance objects is consistent.
        :param other:
        :return:
        """
        # if isinstance(other, Instance):
        #     if type(other) == type(self) and other["id"] == self[
        #         "id"] and other.instance_pool == self.instance_pool \
        #             and other["desc"] == self["desc"] and other.labels == self._labels:
        #         return True
        #     else:
        #         return False
        # else:
        #     if other["id"] == self["id"] and other["desc"] == self["desc"]:
        #         return True
        #     else:
        #         return False

        if type(other) == type(self):
            if self.to_info() == other.to_info():
                return True
        return False

    def to_info(self) -> dict:
        info = {}
        info["desc"] = self["desc"]
        info["labels"] = self.labels
        return info

