class Instance(dict):
    cur_id = 0

    def __init__(self, desc=None, kg=None):
        self["desc"] = "" if desc is None else desc
        self["id"] = Instance.cur_id = Instance.cur_id + 1
        self["kg"] = [] if kg is None else kg
        self["explain"] = []
        self["mention_list"] = []
