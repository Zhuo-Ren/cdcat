class DirectedRelationTable(object):  # 有向图
    def __init__(self, content={}, max_o_degree=None, max_i_degree=None):
        self.center = {}
        """
        以(出节点, 入接点)为key，存放边的值::

            >>> self.center
            {
                ("a", "b"): 3,  # 一条从a指向b的有向边，其边上的值为3
                ("a", "c"): 2,  # 一条从a指向c的有向边，其边上的值为2
                ("无关"， "无关"): "无关"
            }

        语义上，相同的边只能有一条，即从a指向b的边只能有一条。

        一个DirectedRelationTable中实际存放的边可能比center中的少。
        一个DirectedRelationTable中实际存放的边取决于两个索引idx_o和idx_i。
        例如，如果idx_o和idx_i像他们各自注释中缩写的那样，
        那么虽然center中一个无关边，但它其实不起作用，因为索引中没它。

        """

        self.idx_o = {}  # 按照先出节点再入节点的顺序建立索引
        """
        Follow the example in the comment of self.center::

            >>> self.idx_o
            {
                "a": {
                    "b": None,
                    "c": None
                }
            }
        """
        self.idx_i = {}  # 按照先入节点再出节点的顺序建立索引
        """
        Follow the example in the comment of self.center::

            >>> self.idx_i
            {
                "b": {
                    "a": None,
                },
                "c": {
                    "a": None
                }
            }
        """
        self.max_o_degree = max_o_degree
        self.max_i_degree = max_i_degree

        # param check
        if not isinstance(content, dict):
            raise TypeError
        #
        for key, value in content.items():
            self.add_item(key, value)

    def add_item(self, key, value):
        # check: key
        if not isinstance(key, tuple):
            raise TypeError
        if len(key) != 2:
            raise TypeError
        # check: relation repetition
        """ This function is useless, because there can not be repetition in dict.
        if self.have(key) > 0:
            raise RuntimeError("This relation already exits.")
        """
        # check: in and out degree
        if self.max_o_degree is not None:
            if self.have((key[0], None)) >= self.max_o_degree:
                raise RuntimeError("exceed the out degree limit.")
        if self.max_i_degree is not None:
            if self.have((None, key[1])) >= self.max_i_degree:
                raise RuntimeError("exceed the in degree limit.")
        # add cur item
        self.center[key] = value
        # update idx
        try:
            self.idx_o[key[0]][key[1]] = None
        except KeyError:
            self.idx_o[key[0]] = {}
            self.idx_o[key[0]][key[1]] = None
        try:
            self.idx_i[key[1]][key[0]] = None
        except KeyError:
            self.idx_i[key[1]] = {}
            self.idx_i[key[1]][key[0]] = None

    def __getitem__(self, key):
        """
        a[[1,2]]或a[1,2]或a[(1,2)]             → key=(1,2)
        a[[None, 2]]或a[None, 2]或a[(None, 2)] → key=(None, 2)
        a[[1, None]]或a[1, None]或a[(1, None)] → key=(1, None)
        a[1]                                   → key=(1, None)
        :param key:
        :return:
        """
        o_node = None
        i_node = None

        # key check and extract
        if isinstance(key, tuple):
            if len(key) == 2:
                o_node = key[0]
                i_node = key[1]
            else:
                raise RuntimeError('key with bad format.')
        elif isinstance(key, (str, int)):  # for: a[1]
            o_node = key
            i_node = None
        else:
            raise TypeError('Key should be a tuple, list, str or int.')

        #
        try:
            if o_node is None and i_node is None:
                raise RuntimeError('key with bad format.')
            elif o_node is None and i_node is not None:
                r = {}
                for o_node in self.idx_i[i_node]:
                    r[(o_node, i_node)] = self.center[(o_node, i_node)]
                if len(r) == 0:
                    raise KeyError(key)
                r = DirectedRelationTable(content=r,
                                          max_o_degree=self.max_o_degree,
                                          max_i_degree=self.max_i_degree)
                r.center = self.center  # 这样可以使__getitem__实现浅拷贝
                return r
            elif o_node is not None and i_node is None:
                r = {}
                for i_node in self.idx_o[o_node]:
                    r[(o_node, i_node)] = self.center[(o_node, i_node)]
                if len(r) == 0:
                    raise KeyError(key)
                r = DirectedRelationTable(content=r,
                                          max_o_degree=self.max_o_degree,
                                          max_i_degree=self.max_i_degree)
                r.center = self.center  # 这样可以使__getitem__实现浅拷贝
                return r
            elif o_node is not None and i_node is not None:
                r = self.center[key]
                return r
        except KeyError:
            raise KeyError(key)

    def __setitem__(self, key, value):
        # key check
        if not isinstance(key, tuple):
            raise TypeError
        if len(key) != 2:
            raise RuntimeError
        #
        if key in self.center:
            # 如果当前key已有 直接改
            self.center[key] = value
        else:
            # 如果没有 创建
            self.add_item(key, value)

    def have(self, key):
        """
        Given a key, return the number of matched relation(s).

        :param key: A tuple that describes the two node of target relation.
        :type key: tuple
        :return: Number of matched relation(s).
        :rtype: int
        """
        o_node = None
        i_node = None

        # key check and extract
        if isinstance(key, tuple):
            if len(key) == 2:
                o_node = key[0]
                i_node = key[1]
            else:
                raise RuntimeError('key with bad format.')
        elif isinstance(key, (str, int)):  # for: a[1]
            o_node = key
            i_node = None
        else:
            raise TypeError('Key should be a tuple, list, str or int.')

        #
        try:
            if o_node is None and i_node is None:
                raise RuntimeError('key with bad format.')
            elif o_node is None and i_node is not None:
                count = 0
                for o_node in self.idx_i[i_node]:
                    count += 1
                return count
            elif o_node is not None and i_node is None:
                count = 0
                for i_node in self.idx_o[o_node]:
                    count += 1
                return count
            elif o_node is not None and i_node is not None:
                self.center[(o_node, i_node)]
                return 1
        except KeyError:
            return 0

    def to_dict(self):
        """
        以字典形式返回此对象中的每一条边::

            >>> a_drt.to_dict()
            {
                ("a", "b"): 1,
                ("a", "c"): 4,
                ("b", "a"): 2
            }

        此对象和返回的字典是深拷贝关系。修改字典，不影响此对象。

        :return:
        """
        r = {}
        for o_node in self.idx_o.keys():
            for i_node in self.idx_o[o_node].keys():
                r[(o_node, i_node)] = self.center[(o_node, i_node)]
        return r


class UndirectedRelationTable(object):  # 无向图
    def __init__(self, content={}, max_degree=None):
        self.center = {}
        """
        以(a节点, b接点)为key，存放边的值。（因为无向图部分出入节点，所以称为a节点和b节点）::

            >>> self.center
            {
                ("a", "b"): 3,  # 一条连接a和b的无向边，其边上的值为3
                ("a", "c"): 2,  # 一条链接a和c的有向边，其边上的值为2
                ("无关"， "无关"): "无关"
            }

        语义上，相同的边只能有一条，即连接a和b的边只能有一条。

        一个UndirectedRelationTable中实际存放的边可能比center中的少。
        一个UndirectedRelationTable中实际存放的边取决于两个索引idx_o和idx_i。
        例如，如果idx_o和idx_i像他们各自注释中缩写的那样，
        那么虽然center中一个无关边，但它其实不起作用，因为索引中没它。

        因为是无向图，所以self.center中的边其实两个节点部分先后，
        即("a", "b")和("b", "a")在语义上其实是同一条边。
        但是两者只存一个，任意一个都行。
        """

        self.idx_a = {}  # 按照先a节点再b节点的顺序建立索引
        """
        Follow the example in the comment of self.center::

            >>> self.idx_o
            {
                "a": {
                    "b": None,
                    "c": None
                }
            }
        """
        self.idx_b = {}  # 按照先b节点再a节点的顺序建立索引
        """
        Follow the example in the comment of self.center::

            >>> self.idx_i
            {
                "b": {
                    "a": None,
                },
                "c": {
                    "a": None
                }
            }
        """
        self.max_degree = max_degree

        # param check
        if not isinstance(content, dict):
            raise TypeError
        #
        for key, value in content.items():
            self.add_item(key, value)

    def add_item(self, key, value):
        # check: key
        if not isinstance(key, tuple):
            raise TypeError
        if len(key) != 2:
            raise TypeError
        # check: relation repetition
        if self.have(key) > 0:
            raise RuntimeError("This relation already exits.")
        # check: degree
        if self.max_degree is not None:
            if self.have((key[0])) >= self.max_degree:
                raise RuntimeError("exceed the degree limit.")
            if self.have((key[1])) >= self.max_degree:
                raise RuntimeError("exceed the degree limit.")
        # add cur item
        self.center[key] = value
        # update idx
        try:
            self.idx_a[key[0]][key[1]] = None
        except KeyError:
            self.idx_a[key[0]] = {}
            self.idx_a[key[0]][key[1]] = None
        try:
            self.idx_b[key[1]][key[0]] = None
        except KeyError:
            self.idx_b[key[1]] = {}
            self.idx_b[key[1]][key[0]] = None


    def __getitem__(self, key):
        """
        a[[1,2]]或a[1,2]或a[(1,2)]             → key=(1,2) 等价于(1,2)和(2,1)
        a[1]                                   → key=(1)   等价于(1, None)和(None, 1)

        :param key:
        :return:
        """
        a_node = None
        b_node = None

        # key check and extract
        if isinstance(key, tuple):
            if len(key) == 2:
                if key[0] is not None and key[1] is not None:
                    a_node = key[1]
                    b_node = key[0]
                else:
                    raise RuntimeError("key with bad format.")
            else:
                raise RuntimeError("key with bad format.")
        elif isinstance(key, (str, int)):
            a_node = key
            b_node = None
        else:
            raise TypeError("Key should be a tuple, list, str or int.")

        #
        try:
            if a_node is None and b_node is None:
                raise RuntimeError('key with bad format.')
            elif a_node is None and b_node is not None:
                raise RuntimeError('key with bad format.')
            elif a_node is not None and b_node is None:
                r = {}
                for b_node in self.idx_a[a_node]:
                    r[(a_node, b_node)] = self.center[(a_node, b_node)]
                b_node = a_node
                for a_node in self.idx_b[b_node]:
                    r[(a_node, b_node)] = self.center[(a_node, b_node)]
                if len(r) == 0:
                    raise RuntimeError('key with bad format.')
                r = UndirectedRelationTable(content=r, max_degree=self.max_degree)
                r.center = self.center  # 这样可以使__getitem__实现浅拷贝
                return r
            elif a_node is not None and b_node is not None:
                r = self.center[key]
                return r
        except KeyError:
            raise KeyError(key)

    def __setitem__(self, key, value):
        # key check
        if not isinstance(key, tuple):
            raise TypeError
        if len(key) != 2:
            raise RuntimeError
        #
        if key in self.center:
            # 如果当前key已有 直接改
            self.center[key] = value
        else:
            # 如果没有 创建
            self.add_item(key, value)


    def have(self, key):
        """
        Given a key, return the number of matched relation(s).

        :param key: A tuple that describes the two node of target relation.
        :type key: tuple
        :return: Number of matched relation(s).
        :rtype: int
        """
        a_node = None
        b_node = None

        # key check and extract
        if isinstance(key, tuple):
            if len(key) == 2:
                if key[0] is not None and key[1] is not None:
                    a_node = key[1]
                    b_node = key[0]
                else:
                    raise RuntimeError("key with bad format.")
            else:
                raise RuntimeError("key with bad format.")
        elif isinstance(key, (str, int)):
            a_node = key
            b_node = None
        else:
            raise TypeError("Key should be a tuple, list, str or int.")

        #
        if a_node is None and b_node is None:
            raise RuntimeError('key with bad format.')
        elif a_node is None and b_node is not None:
            raise RuntimeError('key with bad format.')
        elif a_node is not None and b_node is None:
            count = 0
            if a_node in idx_a:
                for b_node in self.idx_a[a_node]:
                    count += 1
            b_node = a_node
            if b_node in idx_b:
                for a_node in self.idx_b[b_node]:
                    count += 1
            return count
        elif a_node is not None and b_node is not None:
            try:
                self.center[(a_node, b_node)]
            except KeyError:
                return 0
            else:
                return 1

    def to_dict(self, repeat=False):
        """
        以字典形式返回此对象中的每一条边::

            >>> a_drt.to_dict(repeat=False)
            {
                ("a", "b"): 1,
                ("a", "c"): 4,
                ("b", "a"): 2
            }
            >>> a_drt.to_dict(repeat=True)
            {
                ("a", "b"): 1,
                ("b", "a"): 1,
                ("a", "c"): 4,
                ("c", "a"): 4,
                ("b", "a"): 2
                ("a", "b"): 2
            }

        此对象和返回的字典是深拷贝关系。修改字典，不影响此对象。

        :return:
        """
        r = {}
        for a_node in self.idx_a.keys():
            for b_node in self.idx_a[a_node].keys():
                if repeat:
                    r[(a_node, b_node)] = self.center[(a_node, b_node)]
                    r[(b_node, a_node)] = self.center[(a_node, b_node)]
                else:
                    r[(a_node, b_node)] = self.center[(a_node, b_node)]
        return r
