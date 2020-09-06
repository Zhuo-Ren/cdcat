from nlp_plantform.config import data_path
from nlp_plantform.center.instances import Instances
import _pickle as cPickle


def input_instances_from_pickle(path: str = data_path+ r'\instances.pkl') -> Instances:
    with open(path, 'rb') as pkl_file:
        instances = cPickle.load(pkl_file)
    return instances
