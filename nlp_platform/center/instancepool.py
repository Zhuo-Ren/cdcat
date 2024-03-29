from typing import Dict, List, Tuple, Union  # for type hinting
from nlp_platform.center.instance import Instance


class InstancePool(dict):
    def __init__(self, corpus=None, info=None):
        """
        init

        :param info: the information of initialize instance object, and its labels param is simple describe
        :type info:Dict
        """
        # param check: info
        if info is None:
            info = {} # 防止默认值为可变元素
        if not isinstance(info, dict):
            raise TypeError("param label_dict should be None or a dict.")

        # self.groups初始化
        self.groups = [
            "group", None, [
                ["instances", "fixed", []],
                ["group", "GName", []]
            ]
        ]
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

        # public: corpus
        self.corpus = corpus
        """
            指向Corpus对象
        """

        #
        for instance_info in info.values():
            i = Instance(info=instance_info, pool=self)

    def add(self, instance):
        # param check
        pass
        # 如果key重复，就报错
        pass
        #
        self[instance["id"]["value"]] = instance
        instance.pool = self
        self.add_instancelink(instance["id"]["value"])

    def get_instance(self, id):
        return [self[id]]


    def add_instancelink(self, i_id):
        self.groups[2][0][2].append(i_id)

    def del_instancelink(self, i_id):

        def del_instancelink_from(group_or_instances, i_id):
            if group_or_instances[0] == "group":
                group = group_or_instances
                for i in group[2]:
                    del_instancelink_from(i, i_id)
            elif group_or_instances[0] == "instances":
                instances = group_or_instances
                li = iter(instances[2])
                while True:
                    try:
                        i = next(li)
                        if i == i_id:
                            instances[2].remove(i)
                    except StopIteration:
                        break

        del_instancelink_from(self.groups, i_id)

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
                if c == '{':
                    s1 += '\t'
                    f.write('{\n%s' % s1)
                elif c == '}':
                    s1 = s1[1:]
                    f.write('\n%s}' % s1)
                elif c == ' ':
                    pass
                elif c == '[':
                    s1 += '\t'
                    flag0 = True
                    f.write('[\n')
                elif c == ']':
                    flag0 = False
                    f.write('\n%s]' % s1)
                    s1 = s1[1:]
                elif c == '(':
                    flag1 = True
                    f.write('%s(' % s1)
                elif c == ')':
                    flag1 = False
                    f.write(')')
                elif c == ',':
                    if flag0 is True and flag1 is True:
                        f.write(c)
                    elif flag0 is True and flag1 is False:
                        f.write(',\n')
                    elif flag0 is False:
                        f.write(',\n%s' % s1)
                else:
                    f.write(c)
        f.close()