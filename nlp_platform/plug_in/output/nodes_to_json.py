import json
import os

def nodes_to_json(dir, np):
    # param check: np
    from nlp_platform.center.nodepool import NodePool
    if not isinstance(np, NodePool):
        raise TypeError
    end = 0
    node_id_dict = dict()
    cur_position = 0
    for key in np.keys():
        node_id_dict[cur_position] = key.split(':')

        if (len(node_id_dict) > 1 and node_id_dict[cur_position-1][1] != node_id_dict[cur_position][1]) or (cur_position+1 == len(np.keys())):
            node_id_mid = node_id_dict[cur_position - 1][1]
            node_id_mid_slice = node_id_mid.split('/')
            part_file_path = ""

            if len(node_id_mid_slice) > 1:
                index = -1
                for s in node_id_mid_slice[0: -1]:
                    part_file_path = part_file_path + s
            else:
                index = 0

            with open(os.path.join(dir, part_file_path, f'{node_id_mid_slice[index][: -8]}.nodes.json'), 'w', encoding='utf-8') as f:
                info = np.to_info()
                start = end
                if cur_position + 1 == len(np.keys()):
                    end = cur_position + 1
                else:
                    end = cur_position
                info = dict_slice(info, start, end)
                data_dict = json.dumps(info, ensure_ascii=False, indent=4)
                f.write(data_dict)

        cur_position += 1


def dict_slice(adict, start, end):
    keys = adict.keys()
    dict_slice = {}
    for k in list(keys)[start:end]:
        dict_slice[k] = adict[k]
    return dict_slice




    # for key, value in raw.items():
    #     if re.search("raw.txt", key, flags=0): # 碰到的是一个存放raw的txt文件
    #         with open(os.path.join(dir, f'{key[:-8]}.raw.txt'), 'w', encoding='utf-8') as f:
    #             data_dict = json.dumps(raw[key], ensure_ascii=False, indent=4)
    #             f.write(data_dict)
    #     else: # 碰到的是一个文件夹
    #         if os.path.exists(key): # 已存在该文件夹，直接进入
    #             raw_to_text(dir=os.path.join(dir, key), raw=raw[key])
    #         else:
    #             os.mkdir(os.path.join(dir, key))
    #             raw_to_text(dir=os.path.join(dir, key), raw=raw[key])