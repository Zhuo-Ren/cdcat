from nlp_plantform.plug_in.input.input_from_sqlite import input_from_sqlite
from nlp_plantform.plug_in.manual_annotation_tool.cdcat.cdcat import cdcat
from nlp_plantform.center.mytree import mytree
from nlp_plantform.center.instance import Instance
import logging
root = input_from_sqlite("../main.sqlite", "websiteTabel")  # 爬虫中table笔误写成了tabel

# annotation
cdcat(root, {"article":True})

