from nlp_plantform.center.instance import Instance
from nlp_plantform.center.instancepool import  InstancePool

i1 = Instance()
i2 = Instance()
i3 = Instance()
p = InstancePool()
#初始的时候p为空
print('*********')
print(i1)
print(i2)
print(i3)
print(p)
print('*********')
print('生成测试')
print('*********')
i1 = p.add_instance(i1)
i2 = p.add_instance(i2)
i3 = p.add_instance(i3)
print(i1)
print(i2)
print(i3)
print('*********')
print('测试字典')
dict1 = {"desc":"国航"}
dict2 = {"desc":"天津航空"}
dict3 = {"desc":"厦航"}
i4 = p.add_instance(dict1)
i5 = p.add_instance(dict2)
i6 = p.add_instance(dict3)
print(i4)
print(i5)
print(i6)
print(i1.instance_pool)











