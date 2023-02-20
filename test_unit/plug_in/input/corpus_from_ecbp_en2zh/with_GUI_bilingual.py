import sys
root_path = r"E:\ProgramCode\cdcat"
sys.path.append(root_path)
import nlp_platform.center.config_log
import logging
from nlp_platform.plug_in.input.corpus_from_ecbp_en2zh import corpus_from_ecbp_en2zh


def import_config():
    """ 读取核心配置load center config """
    import os
    center_config_dir = "config_label.json"
    cur_file_path = os.path.abspath(__file__)
    cur_folder_path = os.path.dirname(cur_file_path)
    center_config_dir = os.path.join(cur_folder_path, center_config_dir)
    from nlp_platform.center.config import Config
    Config.load_config(config_name="center_config", config_dir=center_config_dir)


def test_corpus_from_ecbp_en2zh():
    import_config()
    #
    c = corpus_from_ecbp_en2zh(
        ecbp_en2zh_path=root_path + r"\test_unit\plug_in\input\corpus_from_ecbp_en2zh\corpus\ECBplusEnZh",
        csv_path=root_path + r"\test_unit\plug_in\input\corpus_from_ecbp_en2zh\corpus\ECBplus_coreference_sentences.csv",
        mapping_pkl_path=root_path + r"\test_unit\plug_in\input\corpus_from_ecbp_en2zh\corpus\save.pkl"
    )
    # show
    from nlp_platform.plug_in.manual_annotation_tool.cdcat.cdcat import cdcat
    cdcat(c,
          path_to_label_config=root_path + r"\test_unit\plug_in\input\corpus_from_ecbp_en2zh\config_cdcat_label.json",
          path_to_core_config=root_path + r"\test_unit\plug_in\input\corpus_from_ecbp_en2zh\config_cdcat_core.json")

test_corpus_from_ecbp_en2zh()