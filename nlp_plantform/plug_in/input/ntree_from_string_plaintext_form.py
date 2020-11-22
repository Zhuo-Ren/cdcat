from nlp_plantform.center.nodetree import NodeTree


def input_from_string_plaintext_form(text):
    """
    Generate node tree based on a text.

    This function generate a parent node, and generate child ndoe for each char in param *text*. Thus construct a
    2-layer tree.

    :param text:
    :return: The parent node.
    """
    t = NodeTree(label={}, children=[])
    for cur_char in text:
        cur_node = NodeTree({'char': True}, [cur_char])
        t.append(cur_node)
    return t