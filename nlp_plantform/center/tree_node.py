class TreeNode(object):
    # 静态成员
    pass

    def __init__(self):
        # 数据成员
        self.father = None
        self.child = []
        self.index = None
        pass

    def get_path(self):
        pass

    def add_childnode_direct(self, child_index=-1):
        """
        child_index=None，则在当前节点最后一个孩子节点后顺序添加。
        """
        pass

        pass

    def add_childnode(self,child_generation, child_index=[-1]):
        """
        添加孩子节点

        例子：
        1
            1.1
                1.1.1
                1.1.2
            1.2
                新节点
                1.2.1
                1.2.2
            1.3
        node1.add_childNode(2, [1, 0])
        """
        
        cur_node = self
        for generation_index in range(1, child_generation-1):
            cur_node = self[child_index[generation_index]]
        cur_node.add_directchildnode(child_index[child_generation])

    def getChildNode(self):
        """
        child_index=[2,0,'all']的含义是self[2][0]的所有孩子
        只有最后一个分量可以是all
        分量可以是数字，也可以是0和-1。分别代表第一个和最后一个。
        """
        pass

    def getFatherNode(self):
        pass

    def show(self):
        pass