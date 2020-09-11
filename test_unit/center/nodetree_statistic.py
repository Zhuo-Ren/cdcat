from nlp_plantform.config import data_path
from nlp_plantform.plug_in.input.ntree_from_pickle import input_ntree_from_pickle

# input
nodetree = input_ntree_from_pickle(data_path+ r'\ntree.pkl')
# statistic
nodetree.statistic(ifprint=True)
