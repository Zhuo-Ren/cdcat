import re
from six import string_types
from typing import Dict, List, Tuple, Union  # for type hinting
from nltk.grammar import Production, Nonterminal
from nltk.util import slice_bounds
from nltk.compat import python_2_unicode_compatible, unicode_repr
from nltk.tree import ParentedTree


class NodeTree(ParentedTree):
    r"""
    node::

        -  parent
        -  *position*
        -  labels
            - nltk_label
            - XXXX
    """
    fixed_keys = []
    config = {}

    def __init__(self, label: Union[str, Dict] = None, children: Union[None, List["NodeTree"]] = None):
        # parent
        self.parent = None
        # labels
        self.labels = None
        # fixed label
        pass
        # add children
        pass

    # labels g s
    # nltk_label g s
    # fixed_labels g s
    # configured_labels g s
    # free_labels g s

    # parent
    def get_parent(self) -> Union[None, "NodeTree"]:
        return self._parent
    parent = get_parent
    def set_parent(self, new_parent, new_index):
        raise TypeError("tree obj does not support set_parent, "
                        "tree_obj.set_parent(parent, index) should be"
                        "replaced with parent.insert(index, tree_obj)"
                        "or parent[index]=tree_obj"
                        "or del parent[index]")
    _setparent = set_parent



    def get_label(self):
        """
        Return the node label of the tree.

            t = Tree.fromstring('(S (NP (D the) (N dog)) (VP (V chased) (NP (D the) (N cat))))')
            t.get_label()
            'S'

        :return: the node label (typically a string)
        :rtype: any
        """
        return self._labels

    def set_label(self, label):
        """
        Set the node label of the tree.

            >>> t = Tree.fromstring("(S (NP (D the) (N dog)) (VP (V chased) (NP (D the) (N cat))))")
            >>> t.set_label("T")
            >>> print(t)
            (T (NP (D the) (N dog)) (VP (V chased) (NP (D the) (N cat))))

        :param label: the node label (typically a string)
        :type label: any
        """
        self.labels = label

    def add_label(self, label_dict) -> None:
        """
        Add label.

        :param label_dict: For example: {label_key: label_value, ...}
        """
        self._labels.update(label_dict)

    def del_label(self, label_key):
        del self._labels[label_key]

    # obj operations-------------------------------------------
    def __eq__(self, other):
        return id(self) == id(other)

    def __lt__(self, other):
        if not isinstance(other, NodeTree):
            # raise_unorderable_types("<", self, other)
            # Sometimes children can be pure strings,
            # so we need to be able to compare with non-trees:
            return self.__class__.__name__ < other.__class__.__name__
        elif self.__class__ is other.__class__:
            return (self._labels, list(self)) < (other._labels, list(other))
        else:
            return self.__class__.__name__ < other.__class__.__name__

    __ne__ = lambda self, other: not self == other

    __gt__ = lambda self, other: not (self < other or self == other)

    __le__ = lambda self, other: self < other or self == other

    __ge__ = lambda self, other: not self < other

    # list operations-----------------------------------
    def __mul__(self, v):
        raise TypeError('Tree does not support multiplication')

    def __rmul__(self, v):
        raise TypeError('Tree does not support multiplication')

    def __add__(self, v):
        raise TypeError('Tree does not support addition')

    def __radd__(self, v):
        raise TypeError('Tree does not support addition')

    def __getitem__(self, index):
        # 继承list的索引和切片：tree_obj[1] 或 tree_obj[0:4]
        if isinstance(index, (int, slice)):
            return list.__getitem__(self, index)
        # 新增按路径索引：tree_obj[1, 1, 0] tree_obj(1, 1, 0)，等价于tree_obj[1][1][0]
        elif isinstance(index, (list, tuple)):
            if len(index) == 0:
                return self
            elif len(index) == 1:
                return self[index[0]]
            else:
                return self[index[0]][index[1:]]
        else:
            raise TypeError("%s indices must be integers, not %s" %
                            (type(self).__name__, type(index).__name__))

    def __delitem__(self, index):
        # 继承list的索引：del tree_obj[i]
        if isinstance(index, int):
            child = self[index]
            # Remove the child
            list.__delitem__(self, index)
            # Clear the child's parent pointer.
            if isinstance(child, NodeTree):
                if child.get_parent is not None:
                    child._parent = None

        # 继承list的切片：del tree_obj[start:stop]
        elif isinstance(index, slice):
            start, stop, step = slice_bounds(self, index, allow_step=True)
            # Clear all the children pointers.
            for i in range(start, stop, step):
                del self[i]

        # 新增按路径索引：del tree_obj[1, 1, 0]等价于del tree_obj[1][1][0]
        elif isinstance(index, (list, tuple)):
            # del tree_obj[()] 或 del tree_obj[[]]
            if len(index) == 0:
                raise IndexError('The tree position () may not be deleted.')
            # del tree_obj[(i,)] 或 del tree_obj[[i,]]
            elif len(index) == 1:
                del self[index[0]]
            # del tree_obj[(i1, i2, i3)] 或 del tree_obj[[i1, i2, i3]]
            else:
                del self[index[0]][index[1:]]

        else:
            raise TypeError("%s indices must be integers, not %s" %
                            (type(self).__name__, type(index).__name__))

    def __setitem__(self, index, value):
        assert isinstance(index, (int, slice, list, tuple))
        # 继承list的索引：tree_obj[i] = value
        if isinstance(index, int):
            old_child = self[index]
            new_child = value
            # 修改新孩子
            if isinstance(new_child, NodeTree):
                if new_child._parent is not None:
                    raise RuntimeError("can not add a tree which already has parent")
                else:
                    new_child._parent = self
            # 修改自己
            list.__setitem__(self, index, new_child)
            # 修改旧孩子
            if isinstance(old_child, NodeTree):
                old_child._parent = None

        # 继承list的切片：tree_obj[start:stop] = value
        elif isinstance(index, slice) and isinstance(value, (tuple, list)):
            old_child_list = self[index]
            new_child_list = value if isinstance(value, (tuple, list)) else list(value)
            # 修改新孩子
            for new_child in new_child_list:
                if new_child._parent is not None:
                    raise RuntimeError("can not add a tree which already has parent")
                else:
                    new_child._parent = self
            # 修改自己
            list.__setitem__(self, index, new_child_list)
            # 修改旧孩子
            for old_child in old_child_list:
                if isinstance(old_child, NodeTree):
                    old_child._parent = None

        # 新增按路径索引：tree_obj[1, 1, 0]=value，等价于tree_obj[1][1][0]=value
        elif isinstance(index, (list, tuple)):
            # tree_obj[()] = value
            if len(index) == 0:
                raise IndexError('The tree position () may not be assigned to.')
            # tree_obj[(i,)] = value
            elif len(index) == 1:
                self[index[0]] = value
            # tree_obj[i1, i2, i3] = value
            else:
                self[index[0]][index[1:]] = value

        else:
            raise TypeError("%s indices must be integers, not %s" %
                            (type(self).__name__, type(index).__name__))

    def append(self, value):
        # 孩子节点类型一致性检测
        """
        if len(self) == 0:
            pass
        else:
            if self.is_leaf_node():
                assert not isinstance(value, ntree)
            else:
                assert isinstance(value, ntree)
        """
        # 修改孩子
        if isinstance(value, NodeTree):
            if value._parent is not None:
                raise RuntimeError("can not add a tree which already has parent")
            else:
                value._parent = self
        # 修改自己
        list.append(self, value)

    def extend(self, value_list):
        for value in value_list:
            self.append(value)

    def insert(self, index, value):
        # 孩子节点类型一致性检测
        """
        if len(self) == 0:
            pass
        else:
            if self.is_leaf_node():
                assert not isinstance(value, ntree)
            else:
                assert isinstance(value, ntree)
        """
        # 修改孩子
        if isinstance(value, NodeTree):
            if value._parent is not None:
                raise RuntimeError("can not add a tree which already has parent")
            else:
                value._parent = self
        # 修改自己
        list.insert(self, index, value)

    def pop(self, index=-1):
        assert isinstance(index, int)
        # 修改自己
        child = list.pop(self, index)
        # 修改孩子
        if isinstance(child, NodeTree):
            child._parent = None
        return child

    def remove(self, child):
        for i in range(0, len(self)):
            if self[i] == child:
                del self[i]
                child._parent = None
                return

    if hasattr(list, '__getslice__'):
        def __getslice__(self, start, stop):
            return self.__getitem__(slice(max(0, start), max(0, stop)))

        def __delslice__(self, start, stop):
            return self.__delitem__(slice(max(0, start), max(0, stop)))

        def __setslice__(self, start, stop, value):
            return self.__setitem__(slice(max(0, start), max(0, stop)), value)

    # Basic tree operations-------------------------------------------
    def parent_index(self):
        """
        The index of this tree in its parent.  I.e.,
        ``ptree.parent()[ptree.parent_index()] is ptree``.  Note that
        ``ptree.parent_index()`` is not necessarily equal to
        ``ptree.parent.index(ptree)``, since the ``index()`` method
        returns the first child that is equal to its argument.
        """
        if self._parent is None:
            return None
        for i, child in enumerate(self._parent):
            if child is self: return i
        assert False, 'expected to find self in self._parent!'

    def position(self, output_type="tuple") -> Tuple[int]:
        """获取路径。
        example::
            (1, 1, 0)
        The tree position of this tree, relative to the root of the
        tree.  I.e., ``ptree.root[ptree.treeposition] is ptree``.
        """
        if output_type == "tuple":
            if self.parent() is None:
                return ()
            else:
                return self.parent().treeposition() + (self.parent_index(),)
        elif output_type == "string":
            if self.parent() is None:
                return ""
            else:
                position_tuple = self.parent().treeposition() + (self.parent_index(),)
                position_string = "-".join(str(i) for i in position_tuple)
                return position_string
    treeposition = position

    @staticmethod
    def str_to_position(positionStr: str):
        if positionStr is None:
            return None
        elif positionStr == "":
            return ()
        elif isinstance(positionStr, str):
            return tuple(int(i) for i in positionStr.split("-"))
        else:
            raise TypeError("1th arg should be None or string")

    @staticmethod
    def position_to_str(position: Tuple):
        if position == ():
            return ""
        else:
            r = [str(i) for i in position]
            return "-".join(r)

    def left_sibling(self):
        """获取左边那个兄弟。
        The left sibling of this tree, or None if it has none.
        """
        parent_index = self.parent_index()
        if self._parent and parent_index > 0:
            return self._parent[parent_index - 1]
        return None  # no left sibling

    def right_sibling(self, acceptCousin=False) -> "NodeTree":
        """获取右边那个兄弟。
        The right sibling of this tree, or None if it has none.
        """
        parent_index = self.parent_index()
        if self._parent and parent_index < (len(self._parent) - 1):
            return self._parent[parent_index + 1]
        else:
            if acceptCousin == False:
                return None  # no right sibling
            else:
                cur_node = self.get_parent()
                while cur_node:
                    if cur_node.right_sibling():
                        return cur_node.right_sibling()
                    else:
                         cur_node = cur_node.get_parent()
                return None

    def root(self):
        """获取根。
        The root of this tree.  I.e., the unique ancestor of this tree
        whose parent is None.  If ``ptree.parent()`` is None, then
        ``ptree`` is its own root.
        """
        root = self
        while root.parent() is not None:
            root = root.parent()
        return root

    def flatten(self):
        """
        Return a flat version of the tree, with all non-root non-terminals removed.

            >>> t = Tree.fromstring("(S (NP (D the) (N dog)) (VP (V chased) (NP (D the) (N cat))))")
            >>> print(t.flatten())
            (S the dog chased the cat)

        :return: a tree consisting of this tree's root connected directly to
            its leaves, omitting all intervening non-terminal nodes.
        :rtype: Tree
        """
        return NodeTree(self.get_label(), self.leaves())

    def height(self):
        """
        Return the height of the tree.

            >>> t = Tree.fromstring("(S (NP (D the) (N dog)) (VP (V chased) (NP (D the) (N cat))))")
            >>> t.height()
            5
            >>> print(t[0,0])
            (D the)
            >>> t[0,0].height()
            2

        :return: The height of this tree.  The height of a tree
            containing no children is 1; the height of a tree
            containing only leaves is 2; and the height of any other
            tree is one plus the maximum of its children's
            heights.
        :rtype: int
        """
        max_child_height = 0
        for child in self:
            if isinstance(child, NodeTree):
                max_child_height = max(max_child_height, child.height())
            else:
                max_child_height = max(max_child_height, 1)
        return 1 + max_child_height

    def walk_position(self, order='preorder') -> List[Tuple]:
        """遍历树。
        Traverse the tree, in given order, optionally restricted to leaves.

        example::
            >>> t = NodeTree.fromstring("(S (NP (D the) (N dog)) (VP (V chased) (NP (D the) (N cat))))")
            >>> t.walk_positions()
            [(), (0,), (0, 0), (0, 0, 0), (0, 1), (0, 1, 0), (1,), (1, 0), (1, 0, 0), (1, 1), (1, 1, 0), (1, 1, 0, 0), (1, 1, 1), (1, 1, 1, 0)]
            >>> for pos in t.walk_positions('leaves'):
            ...     t[pos] = t[pos][::-1].upper()
            >>> print(t)
            (S (NP (D EHT) (N GOD)) (VP (V DESAHC) (NP (D EHT) (N TAC))))

        :param order: Select from: ``preorder``先序遍历, ``postorder``后序遍历,
         ``bothorder``中序遍历,``leaves``只遍历叶子.
        :return: A list of tuples, one tuple is one node path.
        """
        positions = []
        if order in ('preorder', 'bothorder'): positions.append( () )
        for i, child in enumerate(self):
            if isinstance(child, NodeTree):
                childpos = child.treepositions(order)
                positions.extend((i,)+p for p in childpos)
            else:
                positions.append( (i,) )
        if order in ('postorder', 'bothorder'): positions.append( () )
        return positions
    treepositions = walk_position

    def subtrees(self, filter=None):
        """ 获取所有符合要求的子树。
        Generate all the subtrees of this tree, optionally restricted
        to trees matching the filter function.

        example::
            >>> t = Tree.fromstring("(S (NP (D the) (N dog)) (VP (V chased) (NP (D the) (N cat))))")
            >>> for s in t.subtrees(lambda t: t.height() == 2):
            ...     print(s)
            (D the)
            (N dog)
            (V chased)
            (D the)
            (N cat)

        :type filter: function
        :param filter: the function to filter all local trees
        """
        if not filter or filter(self):
            yield self
        for child in self:
            if isinstance(child, NodeTree):
                for subtree in child.subtrees(filter):
                    yield subtree

    def productions(self):
        """返回树中涉及的所有生成式语法。
        Generate the productions that correspond to the non-terminal nodes of the tree.
        For each subtree of the form (P: C1 C2 ... Cn) this produces a production of the
        form P -> C1 C2 ... Cn.

            >>> t = Tree.fromstring("(S (NP (D the) (N dog)) (VP (V chased) (NP (D the) (N cat))))")
            >>> t.productions()
            [S -> NP VP, NP -> D N, D -> 'the', N -> 'dog', VP -> V NP, V -> 'chased',
            NP -> D N, D -> 'the', N -> 'cat']

        :rtype: list(Production)
        """

        if not isinstance(self._labels, string_types):
            raise TypeError(
                'Productions can only be generated from trees having node labels that are strings')

        prods = [Production(Nonterminal(self._labels), _child_names(self))]
        for child in self:
            if isinstance(child, NodeTree):
                prods += child.productions()
        return prods

    def is_parent_of(self, child):
        p_path = self.treeposition()
        c_path = child.treeposition()
        if len(p_path) < len(c_path):
            if p_path == c_path[:len(p_path)]:
                return True
        return False

    @staticmethod
    def is_order(node_list: List, acceptParentChid=False, acceptSameNode=False):
        if not isinstance(node_list, list):
            raise TypeError("1th param should be list")
        if len(node_list) < 2:
            raise ValueError("1th param should be a list that has at least 2 items")
        last_node = node_list[0]
        for cur_node in node_list[1:]:
            # 俩节点都不是一棵树上的，没有可比性，退出
            if last_node.root() != cur_node.root():
                return False
            # 俩节点逆序
            if last_node.treeposition() > cur_node.treeposition():
                return False
            # 俩节点是同一个
            if last_node.treeposition() == cur_node.treeposition():
                if acceptSameNode == True:
                    pass
                else:
                    return False
            # 俩节点是父子
            if last_node.is_parent_of(cur_node):
                if acceptParentChid == True:
                    pass
                else:
                    return False
        return True

    # leaves --------------------------------------------------
    def all_leaves(self):
        """获取所有叶子。
        Return the leaves of the tree.

            >>> t = Tree.fromstring("(S (NP (D the) (N dog)) (VP (V chased) (NP (D the) (N cat))))")
            >>> t.leaves()
            ['the', 'dog', 'chased', 'the', 'cat']

        :return: a list containing this tree's leaves.
            The order reflects the order of the
            leaves in the tree's hierarchical structure.
        :rtype: list
        """
        leaves = []
        for child in self:
            if isinstance(child, NodeTree):
                leaves.extend(child.leaves())
            else:
                leaves.append(child)
        return leaves
    leaves = all_leaves

    def text(self):
        t = ""
        for i in self:
            if isinstance(i, NodeTree):
                t = t + i.text()
            else:
                t = t + str(i)
        return t


    def all_leaves_label(self) -> List[Tuple]:
        """返回叶子节点的标签，nltk中叶子节点的标签都是POS标签，所以就是返回POS标签。
        Return a sequence of pos-tagged words extracted from the tree.

        example::
            >>> t = Tree.fromstring("(S (NP (D the) (N dog)) (VP (V chased) (NP (D the) (N cat))))")
            >>> t.pos()
            [('the', 'D'), ('dog', 'N'), ('chased', 'V'), ('the', 'D'), ('cat', 'N')]

        :return: a list of tuples containing leaves and pre-terminals (part-of-speech tags).
            The order reflects the order of the leaves in the tree's hierarchical structure.
        """
        pos = []
        for child in self:
            if isinstance(child, NodeTree):
                pos.extend(child.pos())
            else:
                pos.append((child, self._labels))
        return pos
    pos = all_leaves_label

    def all_leaves_position(self) -> List[Tuple]:
        """获取所有叶子的路径。

        example::
            >>> t = NodeTree.fromstring("(S (NP (D the) (N dog)) (VP (V chased) (NP (D the) (N cat))))")
            >>> t.treepositions('leaves')
            [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 0, 0), (1, 1, 1, 0)]

        :param order: One of: ``preorder``先序遍历, ``postorder``后序遍历,
         ``bothorder``中序遍历,``leaves``只遍历叶子.
        :return: A list of node path. The path is given in tuple form.
        """
        return self.treepositions(order="leaves")
    leaves_position = all_leaves_position

    def ith_leaf_position(self, index: int) -> Tuple:
        """获得第index个叶子的路径。
        Return the tree position of the ``index``-th leaf in this
        tree.  I.e., if ``tp=self.leaf_treeposition(i)``, then
        ``self[tp]==self.leaves()[i]``.

        example::
            >>> t = NodeTree.fromstring("(S (NP (D the) (N dog)) (VP (V chased) (NP (D the) (N cat))))")
            >>> t.leaf_treeposition(index=3)
            (1, 1, 0, 0)

        :return: The position of index-th leaf.

        :raise IndexError: If this tree contains fewer than ``index+1``
            leaves, or if ``index<0``.
        """
        if index < 0: raise IndexError('index must be non-negative')

        stack = [(self, ())]
        while stack:
            value, treepos = stack.pop()
            if not isinstance(value, NodeTree):
                if index == 0: return treepos
                else: index -= 1
            else:
                for i in range(len(value)-1, -1, -1):
                    stack.append( (value[i], treepos+(i,)) )

        raise IndexError('index must be less than or equal to len(self)')
    leaf_treeposition = ith_leaf_position

    def spanning_leaves_position(self, start, end):
        """即self.leaves()[start:end]。
        :return: The tree position of the lowest descendant of this
            tree that dominates ``self.leaves()[start:end]``.
        :raise ValueError: if ``end <= start``
        """
        if end <= start:
            raise ValueError('end must be greater than start')
        # Find the tree positions of the start & end leaves, and
        # take the longest common subsequence.
        start_treepos = self.leaf_treeposition(start)
        end_treepos = self.leaf_treeposition(end-1)
        # Find the first index where they mismatch:
        for i in range(len(start_treepos)):
            if i == len(end_treepos) or start_treepos[i] != end_treepos[i]:
                return start_treepos[:i]
        return start_treepos
    treeposition_spanning_leaves = spanning_leaves_position

    # nleaves ------------------------------------------------
    def all_nleaves(self) -> List["NodeTree"]:
        nleaves = []
        for child in self:
            if isinstance(child, NodeTree):
                nleaves.extend(child.all_nleaves())
        # 没有孩子，或所有孩子都不是树，那么就是nleaf
        if nleaves == []:
            return [self]
        # 至少有一个孩子是树，那么就不是nleaf
        else:
            return nleaves

    def is_nleaf(self):
        for child in self:
            if isinstance(child, NodeTree):
               return False
        return True

    def right_nleaf(self):
        cur_node = self
        while not cur_node.is_nleaf():
            cur_node = cur_node[-1]
        return cur_node

    def left_nleaf(self):
        cur_node = self
        while not cur_node.is_nleaf():
            cur_node = cur_node[0]
        return cur_node

    @staticmethod
    def nleaf_in_margin(left_margin: "NodeTree", right_margin: "NodeTree", include_margin=1) -> "NodeTree":
        """获取两个节点之间的nleaf列表
        example::

            s{
                a1{
                    f1
                    f2
                    f3
                }
                a2{
                    f4
                    f5
                }
                a3{
                    f6
                    f7
                    f8
                }
            }
            >>> s.nleaf_in_margin(a1, a3, include_margin=3)
            [f1, f2, f3, f4, f5, f6, f7, f8]
            >>> s.nleaf_in_margin(a1, a3, include_margin=2)
            [f3, f4, f5, f6]
            >>> s.nleaf_in_margin(a1, a3, include_margin=1)
            [f4, f5]

        :param left_margin:
        :param right_margin:
        :param include_margin:
        :return:
        """
        # 参数检测：参数类型
        if not isinstance(left_margin, NodeTree):
            raise TypeError("margin1 should be ntree")
        if not isinstance(right_margin, NodeTree):
            raise TypeError("margin2 should be ntree")
        # 参数检测：左右margin是否同树
        if left_margin.root() != right_margin.root():
            raise RuntimeError("the 2 margins should be of the same tree.")
        # 数据准备：获取左右nleaf
        if include_margin == 1 or include_margin == 2:
            left_nleaf = left_margin.right_nleaf()
            right_nleaf = right_margin.left_nleaf()
        if include_margin == 3:
            left_nleaf = left_margin.left_nleaf()
            right_nleaf = right_margin.right_nleaf()
        left_nleaf_position = left_nleaf.position()
        right_nleaf_position = right_nleaf.position()
        # 核心逻辑
        if NodeTree.is_order([left_nleaf, right_nleaf], acceptSameNode=True):
            within_nleaf_list :List["NodeTree"]= []
            cur_nleaf = left_nleaf.right_sibling(acceptCousin=True).left_nleaf()
            while NodeTree.is_order([left_nleaf, cur_nleaf, right_nleaf], acceptSameNode=False):
                within_nleaf_list.append(cur_nleaf)
                cur_nleaf = cur_nleaf.right_sibling(acceptCousin=True).left_nleaf()
            if include_margin == 3 or include_margin == 2:
                within_nleaf_list.insert(0, left_nleaf)
                within_nleaf_list.append(right_nleaf)
            elif include_margin ==1:
                pass
            return within_nleaf_list
        else:
            raise RuntimeError("顺序不对")

    # 智能操作-----------------------------------------------------------
    @staticmethod
    def add_parent(label, node_list: List["NodeTree"]):
        # 类型检测
        if not isinstance(node_list, list):
            raise TypeError('1th param should be a list of tree node')
        for cur_node in node_list:
            if not isinstance(cur_node, NodeTree):
                raise TypeError('item in list should be tree node')
        if len(node_list) < 1:
            raise TypeError('node_list should has at least one item')

        # 遍历node_list，输出parent_list
        parent_list = []
        for cur_node in node_list:
            # 如果当前节点被cover,就跳过当前节点
            if len(parent_list) > 0:
                if parent_list[-1].is_parent_of(cur_node):
                    continue
            # 逐渐追溯当前节点的祖先
            cur_child = cur_node
            cur_parent = cur_child.get_parent()
            while cur_parent is not None:  # cur_parent为None说明cur_node已经是root了。
                # 如果当前节点不是它祖宗的长孙
                if cur_parent[0] != cur_child:
                    # cur_parent不被认可
                    parent_list.append(cur_child)
                    if len(parent_list) >= 2:
                        if parent_list[-1].parent() != parent_list[-2].parent():
                            raise RuntimeError("can not add parent")
                    # 退出寻祖
                    break
                # 如果祖宗节点能cover最右兄弟
                elif NodeTree.is_order([node_list[-1].right_nleaf(), cur_parent.right_nleaf()]):
                    # cur_parent不被认可
                    parent_list.append(cur_child)
                    if len(parent_list) >= 2:
                        if parent_list[-1].parent() != parent_list[-2].parent():
                            raise RuntimeError("can not add parent")
                    # 退出寻祖
                    break
                # 如果最右兄弟正好是祖宗节点的历代老幺
                elif node_list[-1].right_nleaf() == cur_parent.right_nleaf():
                    # cur_parent被认可
                    parent_list.append(cur_parent)
                    if len(parent_list) >= 2:
                        if parent_list[-1].parent() != parent_list[-2].parent():
                            raise RuntimeError("can not add parent")
                    # 退出寻祖
                    break
                # 如果祖宗节点不能cover最右兄弟
                else:
                    # 继续寻祖
                    cur_child = cur_parent
                    cur_parent = cur_parent.parent()

        # parent_list中节点断开和他们旧爸爸的关系
        old_parent = parent_list[0].get_parent()
        index = parent_list[0].parent_index()
        for cur_child in parent_list:
            old_parent.remove(cur_child)
        # parent_list中节点认新爸爸
        new_parent = NodeTree(label, parent_list)
        # 新爸爸的爸爸是旧爸爸
        if index == len(old_parent):
            old_parent.append(new_parent)
        else:
            old_parent.insert(index, new_parent)
        #
        return new_parent

    @staticmethod
    def get_shared_parent(node_list :List["NodeTree"] = None, node_position_list = None):
        # 参数检测
        if node_list is not None:
            if isinstance(node_list, list):
                raise TypeError
        else:
            if isinstance(node_position_list, list):
                raise  TypeError
        # 数据准备
        if node_list is not None:
            node_position_list = [i.position() for i in node_list]
        min_position_lenth = min([len(i) for i in node_position_list])
        # 核心逻辑
        for i in range(0, min_position_lenth-1):
            for cur_node_index in range(0, len(node_position_list)-2):
                cur_position = node_position_list[cur_node_index]
                next_position = node_position_list[cur_node_index + 1]
                if cur_position[i] != next_position[i]:
                    return node_position_list[0][:i-1]

    @staticmethod
    def is_annotated(root: "NodeTree", start_nleaf_position, end_nleaf_positon):
        # 类型检测
        pass
        # 根据position获取nleaf
        start_nleaf = root[start_nleaf_position]
        end_nleaf = root[end_nleaf_positon]
        # 判断：如果是单个节点
        if start_nleaf == end_nleaf:
            return start_nleaf
        # 判断：如果是多个节点
        cur_parent = start_nleaf
        while cur_parent != root:
            cur_parent = cur_parent.get_parent()
            if cur_parent.left_nleaf() != start_nleaf:
                return None
            if cur_parent.right_nleaf() == end_nleaf:
                return cur_parent
        return None

    # Transforms------------------------------------------------------
    def chomsky_normal_form(self, factor="right", horzMarkov=None, vertMarkov=0, childChar="|", parentChar="^"):
        """
        This method can modify a tree in three ways:

          1. Convert a tree into its Chomsky Normal Form (CNF)
             equivalent -- Every subtree has either two non-terminals
             or one terminal as its children.  This process requires
             the creation of more"artificial" non-terminal nodes.
          2. Markov (vertical) smoothing of children in new artificial
             nodes
          3. Horizontal (parent) annotation of nodes

        :param factor: Right or left factoring method (default = "right")
        :type  factor: str = [left|right]
        :param horzMarkov: Markov order for sibling smoothing in artificial nodes (None (default) = include all siblings)
        :type  horzMarkov: int | None
        :param vertMarkov: Markov order for parent smoothing (0 (default) = no vertical annotation)
        :type  vertMarkov: int | None
        :param childChar: A string used in construction of the artificial nodes, separating the head of the
                          original subtree from the child nodes that have yet to be expanded (default = "|")
        :type  childChar: str
        :param parentChar: A string used to separate the node representation from its vertical annotation
        :type  parentChar: str
        """
        from nltk.treetransforms import chomsky_normal_form
        chomsky_normal_form(self, factor, horzMarkov, vertMarkov, childChar, parentChar)

    def un_chomsky_normal_form(self, expandUnary = True, childChar = "|", parentChar = "^", unaryChar = "+"):
        """
        This method modifies the tree in three ways:

          1. Transforms a tree in Chomsky Normal Form back to its
             original structure (branching greater than two)
          2. Removes any parent annotation (if it exists)
          3. (optional) expands unary subtrees (if previously
             collapsed with collapseUnary(...) )

        :param expandUnary: Flag to expand unary or not (default = True)
        :type  expandUnary: bool
        :param childChar: A string separating the head node from its children in an artificial node (default = "|")
        :type  childChar: str
        :param parentChar: A sting separating the node label from its parent annotation (default = "^")
        :type  parentChar: str
        :param unaryChar: A string joining two non-terminals in a unary production (default = "+")
        :type  unaryChar: str
        """
        from nltk.treetransforms import un_chomsky_normal_form
        un_chomsky_normal_form(self, expandUnary, childChar, parentChar, unaryChar)

    def collapse_unary(self, collapsePOS = False, collapseRoot = False, joinChar = "+"):
        """
        Collapse subtrees with a single child (ie. unary productions)
        into a new non-terminal (Tree node) joined by 'joinChar'.
        This is useful when working with algorithms that do not allow
        unary productions, and completely removing the unary productions
        would require loss of useful information.  The Tree is modified
        directly (since it is passed by reference) and no value is returned.

        :param collapsePOS: 'False' (default) will not collapse the parent of leaf nodes (ie.
                            Part-of-Speech tags) since they are always unary productions
        :type  collapsePOS: bool
        :param collapseRoot: 'False' (default) will not modify the root production
                             if it is unary.  For the Penn WSJ treebank corpus, this corresponds
                             to the TOP -> productions.
        :type collapseRoot: bool
        :param joinChar: A string used to connect collapsed node values (default = "+")
        :type  joinChar: str
        """
        from nltk.treetransforms import collapse_unary
        collapse_unary(self, collapsePOS, collapseRoot, joinChar)

    # Convert, copy-------------------------------------------------
    @classmethod
    def convert(cls, tree):
        """
        Convert a tree between different subtypes of Tree.  ``cls`` determines
        which class will be used to encode the new tree.

        :type tree: Tree
        :param tree: The tree that should be converted.
        :return: The new Tree.
        """
        if isinstance(tree, NodeTree):
            children = [cls.convert(child) for child in tree]
            return cls(tree._labels, children)
        else:
            return tree

    def copy(self, deep=False):
        if not deep: return type(self)(self._labels, self)
        else: return type(self).convert(self)

    def readable(self, nolink=False):
        output_dict = {}
        if nolink == True:
            output_dict.update(self.labels.readable(nolink=True))
        else:
            output_dict.update(self.labels.readable())
        output_dict["parent_position"] = self.get_parent().position(output_type="string")
        output_dict["position"] = self.position(output_type="string")
        output_dict["text"] = "".join(self.all_leaves())
        return output_dict


    def to_info(self):
        output_dict = {}
        output_dict["parent"] = ''
        if self.get_parent() is not None:
            output_dict["parent"] = self.get_parent().position(output_type="string")
        output_dict["position"] = self.position(output_type="string")
        output_dict["child"] = []
        for cur_child in self:
            if isinstance(cur_child, str):
                output_dict["child"].append(cur_child)
            elif isinstance(cur_child, NodeTree):
                output_dict["child"].append(cur_child.position())
        output_dict["labels"] = {}
        if nolink == True:
            output_dict["labels"].update(self.labels.readable(nolink=True))
        else:
            output_dict["labels"].update(self.labels.readable())
        return output_dict

    @classmethod
    def from_info(cls, root_node, info):
        """
        Json to obj

        :param root_node: The root node of the nood tree, used to locate target node by position.
          If *root_node* is None, *info* is the whole node tree, that means the first
          element in *info* represent the first node.
        :param info:
        :return: A NodeTree obj
        """
        # param check
        if root_node is not None:
            if isinstance(root_node, NodeTree):
                raise TypeError

        node = NodeTree(labels=None, Children=None)

        if root_node is None:
            root_node = node

        # parent
        if root_node is None:
            node._parent = None
        else:
            parent_node = root_node[tuple(info["parent"])]
            parent_node.append(node)

        # children
        """do not care *children*, we deal with *parent* only, cause the two are the same thing"""

        # labels
        from nlp_platform.center.labels import NodeLabels
        node._labels = NodeLabels(owner=node, labels_dict=info["labels"])

    # Parsing-------------------------------------------------------
    @classmethod
    def fromstring(cls, s, brackets='()', read_node=None, read_leaf=None,
              node_pattern=None, leaf_pattern=None,
              remove_empty_top_bracketing=False):
        """
        Read a bracketed tree string and return the resulting tree.
        Trees are represented as nested brackettings, such as::

          (S (NP (NNP John)) (VP (V runs)))

        :type s: str
        :param s: The string to read

        :type brackets: str (length=2)
        :param brackets: The bracket characters used to mark the
            beginning and end of trees and subtrees.

        :type read_node: function
        :type read_leaf: function
        :param read_node, read_leaf: If specified, these functions
            are applied to the substrings of ``s`` corresponding to
            nodes and leaves (respectively) to obtain the values for
            those nodes and leaves.  They should have the following
            signature:

               read_node(str) -> value

            For example, these functions could be used to process nodes
            and leaves whose values should be some type other than
            string (such as ``FeatStruct``).
            Note that by default, node strings and leaf strings are
            delimited by whitespace and brackets; to override this
            default, use the ``node_pattern`` and ``leaf_pattern``
            arguments.

        :type node_pattern: str
        :type leaf_pattern: str
        :param node_pattern, leaf_pattern: Regular expression patterns
            used to find node and leaf substrings in ``s``.  By
            default, both nodes patterns are defined to match any
            sequence of non-whitespace non-bracket characters.

        :type remove_empty_top_bracketing: bool
        :param remove_empty_top_bracketing: If the resulting tree has
            an empty node label, and is length one, then return its
            single child instead.  This is useful for treebank trees,
            which sometimes contain an extra level of bracketing.

        :return: A tree corresponding to the string representation ``s``.
            If this class method is called using a subclass of Tree,
            then it will return a tree of that type.
        :rtype: Tree
        """
        if not isinstance(brackets, string_types) or len(brackets) != 2:
            raise TypeError('brackets must be a length-2 string')
        if re.search('\s', brackets):
            raise TypeError('whitespace brackets not allowed')
        # Construct a regexp that will tokenize the string.
        open_b, close_b = brackets
        open_pattern, close_pattern = (re.escape(open_b), re.escape(close_b))
        if node_pattern is None:
            node_pattern = '[^\s%s%s]+' % (open_pattern, close_pattern)
        if leaf_pattern is None:
            leaf_pattern = '[^\s%s%s]+' % (open_pattern, close_pattern)
        token_re = re.compile('%s\s*(%s)?|%s|(%s)' % (
            open_pattern, node_pattern, close_pattern, leaf_pattern))
        # Walk through each token, updating a stack of trees.
        stack = [(None, [])] # list of (node, children) tuples
        for match in token_re.finditer(s):
            token = match.group()
            # Beginning of a tree/subtree
            if token[0] == open_b:
                if len(stack) == 1 and len(stack[0][1]) > 0:
                    cls._parse_error(s, match, 'end-of-string')
                label = token[1:].lstrip()
                if read_node is not None: label = read_node(label)
                stack.append((label, []))
            # End of a tree/subtree
            elif token == close_b:
                if len(stack) == 1:
                    if len(stack[0][1]) == 0:
                        cls._parse_error(s, match, open_b)
                    else:
                        cls._parse_error(s, match, 'end-of-string')
                label, children = stack.pop()
                stack[-1][1].append(cls(label, children))
            # Leaf node
            else:
                if len(stack) == 1:
                    cls._parse_error(s, match, open_b)
                if read_leaf is not None: token = read_leaf(token)
                stack[-1][1].append(token)

        # check that we got exactly one complete tree.
        if len(stack) > 1:
            cls._parse_error(s, 'end-of-string', close_b)
        elif len(stack[0][1]) == 0:
            cls._parse_error(s, 'end-of-string', open_b)
        else:
            assert stack[0][0] is None
            assert len(stack[0][1]) == 1
        tree = stack[0][1][0]

        # If the tree has an extra level with node='', then get rid of
        # it.  E.g.: "((S (NP ...) (VP ...)))"
        if remove_empty_top_bracketing and tree._labels == '' and len(tree) == 1:
            tree = tree[0]
        # return the tree.
        return tree

    @classmethod
    def _parse_error(cls, s, match, expecting):
        """
        Display a friendly error message when parsing a tree string fails.
        :param s: The string we're parsing.
        :param match: regexp match of the problem token.
        :param expecting: what we expected to see instead.
        """
        # Construct a basic error message
        if match == 'end-of-string':
            pos, token = len(s), 'end-of-string'
        else:
            pos, token = match.start(), match.group()
        msg = '%s.read(): expected %r but got %r\n%sat index %d.' % (
            cls.__name__, expecting, token, ' '*12, pos)
        # Add a display showing the error token itsels:
        s = s.replace('\n', ' ').replace('\t', ' ')
        offset = pos
        if len(s) > pos+10:
            s = s[:pos+10]+'...'
        if pos > 10:
            s = '...'+s[pos-10:]
            offset = 13
        msg += '\n%s"%s"\n%s^' % (' '*16, s, ' '*(17+offset))
        raise ValueError(msg)

    # Visualization & String Representation---------------------------

    def draw(self):
        """
        Open a new window containing a graphical diagram of this tree.
        """
        from nltk.draw.tree import draw_trees
        draw_trees(self)

    def pretty_print(self, sentence=None, highlight=(), stream=None, **kwargs):
        """
        Pretty-print this tree as ASCII or Unicode art.
        For explanation of the arguments, see the documentation for
        `nltk.treeprettyprinter.TreePrettyPrinter`.
        """
        from nltk.treeprettyprinter import TreePrettyPrinter
        print(TreePrettyPrinter(self, sentence, highlight).text(**kwargs),
              file=stream)

    def __repr__(self):
        childstr = ", ".join(unicode_repr(c) for c in self)
        return '%s(%s, [%s])' % (type(self).__name__, unicode_repr(self._labels), childstr)

    def _repr_png_(self):
        """
        Draws and outputs in PNG for ipython.
        PNG is used instead of PDF, since it can be displayed in the qt console and
        has wider browser support.
        """
        import os
        import base64
        import subprocess
        import tempfile
        from nltk.draw.tree import tree_to_treesegment
        from nltk.draw.util import CanvasFrame
        from nltk.internals import find_binary
        _canvas_frame = CanvasFrame()
        widget = tree_to_treesegment(_canvas_frame.canvas(), self)
        _canvas_frame.add_widget(widget)
        x, y, w, h = widget.bbox()
        # print_to_file uses scrollregion to set the width and height of the pdf.
        _canvas_frame.canvas()['scrollregion'] = (0, 0, w, h)
        with tempfile.NamedTemporaryFile() as file:
            in_path = '{0:}.ps'.format(file.name)
            out_path = '{0:}.png'.format(file.name)
            _canvas_frame.print_to_file(in_path)
            _canvas_frame.destroy_widget(widget)
            subprocess.call([find_binary('gs', binary_names=['gswin32c.exe', 'gswin64c.exe'], env_vars=['PATH'], verbose=False)] +
                            '-q -dEPSCrop -sDEVICE=png16m -r90 -dTextAlphaBits=4 -dGraphicsAlphaBits=4 -dSAFER -dBATCH -dNOPAUSE -sOutputFile={0:} {1:}'
                            .format(out_path, in_path).split())
            with open(out_path, 'rb') as sr:
                res = sr.read()
            os.remove(in_path)
            os.remove(out_path)
            return base64.b64encode(res).decode()

    def __str__(self):
        return self.pformat()

    def pprint(self, **kwargs):
        """
        Print a string representation of this Tree to 'stream'
        """

        if "stream" in kwargs:
            stream = kwargs["stream"]
            del kwargs["stream"]
        else:
            stream = None
        print(self.pformat(**kwargs), file=stream)

    def pformat(self, margin=70, indent=0, nodesep='', parens='()', quotes=False):
        """
        :return: A pretty-printed string representation of this tree.
        :rtype: str
        :param margin: The right margin at which to do line-wrapping.
        :type margin: int
        :param indent: The indentation level at which printing
            begins.  This number is used to decide how far to indent
            subsequent lines.
        :type indent: int
        :param nodesep: A string that is used to separate the node
            from the children.  E.g., the default value ``':'`` gives
            trees like ``(S: (NP: I) (VP: (V: saw) (NP: it)))``.
        """

        # Try writing it on one line.
        s = self._pformat_flat(nodesep, parens, quotes)
        if len(s) + indent < margin:
            return s

        # If it doesn't fit on one line, then write it on multi-lines.
        if isinstance(self._labels, string_types):
            s = '%s%s%s' % (parens[0], self._labels, nodesep)
        else:
            s = '%s%s%s' % (parens[0], unicode_repr(self._labels), nodesep)
        for child in self:
            if isinstance(child, NodeTree):
                s += '\n'+' '*(indent+2)+child.pformat(margin, indent+2,
                                                  nodesep, parens, quotes)
            elif isinstance(child, tuple):
                s += '\n'+' '*(indent+2)+ "/".join(child)
            elif isinstance(child, string_types) and not quotes:
                s += '\n'+' '*(indent+2)+ '%s' % child
            else:
                s += '\n'+' '*(indent+2)+ unicode_repr(child)
        return s+parens[1]

    def pformat_latex_qtree(self):
        r"""
        Returns a representation of the tree compatible with the
        LaTeX qtree package. This consists of the string ``\Tree``
        followed by the tree represented in bracketed notation.

        For example, the following result was generated from a parse tree of
        the sentence ``The announcement astounded us``::

          \Tree [.I'' [.N'' [.D The ] [.N' [.N announcement ] ] ]
              [.I' [.V'' [.V' [.V astounded ] [.N'' [.N' [.N us ] ] ] ] ] ] ]

        See http://www.ling.upenn.edu/advice/latex.html for the LaTeX
        style file for the qtree package.

        :return: A latex qtree representation of this tree.
        :rtype: str
        """
        reserved_chars = re.compile('([#\$%&~_\{\}])')

        pformat = self.pformat(indent=6, nodesep='', parens=('[.', ' ]'))
        return r'\Tree ' + re.sub(reserved_chars, r'\\\1', pformat)

    def _pformat_flat(self, nodesep, parens, quotes):
        childstrs = []
        for child in self:
            if isinstance(child, NodeTree):
                childstrs.append(child._pformat_flat(nodesep, parens, quotes))
            elif isinstance(child, tuple):
                childstrs.append("/".join(child))
            elif isinstance(child, string_types) and not quotes:
                childstrs.append('%s' % child)
            else:
                childstrs.append(unicode_repr(child))
        if isinstance(self._labels, string_types):
            return '%s%s%s %s%s' % (parens[0], self._labels, nodesep,
                                    " ".join(childstrs), parens[1])
        else:
            return '%s%s%s %s%s' % (parens[0], unicode_repr(self._labels), nodesep,
                                    " ".join(childstrs), parens[1])

    # statistic------------------------------------------------------
    def statistic(self, ifprint=False):
        wp = self.walk_position()
        node_num = len(wp)
        if ifprint == True:
            print("node_num:", node_num)
        return {"node_num": node_num}

    # 兼容nltk.tree


def _child_names(tree):
    names = []
    for child in tree:
        if isinstance(child, NodeTree):
            names.append(Nonterminal(child._labels))
        else:
            names.append(child)
    return names

## Parsing ------------------------------------------------------------
def bracket_parse(s):
    """
    Use Tree.read(s, remove_empty_top_bracketing=True) instead.
    """
    raise NameError("Use Tree.read(s, remove_empty_top_bracketing=True) instead.")

def sinica_parse(s):
    """
    Parse a Sinica Treebank string and return a tree.  Trees are represented as nested brackettings,
    as shown in the following example (X represents a Chinese character):
    S(goal:NP(Head:Nep:XX)|theme:NP(Head:Nhaa:X)|quantity:Dab:X|Head:VL2:X)#0(PERIODCATEGORY)

    :return: A tree corresponding to the string representation.
    :rtype: Tree
    :param s: The string to be converted
    :type s: str
    """
    tokens = re.split(r'([()| ])', s)
    for i in range(len(tokens)):
        if tokens[i] == '(':
            tokens[i-1], tokens[i] = tokens[i], tokens[i-1]     # pull nonterminal inside parens
        elif ':' in tokens[i]:
            fields = tokens[i].split(':')
            if len(fields) == 2:                                # non-terminal
                tokens[i] = fields[1]
            else:
                tokens[i] = "(" + fields[-2] + " " + fields[-1] + ")"
        elif tokens[i] == '|':
            tokens[i] = ''

    treebank_string = " ".join(tokens)
    return NodeTree.fromstring(treebank_string, remove_empty_top_bracketing=True)
