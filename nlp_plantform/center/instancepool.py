from typing import Dict, List, Tuple, Union  # for type hinting
from nlp_plantform.center.instance import Instance


class InstancePool(dict):
    def __init__(self):
        self.next_id : int = 0
        """
        The id of next instance in this instance pool. Id of instance start of 0. The latest instance id is self。next_id - 1
        """

    def add_instance(self, info_dict=None):
        new_instance = Instance(instance_pool=self, labels_dict=info_dict)
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

    def statistic(self, ifprint=False) -> Dict:
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
        :return: A statistic info dict likes shown above.
        """
        temp = {}
        max = 0
        for instance in self.values():
            l = len(instance["mention_list"])
            try:
                temp[l] += 1
            except:
                temp[l] = 1
            if l > max:
                max = l

        r = {}
        coref_num = 0
        for i in range(0, max+1):
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
