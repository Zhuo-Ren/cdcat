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

# 测试空字典
print("*"*20)
i7 = p.add_instance({})
print(i7, i7.instance_pool)
print(p)
print("*"*20)

# 强制给ID看Instance_Pool中的ID会不会改变（逻辑上应该不允许改变）
i8 = p.add_instance({'id':'88','desc':'东方航空'})
print(i8, i8.instance_pool)
print(p)
print("验证了Instance_Pool中的ID逻辑是对的")
print("*"*20)

# 一个实例给两个Instance_Pool看结果如何
i9 = Instance()
new_p = InstancePool()
print(i9,p,new_p)
p.add_instance(i9)
new_p.add_instance(i9)
print(p)
print(new_p)
print("*"*20)

# 一个instance重复给一个pool
i10 = Instance()
repeat_pool = InstancePool()
print(i10,repeat_pool)
for q in range(5):
    repeat_pool.add_instance(i10)
    print(i10, repeat_pool)












