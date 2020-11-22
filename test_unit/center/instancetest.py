from nlp_plantform.center.instance import Instance
from nlp_plantform.center.instancepool import InstancePool

# i1 = Instance（）
# i2 = Instance（{}）
# i3 = Instance（{"id","desc"}）
# i4 = Instance（有desc的字典）
# p1 = InstancePool()
# p2 = InstancePool()
# InstancePool_obj.add_instance({})
# InstancePool_obj.add_instance({"id": 100 })
# InstancePool_obj.add_instance({"desc": "aaa"})
# InstancePool_obj.add_instance(i2)})
# InstancePool_obj.add_instance(i3)})
# InstancePool_obj.add_instance(i3)})


# 测试Instance的构造函数
i1 = Instance()
i2 = Instance()
i3 = Instance()
print(i1, i1.instance_pool)
print(i2, i2.instance_pool)
print(i3, i3.instance_pool)

# 测试InstancePool的构造函数
p = InstancePool()
print(p)

# 测试InstancePool(instance_obj)
p.add_instance(i1)
p.add_instance(i2)
p.add_instance(i3)
print(i1, i1.instance_pool)
print(i2, i2.instance_pool)
print(i3, i3.instance_pool)
print(p)

# 测试InstancePool(dict_obj)
i4 = p.add_instance({"desc":"国航"})
i5 = p.add_instance({"desc":"天津航空"})
i6 = p.add_instance({"desc":"厦航"})
print(i4, i4.instance_pool)
print(i5, i5.instance_pool)
print(i6, i6.instance_pool)
print(p)











