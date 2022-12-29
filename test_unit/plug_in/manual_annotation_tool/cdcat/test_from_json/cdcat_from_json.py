import os

# center config
center_config_dir = "config_label.json"
# load center config
cur_file_path = os.path.abspath(__file__)
cur_folder_path = os.path.dirname(cur_file_path)
center_config_dir = os.path.join(cur_folder_path, center_config_dir)
from nlp_platform.center.config import Config
Config.load_config(config_name="center_config", config_dir=center_config_dir)

# create corpus
from nlp_platform.plug_in.input.from_files import from_files
c = from_files(dir="./corpus")

# annotation
from nlp_platform.plug_in.manual_annotation_tool.cdcat.cdcat import cdcat
cdcat(c)


