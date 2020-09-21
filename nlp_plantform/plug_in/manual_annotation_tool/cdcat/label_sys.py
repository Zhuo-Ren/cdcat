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
    "list-one": setValue_list_one,
    "list-multi": setValue_list_multi,
    "text-readonly": setValue_text_readonly,
    "text-input":setValue_text_input,
    "instance": setValue_instance,
    "instances": setValue_instances,
    "node":setValue_node
}
