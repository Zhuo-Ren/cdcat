import json
import os

def nodes_to_json(dir, np):
    # param check: np
    from nlp_platform.center.nodepool import NodePool
    if not isinstance(np, NodePool):
        raise TypeError
    with open(os.path.join(dir, f'xx.nodes.json'), 'w', encoding='utf-8') as f:
        data_dict = json.dumps(np.to_info(), ensure_ascii=False, indent=4)
        f.write(data_dict)