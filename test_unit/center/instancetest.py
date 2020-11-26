from nlp_plantform.center.instance import Instance
from nlp_plantform.center.instancepool import InstancePool


print('        测试创建instance功能')
print('-' * 40)
print('         直接创建instance')
i1 = Instance()
print(i1, i1.instance_pool)

print('       通过空字典创建instance')
i2 = Instance({})
print(i2, i2.instance_pool)

print('  通过只含有desc描述的dict创建instance')
i3 = Instance({'desc' : "qqq"})
print(i3, i3.instance_pool)

print(' 通过含有id和desc描述的dict创建instance')
i4 = Instance({"id" : 1, "desc" : '埃塞俄比亚航空公司'})
print(i4, i4.instance_pool)
print('-' * 40)

print()
print()
print()

print('        测试instance_pool功能')
print('-' * 40)
print('      测试instancepool的构造函数')
p1 = InstancePool()
p2 = InstancePool()
print(p1)
print(p2)

print('   测试instance_pool加入instance功能')
print('        通过空字典添加instacne')
i5 = p1.add_instance({})
print(p1)
print(i5.instance_pool)

print(' 通过具有id字段的字典添加实例(id字段不生效才对)')
i6 = p1.add_instance({"id": 100})
print(p1)
print(i6.instance_pool)

print('       通过具有desc的字典添加实例')
i7 = p1.add_instance({"desc": "aaa"})
print(p1)
print(i7.instance_pool)

print('      测试通过实例池加入现有实例(i2)')
i2 = p1.add_instance(i2)
print(p1)
print(i2.instance_pool)

print('      测试通过实例池加入现有实例(i3)')
i3 = p1.add_instance(i3)
print(p1)
print(i3.instance_pool)
print('     测试一个实例反复加入同一实例池(i3)(无法加入)')
i3 = p1.add_instance(i3)
print(p1)
print(i3.instance_pool)

print('     测试一个实例加入多个实例池(i3)(无法加入)')
p2.add_instance(i3)
print(p2)

#print(p1.groups)






# # 测试Instance的构造函数
# i1 = Instance()
# i2 = Instance()
# i3 = Instance()
# print(i1, i1.instance_pool)
# print(i2, i2.instance_pool)
# print(i3, i3.instance_pool)
#
# # 测试InstancePool的构造函数
# p = InstancePool()
# print(p)
#
# # 测试InstancePool(instance_obj)
# p.add_instance(i1)
# p.add_instance(i2)
# p.add_instance(i3)
# print(i1, i1.instance_pool)
# print(i2, i2.instance_pool)
# print(i3, i3.instance_pool)
# print(p)
#
# # 测试InstancePool(dict_obj)
# i4 = p.add_instance({"desc":"国航"})
# i5 = p.add_instance({"desc":"天津航空"})
# i6 = p.add_instance({"desc":"厦航"})
# print(i4, i4.instance_pool)
# print(i5, i5.instance_pool)
# print(i6, i6.instance_pool)
# print(p)

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












