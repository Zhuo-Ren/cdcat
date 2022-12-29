class Corpus(object):
    #raw
    def __init__(self):
        from nlp_platform.center.tablepool import TablePool
        from nlp_platform.center.nodepool import NodePool
        from nlp_platform.center.instancepool import InstancePool
        from nlp_platform.center.raw import Raw

        self.raw = Raw()
        self._tp = TablePool(corpus=self)
        self._np = NodePool(corpus=self)
        self._ip = InstancePool(corpus=self)

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

    @np.setter
    def np(self, value):
        from nlp_platform.center.nodepool import NodePool
        if not isinstance(value, NodePool):
            raise TypeError
        self._np = value
        self._np.corpus = self

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, value):
        from nlp_platform.center.instancepool import InstancePool
        if not isinstance(value, InstancePool):
            raise TypeError
        self._ip = value
        self._ip.corpus = self
