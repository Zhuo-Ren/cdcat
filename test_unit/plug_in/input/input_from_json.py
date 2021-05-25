from nlp_platform.center.corpus import Corpus
from nlp_platform.center.node import Node
from nlp_platform.center.instance import Instance
from nlp_platform.center.instancepool import InstancePool
from nlp_platform.center.nodepool import NodePool
from nlp_platform.center.tablepool import TablePool

import json
import os

from nlp_platform.plug_in.input.from_files import from_files
c = from_files(file_dir="../output")
