from nlp_plantform.center.mytree import mytree
from typing import Dict, List, Tuple, Union

def add_from_list_of_token(basetree: mytree, token_list: List[str]):
    """
    example::
        >>> s = "abc def g 我爱北京天安门"
        >>> root = input_from_string_plaintext_form(s)
        >>> add_from_list_of_token(root, ['abc', 'def', 'g', '我', '爱', '北京', '天安门'])
    :param basetree:
    :param token_list:
    :return:
    """
    leaves_iter = iter(basetree.all_nleaves())
    cur_node = None
    for token_index in range(0, len(token_list)):
        token_list[token_index] = [[i, None] for i in token_list[token_index]]
        for char_unit_index in range(0, len(token_list[token_index])):
            while (
                cur_node is None
                or
                cur_node[0] is " "
            ):
                cur_node = next(leaves_iter)
            if cur_node[0] == token_list[token_index][char_unit_index][0]:
                token_list[token_index][char_unit_index][1] = cur_node
                try:
                    cur_node = next(leaves_iter)
                except StopIteration:
                    pass
            else:
                raise RuntimeError("can not add token")
    for cur_token in token_list:
        mytree.add_parent("token", [i[1] for i in cur_token])

