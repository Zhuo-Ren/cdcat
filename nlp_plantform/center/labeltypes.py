class labeltype_radio(str):
    pass


class labeltype_listone(str):
    pass


class labeltype_readonly(str):
    pass


class labeltype_textinput(str):
    pass

from nlp_plantform.center.instance import Instance
class labeltype_instance(Instance):
    def __init__(self, value):
        print("构造")

    def __del__(self):
        print("析构")


class labeltype_nodes(list):
    pass


labeltypes = {
    "radio":labeltype_radio,
    "listone":labeltype_listone,
    "textreadonly":labeltype_readonly,
    "textinput":labeltype_textinput,
    "instance":labeltype_instance,
    "nodes": labeltype_nodes
}