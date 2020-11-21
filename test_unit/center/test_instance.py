from nlp_plantform.center.instance import Instance
from nlp_plantform.center.instancepool import InstancePool

ip1 = InstancePool()

i1 = Instance()
i2 = Instance()
i3 = Instance()

print('           初始化对象')
print('-' * 35)
print(ip1)
print(i1)
print(i2)
print(i3)
print('-' * 35)


print('         测试添加实例功能')
print('-' * 35)
i1 = ip1.add_instance(i1)
i2 = ip1.add_instance(i2)
i3 = ip1.add_instance(i3)
print(ip1)
print('-' * 35)

print('测试输入类型为dict:其中，若dict中不含desc则用id临时替代')
print('-' * 35)
dict1 = {'desc': '埃塞俄比亚航空公司'}
dict2 = {}
i4 = ip1.add_instance(dict1)
i5 = ip1.add_instance(dict2)
print(i4)
print(i5)
print(ip1)
print('-' * 35)

print('测试实例对应的实例池是否正确')
print('-' * 35)
print(i1.instance_pool)
print('-' * 35)
