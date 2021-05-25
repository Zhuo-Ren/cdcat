import json
import os

def instances_to_json(dir, corpus=None):
    with open(os.path.join(dir, f'xx.instances.json'), 'w', encoding='utf-8') as f:
        data_dict = json.dumps(corpus.ip.to_info(), ensure_ascii=False, indent=4)
        f.write(data_dict)