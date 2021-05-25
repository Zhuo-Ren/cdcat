import json
import os

def nodes_to_json(dir, corpus=None):
    with open(os.path.join(dir, f'xx.nodes.json'), 'w', encoding='utf-8') as f:
        data_dict = json.dumps(corpus.np.to_info(), ensure_ascii=False, indent=4)
        f.write(data_dict)