from nlp_platform.center.config import data_path
from nlp_platform.center.instancepool import InstancePool
import _pickle as cPickle


def output_instances_to_pickle(instances: InstancePool, path: str = data_path + r'\instances.pkl') -> None:
    with open(path, 'wb') as pkl_file:
        cPickle.dump(instances, pkl_file)
