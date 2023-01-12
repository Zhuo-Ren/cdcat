import pytest
from nlp_platform.plug_in.input.corpus_from_ecbpxml import corpus_from_ecbpxml


class TestNodesFromEcbpXml:
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

    def test_nodes_from_ecbpxml(self, import_config):
        c = corpus_from_ecbpxml(
            ecbp_path=r"E:\ProgramCode\cdcat\test_unit\corpus\ecb+\ECBplus",
            csv_path=r"E:\ProgramCode\cdcat\test_unit\corpus\ecb+\ECBplus_coreference_sentences.csv"
        )
        """
        这一段跑不了，在pytest中跑flask需要特殊的方法。
        from nlp_platform.plug_in.manual_annotation_tool.cdcat.cdcat import cdcat
        cdcat(c,
              path_to_label_config=r"E:\ProgramCode\cdcat\test_unit\plug_in\input\nodes_from_ecbpxml\config_cdcat_label.json",
              path_to_core_config=r"E:\ProgramCode\cdcat\test_unit\plug_in\input\nodes_from_ecbpxml\config_cdcat_core.json")
        """
        assert True
