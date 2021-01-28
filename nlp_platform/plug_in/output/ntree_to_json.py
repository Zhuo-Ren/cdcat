from nlp_platform.config import data_path
from nlp_platform.plug_in.input.ntree_from_pickle import input_ntree_from_pickle
from nlp_platform.plug_in.input.instances_from_pickle import input_instances_from_pickle
from nlp_platform.plug_in.manual_annotation_tool.cdcat.cdcat import cdcat
import json

# input
ntree = input_ntree_from_pickle(data_path + r"\ntree.pkl")
instances = input_instances_from_pickle(data_path + r"\instances.pkl")

node_list = []
ntree_position_list = ntree.walk_position()
for cur_node_position in ntree_position_list:
    cur_node = ntree[cur_node_position]
    from nlp_platform.center.nodetree import NodeTree
    if isinstance(cur_node, NodeTree):
        cur_node_dict = cur_node.to_info()
        node_list.append(cur_node_dict)
ntree_json = json.dumps(node_list, indent=4)
f = open('./ttt.json', 'w')
f.write(ntree_json)
f.close()

f = open('./ttt.json', 'r')
s = f.read()
info = json.loads(s)
print(info[3]['labels']['instance'])
root_node = NodeTree.from_info(root_node=None, info=info[0])
for cur_info in info[1:]:
    NodeTree.from_info(root_node=root_node, info= cur_info)
