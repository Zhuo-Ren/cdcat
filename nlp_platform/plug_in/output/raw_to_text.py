import json
import os
import re
import sys

def raw_to_text(dir, raw):
    # param check: raw #这个地方检查raw的类型有问题：如果设置为Raw则递归出错，如果设置为dict感觉怪怪的，可能会影响到别的地方 先就这样
    if not isinstance(raw, dict):
        raise TypeError
    #
    for key, value in raw.items():
        if isinstance(value, str):# 碰到的是一个存放raw的text文件
            if "raw.txt" in key:
                key=key[:-8]
            with open(os.path.join(dir, f'{key}.raw.txt'), 'w+', encoding='utf-8') as f:
                f.write(raw[key])
        else: # 碰到的是一个文件夹
            if os.path.exists(os.path.join(dir, key)): # 已存在该文件夹，直接进入
                raw_to_text(dir=os.path.join(dir, key), raw=raw[key])
            else:
                os.makedirs(os.path.join(dir, key))
                raw_to_text(dir=os.path.join(dir, key), raw=raw[key])