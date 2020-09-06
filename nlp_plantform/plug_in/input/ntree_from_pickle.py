from nlp_plantform.center.nodetree import NodeTree
import _pickle as cPickle


def input_ntree_from_pickle(path: str ='data/ntree.pkl') -> NodeTree:
    with open(path, 'wb') as pkl_file:
        ntree = cPickle.load(pkl_file)
    return ntree