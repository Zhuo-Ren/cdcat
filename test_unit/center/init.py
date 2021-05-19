from nlp_platform.center.corpus import Corpus
from nlp_platform.center.node import Node
from nlp_platform.center.instance import Instance


c = Corpus()
n1 = Node()
t = c.np
t.add(n1)
i1 = Instance()
c.ip.add(i1)

# # 赋值
# n1["type"]["value"] = "entity"

# to_info()

print(1)

