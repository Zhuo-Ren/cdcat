from nlp_plantform.config import data_path
from nlp_plantform.center.instancepool import InstancePool
import _pickle as cPickle
from nlp_plantform.plug_in.manual_annotation_tool.cdcat.cdcat import cdcat

def input_instances_from_pickle(path: str = data_path + r'/instances.pkl') -> InstancePool:
    with open(path, 'rb') as pkl_file:
        instances = cPickle.load(pkl_file)
    return instances

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