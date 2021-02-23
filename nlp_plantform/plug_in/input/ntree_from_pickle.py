from nlp_plantform.config import data_path
from nlp_plantform.center.nodetree import NodeTree
import _pickle as cPickle
from nlp_plantform.center.labeltypes import regiest_cofigured_label_types

def input_ntree_from_pickle(path: str = data_path+ r'\ntree.pkl') -> NodeTree:
    regiest_cofigured_label_types()
    with open(path, 'rb') as pkl_file:
        ntree = cPickle.load(pkl_file)
    return ntree