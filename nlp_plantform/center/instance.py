from typing import Dict, List, Tuple, Union  # for type hinting
from nlp_plantform.center.mytree import mytree
class Instance(dict):
    next_id = 0
    instance_dict = {}
    def __init__(self, desc=None, kg=None):
        self["desc"] = "" if desc is None else desc
        self["id"] = Instance.next_id
        self["kg"] = [] if kg is None else kg
        self["mention_list"]: List[mytree] = []
        #
        Instance.next_id = Instance.next_id + 1
        Instance.instance_dict[self["id"]] = self

    @staticmethod
    def getInstanceById(instance_id):
        if isinstance(instance_id, str):
            instance_id = int(instance_id)
        if not isinstance(instance_id, int):
            raise TypeError("id should be str or int")
        return Instance.instance_dict[instance_id]

    def output_to_dict(self) -> Dict:
        output_dict = {}
        output_dict["desc"]: str = self["desc"]
        output_dict["id"]: int = self["id"]
        output_dict["kg"]: str = self["kg"]
        output_dict["mention_list"]: List[List[mytree]] = []
        for cur_mention in self["mention_list"]:
            m = []
            for cur_part in cur_mention:
                m.append(cur_part.output_to_dict())
            output_dict["mention_list"].append(m)
        return output_dict
