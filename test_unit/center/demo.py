from nlp_platform.center.corpus import Corpus
from nlp_platform.center.raw import Raw
from nlp_platform.center.node import Node
from nlp_platform.center.instance import Instance
from nlp_platform.center.instancepool import InstancePool
from nlp_platform.center.nodepool import NodePool
from nlp_platform.center.tablepool import TablePool

c = Corpus()

#
raw = {
    "folder1": {
        "text1": "10日，埃航一架飞机坠毁，事故导致机上150人全部死亡。"
    },
    "text2": "当日，埃航展开事故遇难者的赔偿工作"
}
c.raw = Raw(raw)

#
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

#
n1 = Node()
n1["id"]["value"] = "n:xx:0-0"
n1["type"]["value"] = "entity"
n1["refer"]["value"] = "i:000"

n2 = Node()
n2["id"]["value"] = "n:xx:0-1"
n2["type"]["value"] = "entity"
n2["refer"]["value"] = "i:001"

n3 = Node()
n3["id"]["value"] = "n:xx:0-2"
n3["type"]["value"] = "entity"
n3["refer"]["value"] = "i:002"

n4 = Node()
n4["id"]["value"] = "n:xx:0-3"
n4["type"]["value"] = "event"
n4["refer"]["value"] = "i:003"

n5 = Node()
n5["id"]["value"] = "n:xx:0-4"
n5["type"]["value"] = "event"
n5["refer"]["value"] = "i:003"

n6 = Node()
n6["id"]["value"] = "n:xx:0-5"
n6["type"]["value"] = "event"
n6["refer"]["value"] = "i:005"

n7 = Node()
n7["id"]["value"] = "n:xx:0-6"
n7["type"]["value"] = "event"
n7["refer"]["value"] = "i:002"

n8 = Node()
n8["id"]["value"] = "n:xx:0-7"
n8["type"]["value"] = "entity"
n8["refer"]["value"] = "i:006"

n9 = Node()
n9["id"]["value"] = "n:xx:0-8"
n9["type"]["value"] = "event"
n9["refer"]["value"] = "i:007"

n10 = Node()
n10["id"]["value"] = "n:xx:1-10"
n10["type"]["value"] = "entity"
n10["refer"]["value"] = "i:000"

n11 = Node()
n11["id"]["value"] = "n:xx:1-11"
n11["type"]["value"] = "entity"
n11["refer"]["value"] = "i:001"

n12 = Node()
n12["id"]["value"] = "n:xx:1-12"
n12["type"]["value"] = "entity"
n12["refer"]["value"] = "i:003"

n13 = Node()
n13["id"]["value"] = "n:xx:1-13"
n13["type"]["value"] = "entity"
n13["refer"]["value"] = "i:006"

n14 = Node()
n14["id"]["value"] = "n:xx:1-14"
n14["type"]["value"] = "event"
n14["refer"]["value"] = "i:008"

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

#####################################
#               测试
#####################################
print(n1["refer"]["value"])
print(i1["mentions"]["value"])
print(n2.text)

# node的id有所修改，核实
# 实现raw[nid]功能
# 修改node的id
# 实现node.text方法
  # self.pool.corpus.raw[self["id"]["value"]]