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


n1 = Node()
n1["id"]["value"] = "n:0-0"
n1["type"]["value"] = "entity"

n2 = Node()
n2["id"]["value"] = "n:0-1"
n2["type"]["value"] = "entity"

n3 = Node()
n3["id"]["value"] = "n:0-2"
n3["type"]["value"] = "entity"

n4 = Node()
n4["id"]["value"] = "n:0-3"
n4["type"]["value"] = "event"

n5 = Node()
n5["id"]["value"] = "n:0-4"
n5["type"]["value"] = "event"

n6 = Node()
n6["id"]["value"] = "n:0-5"
n6["type"]["value"] = "event"

n7 = Node()
n7["id"]["value"] = "n:0-6"
n7["type"]["value"] = "event"

n8 = Node()
n8["id"]["value"] = "n:0-7"
n8["type"]["value"] = "entity"

n9 = Node()
n9["id"]["value"] = "n:0-8"
n9["type"]["value"] = "event"

n10 = Node()
n10["id"]["value"] = "n:1-0"
n10["type"]["value"] = "entity"

n11 = Node()
n11["id"]["value"] = "n:1-1"
n11["type"]["value"] = "entity"

n12 = Node()
n12["id"]["value"] = "n:1-2"
n12["type"]["value"] = "entity"

n13 = Node()
n13["id"]["value"] = "n:1-3"
n13["type"]["value"] = "entity"

n14 = Node()
n14["id"]["value"] = "n:1-4"
n14["type"]["value"] = "event"


c = Corpus()
c.ip.add(i1)
c.ip.add(i2)
c.ip.add(i3)
c.ip.add(i4)
c.ip.add(i5)
c.ip.add(i6)
c.ip.add(i7)
c.ip.add(i8)

c.np.add(n1)
c.np.add(n2)
c.np.add(n3)
c.np.add(n4)
c.np.add(n5)
c.np.add(n6)
c.np.add(n7)
c.np.add(n8)
c.np.add(n9)
c.np.add(n10)
c.np.add(n11)
c.np.add(n12)
c.np.add(n13)
c.np.add(n14)

n1["refer"]["value"] = "i:000"
n2["refer"]["value"] = "i:001"
n3["refer"]["value"] = "i:002"
n4["refer"]["value"] = "i:003"
n5["refer"]["value"] = "i:003"
n6["refer"]["value"] = "i:005"
n7["refer"]["value"] = "i:002"
n8["refer"]["value"] = "i:006"
n9["refer"]["value"] = "i:007"
n10["refer"]["value"] = "i:000"
n11["refer"]["value"] = "i:001"
n12["refer"]["value"] = "i:003"
n13["refer"]["value"] = "i:006"
n14["refer"]["value"] = "i:008"


relation_0 = n1["refer"]["value"]
relation_1 = i1["mentions"]["value"]

c.raw = s

# 输入一个路径 把内容输出到路径下 输出到xx.raw raw里存纯文本 xx.nodes存node的信息（nodepool.to_info） xx.instances (instancepool.to_info)
# 输出为.json 或 .xml


from nlp_platform.plug_in.output.to_files import save

save(dir="./", corpus=c)




print(1)
