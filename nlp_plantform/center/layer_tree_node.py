from nlp_plantform.center.tree_node import TreeNode

class LayerTreeNode(TreeNode):
    # 静态数据成员
    layers = None
    config = None

    @staticmethod
    def read_config(config_path=None):
        # 读取配置文件
        if config_path is not None:
            """读取配置文件"""
            pass
        else:
            LayerTreeNode.config = {
                'layers_def': ['corpus', 'doc', 'para', 'sentence', 'token', 'char']
            }

        # 初始化层
        for layer_name in LayerTreeNode.config['layers_def']:
            LayerTreeNode.layers[layer_name] = []

    def __init__(self, layer=[]):
        # 动态数据成员
        self.brotherIndex = None
        self.layerindex = {'Token':13, 'char':56}
        self.fatherNode = None
        self.childNode = []
        self.text = ""

        # 初始化root
        root = LayerTreeNode(layers=['corpus'])
        root.father = self

    @staticmethod
    def get_node_by_path(self, path):
        pass

    @staticmethod
    def add_childnode(self, child_index=[-1], layer_list=[]):
        pass

    @staticmethod
    def add_fathernode(self, childNodeList):
        pass

    def addChildNode(self):
        def addDirectChildNode(Child_brotherIndex):
            pass

        def addDescendantCthildNode():
            pass
        
        pass

    def getChildNode(layer, dowenNth, leftMost, rightMost):
        childNodeList = None
        return childNodeList
    
    def getChildNodeAttr(layer, dowenNth, leftMost, rightMost, attr):
        childNodeList = getChildNode(layer, dowenNth, leftMost, rightMost)
        attrList = [x.getAttr(attr) for x in childNodeList]
        return attrList
        
    def getFatherNode(self):
        pass

    def getPath(upN,toLayer):
        # 返回绝对路径或相对路径
        pass

