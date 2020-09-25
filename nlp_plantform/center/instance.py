from typing import Dict, List, Tuple, Union  # for type hinting


class Instance(object):

    def __init__(self, labelsValue:Dict={}):
        from nlp_plantform.center.instancelabels import InstanceLabels
        self._labels = InstanceLabels(self, labelsValue)

    # public: labels
    @property
    def labels(self):
        return self._labels
    @labels.setter
    def labels(self, labelsValue):
        from nlp_plantform.center.instancelabels import InstanceLabels
        # 析构旧label
        del self._labels
        # 添加新label
        self._labels = InstanceLabels(labelsValue)


    def output_to_infodict(self) -> dict:
        """
        This function return labels of this instance in dict format.
        :return:
        """
        return self._labels.__str__()

