from nlp_plantform.config import data_path
from nlp_plantform.center.instancepool import InstancePool
import _pickle as cPickle
from nlp_plantform.center.labeltypes import regiest_cofigured_label_types


def input_instances_from_pickle(path: str = data_path+ r'\instances.pkl') -> InstancePool:
    regiest_cofigured_label_types()
    with open(path, 'rb') as pkl_file:
        instances = cPickle.load(pkl_file)
    return instances