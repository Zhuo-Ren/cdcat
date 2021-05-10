from nlp_platform.config import data_path
from nlp_platform.center.nodetree import NodeTree
import _pickle as cPickle


def output_ntree_to_pickle(ntree: NodeTree, path: str = data_path+r'\ntree.pkl') -> None:
    with open(path, 'wb') as pkl_file:
        cPickle.dump(ntree, pkl_file)
