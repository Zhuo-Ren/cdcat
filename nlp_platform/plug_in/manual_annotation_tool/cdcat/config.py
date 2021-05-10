import os

root_path = os.path.abspath(os.path.dirname(__file__)).split('cdcat')[0]

lang_dict_path = r"%scdcat_systemv4/nlp_platform/plug_in/manual_annotation_tool/cdcat/config_lang_dict.json"%root_path
label_sys_dict_path = r"%scdcat_systemv4/nlp_platform/plug_in/manual_annotation_tool/cdcat/config_label_sys.json"%root_path

length_of_title = 7
allow_one_node_refer_to_more_than_one_instance = False