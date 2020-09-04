"""
This is a integration test file.
This program:
 1. read raw text from a sqlite file.
 2. annotate those text with CDCAT
"""
from nlp_plantform.plug_in.input.input_from_sqlite import input_from_sqlite
from nlp_plantform.plug_in.manual_annotation_tool.cdcat.cdcat import cdcat
from nlp_plantform.center.instances import instances

# read raw text from a sqlite file.
ntree = input_from_sqlite("../data/main.sqlite", "websiteTabel")  # 爬虫中table笔误写成了tabel
instances = instances()

# annotate those text with CDCAT
cdcat(ntree, instances, {"article": True})
