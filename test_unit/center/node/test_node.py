import pytest
import re


class TestNode:
    @pytest.fixture()
    def import_config(self):
        """ 读取核心配置load center config """
        import os
        center_config_dir = "config_label.json"
        cur_file_path = os.path.abspath(__file__)
        cur_folder_path = os.path.dirname(cur_file_path)
        center_config_dir = os.path.join(cur_folder_path, center_config_dir)
        from nlp_platform.center.config import Config
        Config.load_config(config_name="center_config", config_dir=center_config_dir)

    def test_import(self, import_config):
        """ 测试正确import instance.py """
        # 必须先导入center config，才能import Node
        "通过fixture：import_config导入配置"
        #
        from nlp_platform.center.node import Node
        # 不报错就算import成功
        assert True

    def test_init_with_default(self, import_config):
        from nlp_platform.center.node import Node
        n1 = Node()
        f = 0
        if n1.pool is not None:
            f = 1
        if re.match('n:InitId:0-0', n1['id']['value']) is None:
            f = 1
        if n1['type']['value'] != 'none':
            f = 1
        #
        assert f == 0

    def test_init_with_info(self, import_config):
        from nlp_platform.center.node import Node
        from nlp_platform.center.nodepool import NodePool
        info = {
            "id": "n:some/path:0-0;8-10",
            "type": "event"
        }
        np = NodePool()
        n1 = Node(pool=np, info=info)
        f = 0
        if n1.pool != np:
            f = "n1.pool != np"
        if n1["id"]["value"] != 'n:some/path:0-0;8-10':
            f = 'n1["id"]["value"] != "n:some/path:0-0;8-10"'
        if n1['type']['value'] != 'event':
            f = "n1['type']['value'] != 'event'"
        #
        assert f == 0

    def test_register_1(self, import_config):
        """把node_obj注册到nodepool_obj的方法1：`Node(pool=nodepool_obj)`，可以维护双向关系。"""
        from nlp_platform.center.node import Node
        from nlp_platform.center.nodepool import NodePool
        np = NodePool()
        n1 = Node(pool=np, info={"id":'n:some/path:0-0;8-10'})
        assert (('n:some/path:0-0;8-10' in n1.pool) and (n1.pool == np))

    def test_register_2(self, import_config):
        """把node_obj注册到nodepool_obj的方法2：`node_obj.pool=nodepool_obj`，只维护node_obj向nodepool_obj的关系。"""
        from nlp_platform.center.node import Node
        from nlp_platform.center.nodepool import NodePool
        np = NodePool()
        n1 = Node(info={"id":'n:some/path:0-0;8-10'})
        n1.pool = np
        assert ('n:some/path:0-0;8-10' not in n1.pool) and (n1.pool == np)

    def test_register_3(self, import_config):
        """把node_obj注册到nodepool_obj的方法3：`nodepool_obj.add(node_obj)`，可以维护双向关系。"""
        from nlp_platform.center.node import Node
        from nlp_platform.center.nodepool import NodePool
        np = NodePool()
        n1 = Node(info={"id":'n:some/path:0-0;8-10'})
        np.add(n1)
        assert (('n:some/path:0-0;8-10' in n1.pool) and (n1.pool == np))

    @pytest.mark.parametrize('node_id, node_text', [
        ["n:folder1/text1.raw.txt:0-3", "10日"],
        ["n:folder2/folder21/text5.raw.txt:1-3", "试用"],
        # ["n:folder1/text1.raw.txt:1-2;5-7", "0航一"] 暂不支持离散指称<ref20221228234911>
    ])
    def test_text(self, import_config, node_id, node_text):
        """测试node_obj.text。"""
        raw = {
            "folder1": {
                "text1.raw.txt": "10日，埃航一架飞机坠毁，事故导致机上150人全部死亡。"
            },
            "text2.raw.txt": "当日，埃航展开事故遇难者的赔偿工作",
            "folder2": {
                "text4.raw.txt": "测试用4",
                "folder21": {
                    "text5.raw.txt": "测试用5",
                    "text6.raw.txt": "测试用6"
                }
            }
        }
        from nlp_platform.center.raw import Raw
        from nlp_platform.center.corpus import Corpus
        c = Corpus()
        c.raw = Raw(raw)
        from nlp_platform.center.node import Node
        info = {"id": node_id}
        n1 = Node(info=info, pool=c.np)
        assert n1.text == node_text
