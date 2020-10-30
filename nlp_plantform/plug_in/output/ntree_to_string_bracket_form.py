from nlp_plantform.config import data_path
from nlp_plantform.center.nodetree import NodeTree
import _pickle as cPickle


def output_ntree_to_string_bracket_form(ntree: NodeTree) -> None:
    return str(ntree)
