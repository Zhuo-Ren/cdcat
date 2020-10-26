from nlp_plantform.center.nodetree import NodeTree


def input_ntree_from_string_bracket_form(bracketstring: str) -> NodeTree:
    """
    This function read a bracket string likes shown below and return the corresponding nodetree obj.

    example::
    >> r = input_ntree_from_string_bracket_form('(S (NP (D the) (N dog)) (VP (V chased) (NP (D the) (N cat))))')
    >> r.draw()

    :param bracketstring:
    :return:
    """
    # param check: bracketstring
    if not isinstance(bracketstring,str):
        raise TypeError

    ntree = NodeTree.fromstring(bracketstring)
    # ntree = NodeTree.fromstring('(S (NP (D the) (N dog)) (VP (V chased) (NP (D the) (N cat))))')

    return ntree
