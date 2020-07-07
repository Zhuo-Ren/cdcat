from nlp_plantform.plug_in.input.input_from_string_plaintext_form import input_from_string_plaintext_form
from nlp_plantform.plug_in.input.add_from_list_of_token import add_from_list_of_token
from nlp_plantform.plug_in.manual_annotation_tool.cdcat.cdcat import cdcat
from nlp_plantform.center.mytree import mytree
from nlp_plantform.center.instance import Instance
import logging
import sys
import os

rootLogger = logging.getLogger()  # 如果getLogger函数没有参数，就返回root logger
rootLogger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler(stream=sys.stdout)  # sys.stderr
streamHandler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    fmt='%(message)s', datefmt=None, style='%'
)  # %(levelname)s
streamHandler.setFormatter(formatter)
rootLogger.addHandler(streamHandler)

# init
pass

# input
root = input_from_string_plaintext_form("我爱北京天安门。I like apple. Tiananmen is my favourite!")
# 分词
add_from_list_of_token(
    root,
    ['我', '爱', '北京', '天安门', '。', 'I', 'like', 'apple', '.', 'Tiananmen', 'is', 'my', 'favourite', '!']
)

# semanticType
root[0].get_label()["semanticType"] = "peo"
root[1].get_label()["semanticType"] = "act"
root[2].get_label()["semanticType"] = "org"
root[3].get_label()["semanticType"] = "addr"
root[5].get_label()["semanticType"] = "peo"
root[7].get_label()["semanticType"] = "act"
root[9].get_label()["semanticType"] = "sub"
root[12].get_label()["semanticType"] = "addr"
root[14].get_label()["semanticType"] = "act"
root[16].get_label()["semanticType"] = "peo"
mytree.add_parent({"semanticType": "addr"},[root[2],root[3]])
mytree.add_parent({}, [root[15], root[16], root[17]])
# instance
Instance(desc="我")
Instance(desc="天安门")
Instance(desc="苹果")
Instance(desc="爱")
Instance(desc="我爱天安门")
Instance(desc="我爱苹果")
Instance(desc="北京")
root[0].get_label()["instance"] = Instance.instance_dict[0]  # 我-我
Instance.instance_dict[0]["mention_list"].append([root[0]])
root[1].get_label()["instance"] = Instance.instance_dict[3]  # 爱-爱
Instance.instance_dict[3]["mention_list"].append([root[1]])
root[2].get_label()["instance"] = Instance.instance_dict[1]  # 北京天安门-天安门
Instance.instance_dict[1]["mention_list"].append([root[2]])
root[2, 0].get_label()["instance"] = Instance.instance_dict[6]  # 北京-北京
Instance.instance_dict[6]["mention_list"].append([root[2, 0]])
root[2, 1].get_label()["instance"] = Instance.instance_dict[1]  # 天安门-天安门
Instance.instance_dict[1]["mention_list"].append([root[2, 1]])
root[4].get_label()["instance"] = Instance.instance_dict[0]  # I-我
Instance.instance_dict[0]["mention_list"].append([root[4]])
root[6].get_label()["instance"] = Instance.instance_dict[3]  # like-爱
Instance.instance_dict[3]["mention_list"].append([root[6]])
root[11].get_label()["instance"] = Instance.instance_dict[1]
Instance.instance_dict[1]["mention_list"].append([root[11]])
root[15, 0].get_label()["instance"] = Instance.instance_dict[0]
Instance.instance_dict[0]["mention_list"].append([root[15, 0]])
root[15, 2].get_label()["instance"] = Instance.instance_dict[3]
Instance.instance_dict[3]["mention_list"].append([root[15, 2]])
#
Instance.getInstanceById(4)["mention_list"].append([root[0], root[1], root[2]])
Instance.getInstanceById(4)["mention_list"].append([root[11], root[13], root[15, 0], root[15, 2]])

# annotation
cdcat(root)

