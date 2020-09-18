def setValue_radio(node, key):
    print(1)

def setValue_checkbox(node, key):
    print(1)

def setValue_list_one(node, key):
    print(1)

def setValue_list_multi(node, key):
    print(1)

def setValue_instance(node, key):
    print(1)

def setValue_instances(node, key):
    print(1)

def setValue_text(node, key):
    print(1)

labelTemplate = {
    "radio": setValue_radio,
    "checkbox": setValue_checkbox,
    "list-one": setValue_list_one,
    "list-multi": setValue_list_multi,
    "instance": setValue_instance,
    "instances": setValue_instances,
    "text": setValue_text
}
