import json
import os

def raw_to_text(dir, corpus=None):

    with open(os.path.join(dir, f'xx.raw.json'), 'w', encoding='utf-8') as f:
        data_dict = json.dumps(corpus.raw, ensure_ascii=False, indent=4)
        f.write(data_dict)