from nlp_plantform.center.mytree import mytree

def input_from_string_plaintext_form(text):
    t = mytree({}, [])
    for cur_char in text:
        cur_node = mytree({'char': True}, [cur_char])
        t.append(cur_node)
    return t