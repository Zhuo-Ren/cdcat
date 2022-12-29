import pytest


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
        from nlp_platform.plug_in.input.corpus_from_json import corpus_from_json
        import os
        # 获取绝对路径（因为pytest可以从dir、module、unit等多个层级进行测试，所以写相对路径是行不通的，必须转成绝对路径）
        corpus_path = "./corpus"
        cur_file_path = os.path.abspath(__file__)
        cur_folder_path = os.path.dirname(cur_file_path)
        corpus_path = os.path.join(cur_folder_path, corpus_path)
        #
        c = corpus_from_json(dir=corpus_path)
        #
        assert True  # 不报错就算成功
