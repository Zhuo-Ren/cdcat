"""
This is a integration test file.
This program:
 1. read raw text from a sqlite file.
 2. annotate those text with CDCAT
"""
from nlp_platform.config import data_path
from nlp_platform.plug_in.input.ntree_from_pickle import input_ntree_from_pickle
from nlp_platform.plug_in.input.instances_from_pickle import input_instances_from_pickle
from nlp_platform.plug_in.manual_annotation_tool.cdcat.cdcat import cdcat


# input
ntree = input_ntree_from_pickle(data_path + r"/ntree.pkl")
instances = input_instances_from_pickle(data_path + r"/instances.pkl")

# annotate those text with CDCAT
cdcat(ntree, instances, {"article": True})
