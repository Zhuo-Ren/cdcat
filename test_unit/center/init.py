from nlp_platform.center.corpus import Corpus
from nlp_platform.center.node import Node
from nlp_platform.center.instance import Instance
from nlp_platform.center.instancepool import InstancePool
from nlp_platform.center.nodepool import NodePool
from nlp_platform.center.tablepool import TablePool

# 初始化Corpus 和三个pool
c = Corpus()
ip = InstancePool()
np = NodePool()
tp = TablePool()

# # 将三个pool赋给Corpus
# c.ip = ip
# c.np = np
# c.tp = tp

# 测试 创建node和instance加入pool中
n1 = Node()
c.np.add(n1)
i1 = Instance()
c.ip.add(i1)

# 赋值 赋值是更改了id的value 导致与初始值不同 在pool中的key没有更改 下一步统一？
n1["type"]["value"] = "entity"
n1["id"]["value"] = "0"

i1["id"]["value"] = "1"
i1["type"]["value"] = "entity"
i1["desc"]["value"] = "奥巴马"

# to_info()
info_n1 = n1.to_info()
info_i1 = i1.to_info()
info_c_ip = c.ip.to_info()
info_c_np = c.np.to_info()

# id 统一
# node["refer"]["value"]
n1["refer"]["value"] = "746"


print(1)

