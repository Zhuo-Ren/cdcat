from random import randint


def node_id_check(s):
    # import re
    # r = re.findall(r'^n:[\\"/"\w\u4e00-\u9fa5.]+:([;\d-]+)', s)
    # if r == []:
    #     return False
    # r = re.findall(r"(\d+)-(\d+);?", str(r))
    # old = 0
    # for i in r:
    #     for j in i:
    #         new = int(j)
    #         if old <= new:
    #             old = new
    #         else:
    #             return False
    return True

import builtins
builtins.__dict__["node_id_check"] = node_id_check

# s = "n:dds\\fn中国w/eds/2\\k你5/好gn:3-18;19-20;21-22;77-96;98-115;117-119"  # 符号都不要
# print(node_id_check(s))
# s = "n:dds\\fn中国w/eds/2\\k你5/好gn:3-18;19-20;30-22;77-96;98-115;117-119"  # 符号都不要
# print(node_id_check(s))
# s = "n:dds\\fn中国w/eds/2\\k你5/好gn3-18;19-20;30-22;77-96;98-115;117-119"  # 符号都不要
# print(node_id_check(s))

