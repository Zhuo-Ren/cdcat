from nlp_platform.center.config import data_path
from nlp_platform.plug_in.input.instances_from_pickle import input_instances_from_pickle


ip = input_instances_from_pickle(data_path + r"/instances.pkl")
info = ip.to_dict()

ip.format_print(info)


'''
#每个逗号后强制添加新行
pprint.pprint(info, width=1)
效果：
{0: {'desc': '埃航',
     'id': 0,
     'labels': {'mention_list': [(0,
                                  0,
                                  0),
                                 (0,
                                  3),
                                 (0,
                                  97),
                                 (1,
                                  309,
                                  0),
                                 (1,
                                  586,
                                  0)]}},
 1: {'desc': '埃航客机',
     'id': 1,
     'labels': {'mention_list': [(0,
                                  0,
                                  1),
                                 (0,
                                  4),
                                 (0,
                                  21),
                                 (0,
                                  72,
                                  0)]}}}
'''

"""
json的中文不被转义的方法。dumps函数中加入参数ensure_ascii=False即可
"""


"""
0: {
    "id": 0,
    "desc": "埃航",
    "labels": {
        "mention_list": [
            0-0-1-2-0,
            0-107
        ],
        "kg": xx,
    }
},
2: {
    "desc": "apple"
    "labels": {
        "freelabel1": info of this label,
        "freelabel2": info of this label,
        "token": info of this label,
        "type": info of this label
    }
}
"""