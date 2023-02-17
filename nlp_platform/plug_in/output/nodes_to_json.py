import json
import os

def nodes_to_json(dir, np):
    # param check: np
    from nlp_platform.center.nodepool import NodePool
    if not isinstance(np, NodePool):
        raise TypeError
    nplist=[(k, np[k]) for k in sorted(np.keys())]
    sum_node=len(nplist)
    # 修改保存方式
    doc_dict = {}
    for node in nplist:
        doc_id=node[0].split(":")[1]
        if doc_id not in doc_dict:
            doc_dict.update({doc_id: {node[0]:node[1].to_info()}})
        else:
            doc_dict[doc_id].update({node[0]:node[1].to_info()})
    if (sum_node > 0):
        for key in doc_dict.keys():
            node_id_mid_slice = key.split('/')
            part_file_path = ""

            if len(node_id_mid_slice) > 1:
                index = -1
                for s in node_id_mid_slice[0: -1]:
                    part_file_path = part_file_path + s
            else:
                index = 0
            cur_folder = os.path.join(dir, part_file_path)
            if os.path.exists(cur_folder) is False:
                os.mkdirs(cur_folder)
            cur_doc_id=node_id_mid_slice[index]
            if "raw.txt" in cur_doc_id:
                cur_doc_id = cur_doc_id[:-8]
            with open(os.path.join(dir, part_file_path, f'{cur_doc_id}.nodes.json'), 'w+',
                      encoding='utf-8') as f:
                info =  doc_dict[key]
                data_dict = json.dumps(info, ensure_ascii=False, indent=4)
                f.write(data_dict)

    # 原来的方式
    # end = 0
    # # np_map为排序后的nodepool,将相同file_id的node顺序保存，并存储到对应的node.json
    # np_map = {}
    # for np_node in nplist:
    #     np_map[np_node[0]] = np_node[1].to_info()
    # node_id_dict = dict()
    # cur_position = 0
    # if(sum_node>0):
    #     for key in np_map.keys():
    #         node_id_dict[cur_position] = key.split(':')
    #
    #         if (len(node_id_dict) >1 and node_id_dict[cur_position-1][1] != node_id_dict[cur_position][1]):
    #             node_id_mid = node_id_dict[cur_position - 1][1]
    #             node_id_mid_slice = node_id_mid.split('/')
    #             part_file_path = ""
    #
    #             if len(node_id_mid_slice) > 1:
    #                 index = -1
    #                 for s in node_id_mid_slice[0: -1]:
    #                     part_file_path = part_file_path + s
    #             else:
    #                 index = 0
    #             cur_folder=os.path.join(dir, part_file_path)
    #             if os.path.exists(cur_folder) is False:
    #                 os.mkdir(cur_folder)
    #
    #             with open(os.path.join(dir, part_file_path, f'{node_id_mid_slice[index]}.nodes.json'), 'w+', encoding='utf-8') as f:
    #                 info = np_map
    #                 start = end
    #
    #                 end = cur_position
    #                 info = dict_slice(info, start, end)
    #                 data_dict = json.dumps(info, ensure_ascii=False, indent=4)
    #                 f.write(data_dict)
    #         # 如果只有一个节点
    #         if (cur_position+1 == len(np.keys())):
    #             node_id_mid = node_id_dict[cur_position][1]
    #             node_id_mid_slice = node_id_mid.split('/')
    #             part_file_path = ""
    #
    #             if len(node_id_mid_slice) > 1:
    #                 index = -1
    #                 for s in node_id_mid_slice[0: -1]:
    #                     part_file_path = part_file_path + s+'/'
    #             else:
    #                 index = 0
    #
    #             with open(os.path.join(dir, part_file_path, f'{node_id_mid_slice[index][: -8]}.nodes.json'), 'w+', encoding='utf-8') as f:
    #                 info = np_map
    #                 start = end
    #                 end = cur_position + 1
    #                 info = dict_slice(info, start, end)
    #                 data_dict = json.dumps(info, ensure_ascii=False, indent=4)
    #                 f.write(data_dict)
    #
    #         cur_position += 1


# def dict_slice(adict, start, end):
#     keys = adict.keys()
#     dict_slice = {}
#     for k in list(keys)[start:end]:
#         dict_slice[k] = adict[k]
#     return dict_slice


