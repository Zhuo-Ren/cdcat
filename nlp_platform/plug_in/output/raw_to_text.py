import json
import os
import re

def raw_to_text(dir, raw):
    # param check: raw #这个地方检查raw的类型有问题：如果设置为Raw则递归出错，如果设置为dict感觉怪怪的，可能会影响到别的地方 先就这样
    if not isinstance(raw, dict):
        raise TypeError
    #
    for key, value in raw.items():
        if re.search("raw.txt", key, flags=0): # 碰到的是一个存放raw的txt文件
            with open(os.path.join(dir, f'{key[:-8]}.raw.txt'), 'w', encoding='utf-8') as f:
                data_dict = json.dumps(raw[key], ensure_ascii=False, indent=4)
                f.write(data_dict)
        else: # 碰到的是一个文件夹
            if os.path.exists(os.path.join(dir, key)): # 已存在该文件夹，直接进入
                raw_to_text(dir=os.path.join(dir, key), raw=raw[key])
            else:
                os.mkdir(os.path.join(dir, key))
                raw_to_text(dir=os.path.join(dir, key), raw=raw[key])