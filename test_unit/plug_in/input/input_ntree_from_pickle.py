"""
this is the unit test of input_from_pickle.
"""
from nlp_plantform.plug_in.input.ntree_from_pickle import input_ntree_from_pickle
from nlp_plantform.config import data_path

# input
r = input_ntree_from_pickle("corpus-ntree.pkl")
r[0][0].draw()