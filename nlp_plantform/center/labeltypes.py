class labeltype_radio(str):
    def readable(self):
        return  self


class labeltype_listone(str):
    def readable(self):
        return  self


class labeltype_readonly(str):
    def readable(self):
        return  self


class labeltype_textinput(str):
    def readable(self):
        return  self

from nlp_plantform.center.instance import Instance
class labeltype_instance(Instance):
    def __init__(self, value):
        print("构造")

    def __del__(self):
        print("析构")

    def readable(self):
        return  self.labels.readable(nolink=True)

class labeltype_nodes(list):
    def readable(self):
        return [[node.labels.readable(nolink=True) for node in nodeList] for nodeList in self]


labeltypes = {
    "radio":labeltype_radio,
    "listone":labeltype_listone,
    "textreadonly":labeltype_readonly,
    "textinput":labeltype_textinput,
    "instance":labeltype_instance,
    "nodes": labeltype_nodes
}