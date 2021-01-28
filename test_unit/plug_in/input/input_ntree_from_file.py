"""
this is the unit test of input_from_file.
"""
from nlp_platform.plug_in.input.ntree_from_file import input_ntree_from_file

r = input_ntree_from_file("corpus-ntree.txt")
r.draw()
