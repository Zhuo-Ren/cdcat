from nlp_plantform.config import data_path
from nlp_plantform.center.instancepool import InstancePool
from nlp_plantform.plug_in.input.instances_from_pickle import input_instances_from_pickle


ip = input_instances_from_pickle(data_path + r"\instances.pkl")
info = ip.to_dict()
ip.format_print(info)
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