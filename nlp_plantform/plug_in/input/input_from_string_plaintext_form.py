from nlp_plantform.center.ntree import ntree

def input_from_string_plaintext_form(text):
    t = ntree({}, [])
    for cur_char in text:
        cur_node = ntree({'char': True}, [cur_char])
        t.append(cur_node)
    return t