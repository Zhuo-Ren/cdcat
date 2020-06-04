from nlp_plantform.center.lang_node import LangNode
from nlp_plantform.plug_in.input.input_from_string_plaintext_form import input_from_string_plaintext_form
from nlp_plantform.plug_in.input.add_from_list_of_token import add_from_list_of_token
from nlp_plantform.plug_in.manual_annotation_tool.cdcat.cdcat import cdcat
from nlp_plantform.center.mytree import mytree
s = "abc def g 我爱北京天安门"

# init
LangNode()

# input
root = input_from_string_plaintext_form(s)
add_from_list_of_token(root, ['abc', 'def', 'g', '我', '爱', '北京', '天安门'])
# annotation
cdcat(root)
# root.draw()

