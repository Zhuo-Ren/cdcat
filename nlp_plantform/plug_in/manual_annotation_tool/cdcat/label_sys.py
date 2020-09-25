def setValue_radio(node, key):
    print(1)

def setValue_checkbox(node, key):
    print(1)

def setValue_list_one(node, key):
    print(1)

def setValue_list_multi(node, key):
    print(1)

def setValue_text_readonly(node, key):
    print(1)

def setValue_text_input(node, key):
    print(1)

def setValue_instance(node, key):
    print(1)

def setValue_instances(node, key):
    print(1)

def setValue_node(node, key):
    print(1)

labelTemplate = {
    "radio": setValue_radio,
    "checkbox": setValue_checkbox,
    "listone": setValue_list_one,
    "listmulti": setValue_list_multi,
    "textreadonly": setValue_text_readonly,
    "textinput":setValue_text_input,
    "instance": setValue_instance,
    "instances": setValue_instances,
    "node":setValue_node
}
