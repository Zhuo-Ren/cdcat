import json
import os

def instances_to_json(dir, ip):
    # param check: ip
    from nlp_platform.center.instancepool import InstancePool
    if not isinstance(ip, InstancePool):
        raise TypeError
    with open(os.path.join(dir, f'instances.json'), 'w', encoding='utf-8') as f:
        data_dict = json.dumps(ip.to_info(), ensure_ascii=False, indent=4)
        f.write(data_dict)