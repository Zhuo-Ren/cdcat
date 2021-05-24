import json
import os


def save_info(data_dir, data, desc):
    """
    将数据（dict或str）转存为json格式
    :param data_dir: info文件存储目录
    :param data: 数据
    :param desc: 可选项："raw" "instances" "nodes"
    :return:
    """
    with open(os.path.join(data_dir, f'xx.{desc}.json'), 'w', encoding='utf-8') as f:
        if desc == "raw":
            data_dict = json.dumps(data)
        else:
            data_dict = json.dumps(data.to_info())

        f.write(data_dict)