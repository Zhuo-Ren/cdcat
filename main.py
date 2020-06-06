from nlp_plantform.plug_in.input.input_from_string_plaintext_form import input_from_string_plaintext_form
from nlp_plantform.plug_in.input.add_from_list_of_token import add_from_list_of_token
from nlp_plantform.plug_in.manual_annotation_tool.cdcat.cdcat import cdcat
from nlp_plantform.center.mytree import mytree
from nlp_plantform.center.instance import Instance


# init
pass

# input
root = input_from_string_plaintext_form("我爱北京天安门。I like apple.")
# 分词
add_from_list_of_token(root, ['我', '爱', '北京', '天安门', '。', 'I', 'like', 'apple', '.'])
# semanticType
root[0].get_label()["semanticType"] = "peo"
root[2].get_label()["semanticType"] = "org"
root[3].get_label()["semanticType"] = "addr"
mytree.add_parent({},[root[2],root[3]])
root[2].get_label()["semanticType"] = "addr"
# instance
i1 = Instance(desc="我")
i2 = Instance(desc="天安门")
i3 = Instance(desc="苹果")
i4 = Instance(desc="爱")
i5 = Instance(desc="我爱天安门")
i6 = Instance(desc="我爱苹果")

root[0].get_label()["instance"] = Instance.instance_dict[0]
root[1].get_label()["instance"] = Instance.instance_dict[3]
root[2][1].get_label()["instance"] = Instance.instance_dict[1]
# root.draw()
# annotation
cdcat(root)

