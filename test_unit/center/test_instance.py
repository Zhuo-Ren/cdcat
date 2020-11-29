from nlp_plantform.center.instance import Instance
from nlp_plantform.center.instancepool import InstancePool
import pytest

class Test_instance():
    def setup(self):
        print("Start testing a unit of instance")
    def teardown(self):
        print("Complete testing a unit of instance")
    def test_01(self):
        #直接调用构造函数创建instance(i1)
        i1 = Instance()
        #判断i1是否为{'id' : None, 'desc' : None}
        assert i1 == {'id' : None, 'desc' : None}
        #判断i1的所属实例池是否为空
        assert i1.instance_pool == None
    def test_02(self):
        #通过空字典创建instance(i2)
        i2 = Instance({})
        # 判断i2是否为{'id' : None, 'desc' : None}
        assert i2 == {'id' : None, 'desc' : None}
        # 判断i2的所属实例池是否为空
        assert i2.instance_pool == None
    def test_03(self):
        #通过只含有desc描述的dict创建instance(i3)
        i3 = Instance({'desc': "qqq"})
        assert i3 == {'id' : None, 'desc' : 'qqq'}
        # 判断i3的所属实例池是否为空
        assert i3.instance_pool == None
    def test_04(self):
        #通过含有id和desc描述的dict创建instance(i4)
        i4 = Instance({"id": 1, "desc": '埃塞俄比亚航空公司'})
        assert i4 == {'id': None, 'desc': '埃塞俄比亚航空公司'}
        # 判断i4的所属实例池是否为空
        assert i4.instance_pool == None


class Test_instancepool():
    def setup(self):
        print("Start testing a unit of instancepool")
    def teardown(self):
        print("Complete testing a unit of instancepool")
    def test_01(self):
        #测试instancepool的构造函数
        p = InstancePool()
        assert p == {}

    # 测试instance_pool加入instance功能
    def test_02(self):
        #通过空字典添加instacne
        p = InstancePool()
        instance = p.add_instance({})
        #判断p是否成功加入instance并给instance赋予id和desc（instance无desc描述时）
        assert p == {0:{'id' : 0, 'desc' : 0}}
        #判断加入p的instance有没有绑定p（是否完成双向绑定）
        assert instance.instance_pool == p
    def test_03(self):
        #通过具有id字段的字典添加实例(id字段不生效才对)
        p = InstancePool()
        instance = p.add_instance({"id": 100})
        assert instance['id'] == 0
        #判断加入p的instance有没有绑定p（是否完成双向绑定）
        assert instance.instance_pool == p

    def test_04(self):
        #通过具有desc的字典添加实例
        p = InstancePool()
        instance = p.add_instance({"desc": "aaa"})
        assert p == {0: {'id': 0, 'desc': "aaa"}}
        # 判断加入p的instance有没有绑定p（是否完成双向绑定）
        assert instance.instance_pool == p

    def test_05(self):
        #测试通过实例池加入现有实例(instance)(无描述的instance)
        p = InstancePool()
        instance = Instance({})
        instance = p.add_instance(instance)
        assert p == {0:{'id': 0, 'desc': 0}}
        assert instance.instance_pool == p

    def test_06(self):
        #测试通过实例池加入现有实例(instance)（有描述）
        p = InstancePool()
        instance = Instance({'desc' : "张三"})
        instance = p.add_instance(instance)
        assert p == {0:{'id': 0, 'desc': "张三"}}
        assert instance.instance_pool == p

    def test_07(self):
        #测试一个实例池加入多个不同实例
        p = InstancePool()
        i1 = Instance({'desc': "张三"})
        i2 = Instance({'desc': "李四"})
        i1 = p.add_instance(i1)
        i2 = p.add_instance(i2)
        assert p == {0:{'id': 0, 'desc': '张三'}, 1:{'id': 1, 'desc': '李四'}}
        assert i1.instance_pool == p
        assert i2.instance_pool == p

    def test_08(self):
        #测试一个实例反复加入同一实例池(无法加入)（报Exception异常）
        p = InstancePool()
        instance = Instance({'desc': "测试测试"})
        instance = p.add_instance(instance)
        #反复加入同一实例池
        with pytest.raises(Exception) as e:
            instance = p.add_instance(instance)
        assert str(e.value) == "Add failed, because the instance has been bound to the current intancepool"
        assert instance.instance_pool == p

    def test_09(self):
        #测试一个实例加入多个实例池(i3)(无法加入)（报Exception异常）
        p1 = InstancePool()
        p2 = InstancePool()
        instance = Instance({'desc': "测试测试"})
        instance = p1.add_instance(instance)
        with pytest.raises(Exception) as e:
            p2.add_instance(instance)
        assert str(e.value) == "Add failed, because the instance has been bound to another intancepool"
        assert instance.instance_pool == p1


if __name__ == 'main':
    pytest.main('test_instance.py')
