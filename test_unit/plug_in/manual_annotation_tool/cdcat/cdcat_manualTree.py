from nlp_plantform.plug_in.input.ntree_from_string_plaintext_form import input_from_string_plaintext_form
from nlp_plantform.plug_in.process.add_from_list_of_token import add_from_list_of_token
from nlp_plantform.plug_in.manual_annotation_tool.cdcat.cdcat import cdcat
from nlp_plantform.center.nodetree import NodeTree
from nlp_plantform.center.instancepool import InstancePool

# init
pass

# input
root = input_from_string_plaintext_form("我爱北京天安门。I like apple. Tiananmen is my favourite!")
instances = InstancePool()

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
NodeTree.add_parent({"semanticType": "addr"}, [root[2], root[3]])
NodeTree.add_parent({}, [root[15], root[16], root[17]])
# instance
instances.add_instance(desc="我")
instances.add_instance(desc="天安门")
instances.add_instance(desc="苹果")
instances.add_instance(desc="爱")
instances.add_instance(desc="我爱天安门")
instances.add_instance(desc="我爱苹果")
instances.add_instance(desc="北京")
root[0].get_label()["instance"] = instances[0]  # 我-我
instances[0]["mention_list"].append([root[0]])
root[1].get_label()["instance"] = instances[3]  # 爱-爱
instances[3]["mention_list"].append([root[1]])
root[2].get_label()["instance"] = instances[1]  # 北京天安门-天安门
instances[1]["mention_list"].append([root[2]])
root[2, 0].get_label()["instance"] = instances[6]  # 北京-北京
instances[6]["mention_list"].append([root[2, 0]])
root[2, 1].get_label()["instance"] = instances[1]  # 天安门-天安门
instances[1]["mention_list"].append([root[2, 1]])
root[4].get_label()["instance"] = instances[0]  # I-我
instances[0]["mention_list"].append([root[4]])
root[6].get_label()["instance"] = instances[3]  # like-爱
instances[3]["mention_list"].append([root[6]])
root[11].get_label()["instance"] = instances[1]
instances[1]["mention_list"].append([root[11]])
root[15, 0].get_label()["instance"] = instances[0]
instances[0]["mention_list"].append([root[15, 0]])
root[15, 2].get_label()["instance"] = instances[3]
instances[3]["mention_list"].append([root[15, 2]])
#
instances.get_instance(4)[0]["mention_list"].append([root[0], root[1], root[2]])
instances.get_instance(4)[0]["mention_list"].append([root[11], root[13], root[15, 0], root[15, 2]])

# annotation
cdcat(root)

