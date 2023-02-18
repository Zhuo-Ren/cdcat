import nlp_platform.center.config_log
import logging
from nlp_platform.plug_in.input.corpus_from_ecbpxml import corpus_from_ecbpxml


def import_config():
    """ 读取核心配置load center config """
    import os
    center_config_dir = "../corpus_from_json/config_label.json"
    cur_file_path = os.path.abspath(__file__)
    cur_folder_path = os.path.dirname(cur_file_path)
    center_config_dir = os.path.join(cur_folder_path, center_config_dir)
    from nlp_platform.center.config import Config
    Config.load_config(config_name="center_config", config_dir=center_config_dir)


def test_corpus_from_ecbpxml():
    import_config()
    #
    c = corpus_from_ecbpxml(
        ecbp_path=r"E:\\ProgramCode\cdcat\test_unit\plug_in\input\corpus_from_ecbpxml\corpus\ECBplus",
        csv_path=r"E:\\ProgramCode\cdcat\test_unit\plug_in\input\corpus_from_ecbpxml\corpus\ECBplus_coreference_sentences.csv"
    )
    # show
    from nlp_platform.plug_in.manual_annotation_tool.cdcat.cdcat import cdcat
    cdcat(c,
          path_to_label_config=r"E:\\ProgramCode\cdcat\test_unit\plug_in\input\corpus_from_ecbpxml\config_cdcat_label.json",
          path_to_core_config=r"E:\\ProgramCode\cdcat\test_unit\plug_in\input\corpus_from_ecbpxml\config_cdcat_core.json")

test_corpus_from_ecbpxml()