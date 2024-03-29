"""
This is a integration test file.
This program:
 1. get nodetree from a sqlite file.
 2. get instances from a new empty Instances object.
 3. annotate with CDCAT
"""
from nlp_platform.center.config import data_path
from nlp_platform.center.instancepool import InstancePool
from nlp_platform.plug_in.input.ntree_from_sqlite import input_ntree_from_sqlite


# input
node_pool = input_ntree_from_sqlite(data_path + "/main.sqlite", "websiteTabel")  # 爬虫中table笔误写成了tabel
instance_pool = InstancePool()
relation_pool = None

# annotate those text with CDCAT
from nlp_platform.plug_in.manual_annotation_tool.cdcat.cdcat import cdcat
cdcat(node_pool, instance_pool, relation_pool)

