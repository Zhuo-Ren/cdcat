from nlp_plantform.config import data_path
from nlp_plantform.center.instances import Instances
import _pickle as cPickle


def output_instances_to_pickle(instances: Instances, path: str =data_path+r'\instances.pkl') -> None:
    with open(path, 'wb') as pkl_file:
        cPickle.dump(instances, pkl_file)
