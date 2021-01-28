"""
this is the unit test of input_from_sqlite
"""
from nlp_platform.plug_in.input.ntree_from_sqlite import input_ntree_from_sqlite

r = input_ntree_from_sqlite("corpus-ntree.sqlite", "websiteTabel")  # 爬虫中table笔误写成了tabel
r[0][0].draw()
