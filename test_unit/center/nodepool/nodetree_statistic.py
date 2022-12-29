from nlp_platform.center.config import data_path
from nlp_platform.plug_in.input.ntree_from_pickle import input_ntree_from_pickle
from nlp_platform.center.labeltypes import regiest_cofigured_label_types

regiest_cofigured_label_types()
# input
nodetree = input_ntree_from_pickle(data_path+ r'\ntree.pkl')
# statistic
nodetree.statistic(ifprint=True)
