from typing import Dict, List, Tuple, Union  # for type hinting
from nlp_plantform.center.nodetree import NodeTree


class Instance(dict):

    def __init__(self, id=None, desc=None, kg=None):
        self["id"] = id
        self["desc"] = "" if desc is None else desc
        self["kg"] = [] if kg is None else kg
        self["mention_list"]: List[List[NodeTree]] = [[]]

    def output_to_dict(self) -> Dict:
        output_dict = {}
        output_dict["desc"]: str = self["desc"]
        output_dict["id"]: int = self["id"]
        output_dict["kg"]: str = self["kg"]
        output_dict["mention_list"]: List[List[NodeTree]] = []
        for cur_mention in self["mention_list"]:
            m = []
            for cur_part in cur_mention:
                m.append(cur_part.output_to_dict())
            output_dict["mention_list"].append(m)
        return output_dict
