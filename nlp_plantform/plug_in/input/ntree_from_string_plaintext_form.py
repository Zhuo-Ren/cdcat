from nlp_plantform.center.nodetree import NodeTree

def input_from_string_plaintext_form(text):
    t = NodeTree({}, [])
    for cur_char in text:
        cur_node = NodeTree({'char': True}, [cur_char])
        t.append(cur_node)
    return t