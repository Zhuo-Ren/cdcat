from typing import Dict, List, Tuple, Union  # for type hinting
from nlp_plantform.center.instance import Instance

"""InstancePool的改进"""
class Instancepool(dict):
    def __init__(self, info=None, load_label=None, sync=None):
        if info is None :
            info={}
        if not isinstance(info, dict):
            raise TypeError("param info should be None or a dict.")
        self.next_id: int = 0
        self.groups = ["group", None, [["instances", "fixed", []],["group", "GName", []]]]

    def add_instance(self,new_instance)-> Instance:
        if not isinstance(new_instance,Instance):
            raise Exception("new_instance must be a Instance!")
        # update the new instance
        new_instance["id"] = self.next_id
        if new_instance["desc"] is None:
            new_instance["desc"] = new_instance["id"]
        new_instance.instance_pool = self
        # update the instance pool
        self[new_instance["id"]] = new_instance
        self.next_id += 1
        # 把新的实例放在fixed里面
        self.groups[2][0][2].append(new_instance)

        return new_instance

    def get_instance(self, info_dict)-> List[Instance]:
        """
        This is a polymorphic functions which accepts multiple kinds of input and search for eligible instance.

        :param info_dict:

        :return: a list of eligible instance
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

    def get_instance_by_id(self, id: Union[int, str])-> List[Instance]:
        """
        get_instance_by_id

        :param id:
        :return:  a list of eligible instance
        """
        if isinstance(id, str):
            id = int(id)
        if not isinstance(id, int):
            raise TypeError("id should be str or int")
        try:
            return [self[id]]
        except:
            return []

    def delete_instance(self,target_instance)-> List[Instance]:
        delete_list = self.get_instance(target_instance)
        if len(delete_list) == 1:
            return []
        else:
            pass


    def del_instancelink(self, instance_to_be_del):

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
        return self.todict == other.todict


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



