from nlp_platform.center.instance import Instance
from nlp_platform.center.node import Node
from nlp_platform.center.corpus import Corpus

# 初始化Corpus
s = str("10日，埃航一架飞机坠毁，事故导致机上150人全部死亡。当日，埃航展开事故遇难者的赔偿工作")

i1 = Instance()
i1["id"]["value"] = "i:000"
i1["desc"]["value"] = "10日"
i1["type"]["value"] = "entity"

i2 = Instance()
i2["id"]["value"] = "i:001"
i2["desc"]["value"] = "埃航"
i2["type"]["value"] = "entity"

i3 = Instance()
i3["id"]["value"] = "i:002"
i3["desc"]["value"] = "一架飞机"
i3["type"]["value"] = "entity"

i4 = Instance()
i4["id"]["value"] = "i:003"
i4["desc"]["value"] = "坠毁"
i4["type"]["value"] = "event"

i5 = Instance()
i5["id"]["value"] = "i:005"
i5["desc"]["value"] = "导致"
i5["type"]["value"] = "event"

i6 = Instance()
i6["id"]["value"] = "i:006"
i6["desc"]["value"] = "遇难者"
i6["type"]["value"] = "entity"

i7 = Instance()
i7["id"]["value"] = "i:007"
i7["desc"]["value"] = "死亡"
i7["type"]["value"] = "event"

i8 = Instance()
i8["id"]["value"] = "i:008"
i8["desc"]["value"] = "赔偿工作"
i8["type"]["value"] = "event"

from nlp_platform.center.corpus import Corpus
from nlp_platform.center.raw import Raw
from nlp_platform.center.node import Node
from nlp_platform.center.instance import Instance

c = Corpus()

#
raw = {
    "folder1": {
        "text1.raw.txt": "10日，埃航一架飞机坠毁，事故导致机上150人全部死亡。"
    },
    "text2.raw.txt": "当日，埃航展开事故遇难者的赔偿工作"
}
c.raw = Raw(raw)

#
i1 = Instance()
c.ip.add(i1)
i1["id"]["value"] = "i:000"
i1["desc"]["value"] = "10日"
i1["type"]["value"] = "entity"

i2 = Instance()
c.ip.add(i2)
i2["id"]["value"] = "i:001"
i2["desc"]["value"] = "埃航"
i2["type"]["value"] = "entity"

i3 = Instance()
c.ip.add(i3)
i3["id"]["value"] = "i:002"
i3["desc"]["value"] = "一架飞机"
i3["type"]["value"] = "entity"

i4 = Instance()
c.ip.add(i4)
i4["id"]["value"] = "i:003"
i4["desc"]["value"] = "坠毁"
i4["type"]["value"] = "event"


i5 = Instance()
c.ip.add(i5)
i5["id"]["value"] = "i:005"
i5["desc"]["value"] = "导致"
i5["type"]["value"] = "event"


i6 = Instance()
c.ip.add(i6)
i6["id"]["value"] = "i:006"
i6["desc"]["value"] = "遇难者"
i6["type"]["value"] = "entity"


i7 = Instance()
c.ip.add(i7)
i7["id"]["value"] = "i:007"
i7["desc"]["value"] = "死亡"
i7["type"]["value"] = "event"


i8 = Instance()
c.ip.add(i8)
i8["id"]["value"] = "i:008"
i8["desc"]["value"] = "赔偿工作"
i8["type"]["value"] = "event"


#node
n1 = Node()
c.np.add(n1)
n1["id"]["value"] = "n:folder1/text1.raw.txt:0-3"
n1["type"]["value"] = "entity"
n1["refer"]["value"] = "i:000"

n2 = Node()
c.np.add(n2)
n2["id"]["value"] = "n:folder1/text1.raw.txt:4-5"
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

from nlp_platform.plug_in.output.to_files import save

save(dir="./", corpus=c)

print(1)
