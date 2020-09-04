from typing import Dict, List, Tuple, Union  # for type hinting
from nlp_plantform.center.instance import instance


class instances(dict):
    def __init__(self):
        self.next_id = 0

    def add_instance(self, desc=None, kg=None):
        new_instance = instance(id=self.next_id, desc=desc, kg=kg)
        self[self.next_id] = new_instance
        self.next_id = self.next_id + 1
        return new_instance

    def get_instance(self,
                     id: Union[int, str, None] = None,
                     desc: Union[str, None] = None,
                     kg: Union[str, None] = None,
                     mention: Union[str, None] = None
                     )-> List[instance]:
        """
        This is a polymorphic functions which accepts multiple kinds of input and search for eligible instance.

        :param id:
        :param desc:
        :param kg:
        :param mention:

        :return: a list of eligible instance
        """
        if id is not None:
            return self.get_instance_by_id(id)

    def get_instance_by_id(self, id: Union[int, str])-> List[instance]:
        """
        get_instance_by_id

        :param id:
        :return:  a list of eligible instance
        """
        if isinstance(id, str):
            id = int(id)
        if not isinstance(id, int):
            raise TypeError("id should be str or int")
        try:
            return [self[id]]
        except:
            return []

