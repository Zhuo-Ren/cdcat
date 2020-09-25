from typing import Dict, List, Tuple, Union  # for type hinting


class InstanceLabels(dict):
    # static
    config = {}
    from nlp_plantform.plug_in.manual_annotation_tool.cdcat import config as cdcat_config
    import json
    with open(cdcat_config.label_sys_dict_path, 'r', encoding='utf8') as labelf:
        label_sys_dict = json.load(labelf)
    for cur_label in label_sys_dict["instance"]:
        config.update({
            cur_label["key"]: cur_label
        })

    from nlp_plantform.center.instance import Instance
    def __init__(self, owner: Instance, label_value: Dict = {}):
        """
        Init the labels of a instance.

        :param owner: The instance is the owner of the labels.
          The labels obj need knows it owner when edit a linked label such as a_node.labels["instance"] ---
          a_instance.labels["mentionList"]

        :param label_value: Value of labels.
          Only the one who follows the config in config_label_sys.json will be accept, or the default value will be
          used.

        """
        # private
        self.owner = owner

        # init label value
        from nlp_plantform.center.labeltypes import labeltypes
        for (cur_label_key, cur_label_config) in self.config.items():
            # if the label value is given in param, and the label value is not None, use the given value
            if cur_label_key in label_value:
                if label_value[cur_label_key] is not None:
                    self.update({
                        cur_label_key: labeltypes[cur_label_config["value_type"]](label_value[cur_label_key])
                    })
            # if the label value is given in param, but the label value is None, use the default value.
                else:
                    self.update({
                        cur_label_key: labeltypes[cur_label_config["value_type"]](cur_label_config["value_default"])
                    })
            # if the label value is not given in param, use the default value
            else:
                self.update({
                    cur_label_key: labeltypes[cur_label_config["value_type"]](cur_label_config["value_default"])
                })

    def __setitem__(self, key, value):
        # destruct old value
        try:
            old_value = self[key]
            del self[key]
        except:
            pass
        # construct new value
        from nlp_plantform.center.labeltypes import labeltypes
        self[key] = labeltypes[self.config[key]["value_type"]](value)

    def __str__(self) -> str:
        output_dict = {}
        for cur_label_key in self.keys():
            output_dict.update({cur_label_key: self[cur_label_key].output_to_infodict()})
        return str(output_dict)

    def nolink_labels(self):
        nolink_labels = {}
        for (label_key,label_config) in InstanceLabels.config.items():
            if "linkto" in label_config:
                pass
            else:
                nolink_labels.update({label_key: self[label_key]})
        return nolink_labels