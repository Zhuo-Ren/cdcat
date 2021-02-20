from nlp_plantform.config import data_path
from nlp_plantform.center.instancepool import InstancePool
import _pickle as cPickle
from nlp_plantform.plug_in.manual_annotation_tool.cdcat.cdcat import cdcat


def input_instances_from_pickle(path: str = data_path + r'/instances.pkl') -> InstancePool:
    with open(path, 'rb') as pkl_file:
        instances = cPickle.load(pkl_file)
    return instances


ip = input_instances_from_pickle(data_path + r"/instances.pkl")
print(ip.to_dict())

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