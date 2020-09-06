"""
This is a integration test file.
This program:
 1. read raw text from a sqlite file.
 2. annotate those text with CDCAT
"""
from nlp_plantform.config import data_path
from nlp_plantform.center.instances import Instances
from nlp_plantform.plug_in.input.ntree_from_sqlite import input_from_sqlite
from nlp_plantform.plug_in.manual_annotation_tool.cdcat.cdcat import cdcat
from nlp_plantform.plug_in.output.instances_to_pickle import output_instances_to_pickle
from nlp_plantform.plug_in.output.ntree_to_pickle import output_ntree_to_pickle

# input
ntree = input_from_sqlite(data_path+"\main.sqlite", "websiteTabel")  # 爬虫中table笔误写成了tabel
instances = Instances()

# annotate those text with CDCAT
cdcat(ntree, instances, {"article": True})

# output
output_ntree_to_pickle(ntree)
output_instances_to_pickle(instances)

