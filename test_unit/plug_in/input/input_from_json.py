from nlp_platform.center.corpus import Corpus
from nlp_platform.center.node import Node
from nlp_platform.center.instance import Instance
from nlp_platform.center.instancepool import InstancePool
from nlp_platform.center.nodepool import NodePool
from nlp_platform.center.tablepool import TablePool

import json
import os

from nlp_platform.plug_in.input.from_files import file_to_corpus


c1 = file_to_corpus(file_dir="../../center", desc="raw")

# 创建instance和node对象，但不能存储mentions和refer标签，因为创建两个对象前后是相关的
c1 = file_to_corpus(file_dir="../../center", corpus=c1, desc="instances")
c1 = file_to_corpus(file_dir="../../center", corpus=c1, desc="nodes")

from nlp_platform.plug_in.input.from_files import create_relation_by_file

# 采用xx.instances.json创建关系
# c1 = create_relation_by_file(file_dir="../center", corpus=c1, desc="instances")
# 采用xx.nodes.json创建关系
c1 = create_relation_by_file(file_dir="../../center", corpus=c1, desc="nodes")
print(1)

