class Instance(dict):
    next_id = 0
    instance_dict = {}
    def __init__(self, desc=None, kg=None):
        self["desc"] = "" if desc is None else desc
        self["id"] = Instance.next_id
        self["kg"] = [] if kg is None else kg
        self["explain"] = []
        self["mention_list"] = []
        #
        Instance.next_id = Instance.next_id + 1
        Instance.instance_dict[self["id"]] = self
