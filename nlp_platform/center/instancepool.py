from typing import Dict, List, Tuple, Union  # for type hinting
from nlp_platform.center.instance import Instance


class InstancePool(dict):
    def __init__(self):
        self.next_id : int = 0
        """
        The id of next instance in this instance pool. Id of instance start of 0. The latest instance id is self。next_id - 1
        """

        self.groups = ["group", None, [
            ["instances", "fixed", []],
            ["group", "GName", []]
        ]]

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
            l = len(instance.labels["mention_list"].value)
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

    """
    Getting info(type: dict) of an object of Instancepool
    """
    def to_info(self):
        info_dict = {}
        for key in self:
            info_dict.update({key: self[key].to_info()})
        return info_dict

    """
    Info(type: dict) to info(type: str) 
    """
    def info_to_str(self, info_dict: Dict = None):
        return str(info_dict)

    """
    Info(type: str) to a file
    """

    def info_to_file(self):
        info_dict = self.info_to_str(self.to_info())
        flag0 = False  # ','是否在[]内
        flag1 = False  # ','是否在()内
        s1 = ''
        with open('instancepool_test.txt', 'w')as f:
            for c in info_dict:
                if c is '{':
                    s1 += '\t'
                    f.write('{\n%s' % s1)
                elif c is '}':
                    s1 = s1[1:]
                    f.write('\n%s}' % s1)
                elif c is ' ':
                    pass
                elif c is '[':
                    s1 += '\t'
                    flag0 = True
                    f.write('[\n')
                elif c is ']':
                    flag0 = False
                    f.write('\n%s]' % s1)
                    s1 = s1[1:]
                elif c is '(':
                    flag1 = True
                    f.write('%s(' % s1)
                elif c is ')':
                    flag1 = False
                    f.write(')')
                elif c is ',':
                    if flag0 is True and flag1 is True:
                        f.write(c)
                    elif flag0 is True and flag1 is False:
                        f.write(',\n')
                    elif flag0 is False:
                        f.write(',\n%s' % s1)
                else:
                    f.write(c)
        f.close()