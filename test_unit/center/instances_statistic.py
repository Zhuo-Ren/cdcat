from nlp_plantform.config import data_path
from nlp_plantform.plug_in.input.instances_from_pickle import input_instances_from_pickle

# input
instances = input_instances_from_pickle(data_path+ r'\instances.pkl')
# statistic
instances.statistic(ifprint=True)
