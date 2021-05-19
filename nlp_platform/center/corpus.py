class Corpus(object):
    def __init__(self):
        from nlp_platform.center.tablepool import TablePool
        from nlp_platform.center.nodepool import NodePool
        from nlp_platform.center.instancepool import InstancePool
        self.raw = {}
        self._tp = TablePool()
        self._np = NodePool()
        self._ip = InstancePool()

    @property
    def tp(self):
        return self._tp

    @tp.setter
    def tp(self, value):
        from nlp_platform.center.tablepool import TablePool
        if not isinstance(value, TablePool):
            raise TypeError
        self._tp = value
        self._tp.corpus = self

    @property
    def np(self):
        return self._np

    @tp.setter
    def np(self, value):
        from nlp_platform.center.nodepool import NodePool
        if not isinstance(value, NodePool):
            raise TypeError
        self._np = value
        self._np.corpus = self

    @property
    def ip(self):
        return self._ip

    @tp.setter
    def ip(self, value):
        from nlp_platform.center.instancepool import InstancePool
        if not isinstance(value, InstancePool):
            raise TypeError
        self._ip = value
        self._ip.corpus = self
