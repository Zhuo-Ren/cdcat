from nlp_plantform.center.layer_tree_node import LayerTreeNode

class LangNode(LayerTreeNode):
    # 静态数据成员
    config = None

    @staticmethod
    def read_config(config_path = None):
        # 读取配置文件
        if config_path is not None:
            """读取配置文件"""
            pass
        else:
            LangNode.config = {
                'type_def': {
                    'corpus': ['absolutePath'],
                    'folder': ['folderIndex'],
                    'doc': ['docIndex'],
                    'para': ['paraIndex'],
                    'sentence': ['sentenceIndex'],
                    'token': ['tokenIndex'],
                    'char': ['charIndex']
                }
        }

    @staticmethod
    def is_config(self):
        if LangNode.config is not None:
            return True
        else:
            return False

    def __init__(self):
        # 动态数据成员
        self.resource = None
        self.time = None

    def add_type(self, types):
        # for type in types:
        #     if type in LayerTree.type_define
        #         self.__setattr__()
        #         self.__setattr__
        pass
