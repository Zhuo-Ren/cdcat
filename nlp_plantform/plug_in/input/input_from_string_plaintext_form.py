from nlp_plantform.center.mytree import mytree

def input_from_string_plaintext_form(text):
    t = mytree('S', [])
    for cur_char in text:
        cur_node = mytree('char', [cur_char])
        t.append(cur_node)
    return t