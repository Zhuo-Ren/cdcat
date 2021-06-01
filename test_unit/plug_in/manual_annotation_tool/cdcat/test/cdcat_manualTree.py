import os

# center config
center_config_dir = "config_label.json"
# load center config
cur_file_path = os.path.abspath(__file__)
cur_folder_path = os.path.dirname(cur_file_path)
center_config_dir = os.path.join(cur_folder_path, center_config_dir)
from nlp_platform.center.config import Config
Config.load_config(config_name="center_config", config_dir=center_config_dir)

# create corpus
from nlp_platform.center.corpus import Corpus
c = Corpus()

raw = {
    "folder1": {
        "text1.raw.txt": "10日，埃航一架飞机坠毁，事故导致机上150人全部死亡。"
    },
    "text2.raw.txt": "当日，埃航展开事故遇难者的赔偿工作",
    "text3.raw.txt": "测试用3",
    "folder2": {
        "text4.raw.txt": "测试用4",
        "folder21": {
            "text5.raw.txt": "测试用5",
            "text6.raw.txt": "测试用6"
        }
    }
}
from nlp_platform.center.raw import Raw
c.raw = Raw(raw)

from nlp_platform.center.instance import Instance
i1 = Instance()
i1["id"]["value"] = "i:000"
i1["desc"]["value"] = "10日"
i1["type"]["value"] = "entity"
c.ip.add(i1)
i2 = Instance()
i2["id"]["value"] = "i:001"
i2["desc"]["value"] = "埃航"
i2["type"]["value"] = "entity"
c.ip.add(i2)
i3 = Instance()
i3["id"]["value"] = "i:002"
i3["desc"]["value"] = "一架飞机"
i3["type"]["value"] = "entity"
c.ip.add(i3)
i4 = Instance()
i4["id"]["value"] = "i:003"
i4["desc"]["value"] = "坠毁"
i4["type"]["value"] = "event"
c.ip.add(i4)
i5 = Instance()
i5["id"]["value"] = "i:005"
i5["desc"]["value"] = "导致"
i5["type"]["value"] = "event"
c.ip.add(i5)
i6 = Instance()
i6["id"]["value"] = "i:006"
i6["desc"]["value"] = "遇难者"
i6["type"]["value"] = "entity"
c.ip.add(i6)
i7 = Instance()
i7["id"]["value"] = "i:007"
i7["desc"]["value"] = "死亡"
i7["type"]["value"] = "event"
c.ip.add(i7)
i8 = Instance()
i8["id"]["value"] = "i:008"
i8["desc"]["value"] = "赔偿工作"
i8["type"]["value"] = "event"
c.ip.add(i8)


from nlp_platform.center.node import Node
n1 = Node()
c.np.add(n1)
n1["id"]["value"] = "n:folder1/text1.raw.txt:0-3"
n1["type"]["value"] = "entity"
n1["refer"]["value"] = "i:000"
n2 = Node()
c.np.add(n2)
n2["id"]["value"] = "n:folder1/text1.raw.txt:4-6"
n2["type"]["value"] = "entity"
n2["refer"]["value"] = "i:001"
n3 = Node()
c.np.add(n3)
n3["id"]["value"] = "n:folder1/text1.raw.txt:6-10"
n3["type"]["value"] = "entity"
n3["refer"]["value"] = "i:002"
n4 = Node()
c.np.add(n4)
n4["id"]["value"] = "n:folder1/text1.raw.txt:10-12"
n4["type"]["value"] = "event"
n4["refer"]["value"] = "i:003"
n5 = Node()
c.np.add(n5)
n5["id"]["value"] = "n:folder1/text1.raw.txt:13-15"
n5["type"]["value"] = "event"
n5["refer"]["value"] = "i:003"
n6 = Node()
c.np.add(n6)
n6["id"]["value"] = "n:folder1/text1.raw.txt:15-17"
n6["type"]["value"] = "event"
n6["refer"]["value"] = "i:005"
n7 = Node()
c.np.add(n7)
n7["id"]["value"] = "n:folder1/text1.raw.txt:17-18"
n7["type"]["value"] = "event"
n7["refer"]["value"] = "i:002"
n8 = Node()
c.np.add(n8)
n8["id"]["value"] = "n:folder1/text1.raw.txt:19-23"
n8["type"]["value"] = "entity"
n8["refer"]["value"] = "i:006"
n9 = Node()
c.np.add(n9)
n9["id"]["value"] = "n:folder1/text1.raw.txt:25-27"
n9["type"]["value"] = "event"
n9["refer"]["value"] = "i:007"
n10 = Node()
c.np.add(n10)
n10["id"]["value"] = "n:text2.raw.txt:0-2"
n10["type"]["value"] = "entity"
n10["refer"]["value"] = "i:000"
n11 = Node()
c.np.add(n11)
n11["id"]["value"] = "n:text2.raw.txt:3-5"
n11["type"]["value"] = "entity"
n11["refer"]["value"] = "i:001"
n12 = Node()
c.np.add(n12)
n12["id"]["value"] = "n:text2.raw.txt:7-9"
n12["type"]["value"] = "entity"
n12["refer"]["value"] = "i:003"
n13 = Node()
c.np.add(n13)
n13["id"]["value"] = "n:text2.raw.txt:9-12"
n13["type"]["value"] = "entity"
n13["refer"]["value"] = "i:006"
n14 = Node()
c.np.add(n14)
n14["id"]["value"] = "n:text2.raw.txt:13-17"
n14["type"]["value"] = "event"
n14["refer"]["value"] = "i:008"


# annotation
from nlp_platform.plug_in.manual_annotation_tool.cdcat.cdcat import cdcat
cdcat(c)

