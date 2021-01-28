from typing import Dict, List, Tuple, Union  # for type hinting
from nlp_plantform.center.instance import Instance


class InstancePool(dict):
    def __init__(self, info=None, load_label=None, sync=None):
        """
               :param info: the information of initialize instance object,
                            and its labels param is simple describe
               :type info:Dict

               :param load_label:whether to load labels
               :type load_label:bool = None

               :param sync: whether to synchronize
               :type sync: bool = None

        """

        # 防止默认值为可变元素
        if info is None :
            info={}

        # param check: info
        if info:
            pass;
        if not isinstance(info, dict):
            raise TypeError("param info should be None or a dict.")

        # public: next_id
        self.next_id: int = 0
        """
                The id of next instance in this instance pool. 
                Id of instance start of 0. 
                The latest instance id is self.next_id - 1

        """

        # public: groups
        self.groups = ["group", None, [["instances", "fixed", []],["group", "GName", []]]]
        """
               Organization strategy of instances.
               Compared with **InstancePool**, one instance can appear multi times in **groups**.
               **groups** is a nested list with element in the form of [TYPE, NAME, CHILDREN].
               There are two type of element: group and instances.
               A child of "group" can be "instances" and "group".
               A child of "instances" must be Instance object

               The NAME of root group will not be displayed in GUI.
               The first child of root group must be a instances which is used to receive new instance in GUI.

        """

    def add_instance(self,new_instance):
        """
            :param new_instance: the Instance to be added
            :type new_instance: nlp_platform.center.instance.Instance
            :return : the new Instance to be added
            :rtype:nlp_platform.center.instance.Instance
        """
        if not isinstance(new_instance,Instance):
            raise Exception("new_instance must be a Instance!")

        # 1.update the new instance
        new_instance.id = self.next_id
        if new_instance.desc is None:
            new_instance.desc = new_instance.id
        new_instance.instance_pool = self

        # 2.update the instance pool
        self.next_id += 1

        # 2.1 添加新实例
        self[new_instance.id] = new_instance

        # 2.2 添加新实例链接
        self.groups[2][0][2].append(new_instance)

        return new_instance

    def get_instance(self, info_dict):
        """
        This is a polymorphic functions which accepts multiple kinds of input and search for eligible instance.

        :param info_dict:multiple kinds of input
        :type info_dict:dict
        :return: a list of eligible Instance
        :rtype: List[Instance]
        """
        if "id" in info_dict:
            target_instance_list = self.get_instance_by_id(info_dict["id"])
            # 根据id找instance，只有找到1个才是正常
            if len(target_instance_list) == 1:
                # 验证其他属性是否符合
                pass
                #
                return target_instance_list
            # 根据id找instance，只有找到1个才是正常，其他直接返回空列表。
            else:
                return []
        else:
            raise RuntimeError("抱歉这个还没实现。")

    def get_instance_by_id(self, id):
        """
        get_instance_by_id

        :param id:the id of a Instance
        :type id: Union[int, str]
        :return:  a list of eligible instance
        :rtype: List[Instance]
        """
        if isinstance(id, str):
            id = int(id)
        if not isinstance(id, int):
            raise TypeError("id should be str or int")
        try:
            return [self[id]]
        except:
            return []

    def delete_instance(self,target_instance):
        """

        :param target_instance: the Instance to be deleted
        :type target_instance:nlp_platform.center.instance.Instance
        :return:  a list of eligible instance
        :rtype: List[Instance]
        """
        delete_list = self.get_instance(target_instance)
        if len(delete_list) == 1:
            return []
        else:
            pass

    def del_instancelink(self, instance_to_be_del):
        """
        :param instance_to_be_del: the Instance to be deleted
        :type instance_to_be_del:Instance
        :return: None
        """

        def del_instancelink_from(group_or_instances, instance_to_be_del):
            if group_or_instances[0] == "group":
                group = group_or_instances
                for i in group[2]:
                    del_instancelink_from(i, instance_to_be_del)
            elif group_or_instances[0] == "instances":
                instances = group_or_instances
                li = iter(instances[2])
                while True:
                    try:
                        i = next(li)
                        if i == instance_to_be_del:
                            instances[2].remove(i)
                    except StopIteration:
                        break

        del_instancelink_from(self.groups, instance_to_be_del)

    def __eq__(self, other):
        """
        :param other: the other Instance to check
        :type other: nlp_platform.center.instance.Instance
        :return: whether A equal to B
        :rtype:bool
        """
        return self.to_info() == other.to_info()

    def to_info(self):
        """
        get a type of info
        :return: info
        :rtype: Dict
        """
        info = {}
        info["desc"] = self.desc
        info["labels"] = self.labels
        return info

    def statistic(self, ifprint=False):

        """
        calc the statistic info.
        example of the statistic info dict::

            r = {
                "instance_num" : (int)how many instances.
                "0": (int) num of instances which have no mention.
                "1": (int) num of instances which have 1 mention.
                "2": (int) num of instances which have 2 mentions, which means the 2 mentions are co-reffed.
                ...
            }
        :param ifprint: whether print the result.
        :type ifprint:bool = False
        :return: A statistic info dict likes shown above.
        :rtype: Dict

        """
        temp = {}
        max = 0
        for instance in self.values():
            l = len(instance.labels["mention_list"].value)
            try:
                temp[l] += 1
            except:
                temp[l] = 1
            if l > max:
                max = l
        r = {}
        coref_num = 0
        for i in range(0, max + 1):
            try:
                r[i] = temp[i]
            except:
                r[i] = 0

            if ifprint == True:
                print("coreference chain with ", i, "mention(s):", r[i])
            if r[i] == 0:
                pass
            elif r[i] > 0:
                coref_num += (r[i] - 1)
        r["instance_num"] = len(self)

        if ifprint == True:
            print("instance_num: ", r["instance_num"])
        r["coref_num"] = coref_num
        if ifprint == True:
            print("coref_num: ", r["coref_num"])

        return r




"""
__init__()："info"，(类型是dict) load_label用于控制是否加入label，
sync控制同步操作，False时，直接建立单向关系。True时，则根据标签性质自动维系关系（如果A<->B ,但是C想要指向A，
此时根据标签性质自动维系：断开A<->B，建立A<->C关系；还是拒绝C的请求)。
add_instance()：将输入类型直接限制为Instance对象，如果传的参数不是Instance直接报错
添加instancelink指的是，位于GUI的group里的灰色实例块（但它并不是实例），它只是一个链接，可以在group出现多次。InstancePool中存放的才是实例。
remove_instance()：删除instancelink（删除instance时，必须删除与该instance相关的所有关系）
__eq__()：先将instancepool转换为xml。当我们使用该xml恢复instancepol后，用__eq__()来比较结构是否相同。（直接p1==p2仅能比较整体，却不能比较细节）
to_info()：将instancepool转换为info(dict)..object->info(大多数情况下是dict)->xml
to_xml !!!!!视频中有，文档里没有。

Class InstancePool(dict):
	self.next_id
	self.groups
	def __init__(self, info=None, load_label=None, sync=None):
		if 都没给
		if info
	def add_instance(new_instance)
		添加instancelink
	def remove_instance(target_instance)
		删除instancelink
	def __eq__()
	def to_info()

"""