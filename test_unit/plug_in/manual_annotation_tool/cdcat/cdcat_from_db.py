"""
This is a integration test file.
This program:
 1. get nodetree from a sqlite file.
 2. get instances from a new empty Instances object.
 3. annotate with CDCAT
"""
from nlp_plantform.config import data_path
from nlp_plantform.center.instancepool import InstancePool
from nlp_plantform.plug_in.input.ntree_from_sqlite import input_ntree_from_sqlite
from nlp_plantform.plug_in.manual_annotation_tool.cdcat.cdcat import cdcat


# input
ntree = input_ntree_from_sqlite(data_path + "\main.sqlite", "websiteTabel")  # 爬虫中table笔误写成了tabel
instances = InstancePool()

# annotate those text with CDCAT
cdcat(ntree, instances, {"article": True})
