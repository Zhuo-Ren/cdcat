from nlp_plantform.center.instance import Instance
from nlp_plantform.center.instancepool import InstancePool
import pytest

def setup_module():
    print("Setup module test_all")
def teardown_module():
    print("Teardown module test_all")


class Test_instancepool():
    def setup(self):
        print("Start testing a unit of instancepool")
    def teardown(self):
        print("Complete testing a unit of instancepool")

    # 测试__init__()
    def test_checkInstancePool(self):
        """初始化Instancepool检查"""
        p = InstancePool()
        assert p == {}

    # 测试add_instance()
    def test_chekNonedict(self):
        """加入空字典的实例"""
        p = InstancePool()
        instance = p.add_instance({})
        # 判断p是否成功加入instance并给instance赋予id和desc（instance无desc描述时）
        assert p == {0: {'id': 0, 'desc': 0}}  # 测试节点2
        # 判断加入p的instance有没有绑定p（是否完成双向绑定）
        assert instance.instance_pool == p # 测试节点3
    def test_checkAddID(self):
        """恶意赋予ID检测"""
        p = InstancePool()
        instance = p.add_instance({"id": 100})
        assert instance['id'] == 0      # 测试节点4
        # 判断加入p的instance有没有绑定p（是否完成双向绑定）
        assert instance.instance_pool == p  # 测试节点5
    def test_checkAddDict(self):
        """通过具有desc的字典添加实例"""
        p = InstancePool()
        instance = p.add_instance({"desc": "abc"})
        assert p == {0: {'id': 0, 'desc': "abc"}}  # 测试节点6
        # 判断加入p的instance有没有绑定p（是否完成双向绑定）
        assert instance.instance_pool == p  # 测试节点7
    def test_checkAddExistInstance(self):
        """测试通过实例池加入现有实例(instance)(无描述的instance)"""
        p = InstancePool()
        instance = Instance({})
        instance = p.add_instance(instance)
        assert p == {0: {'id': 0, 'desc': 0}}  # 测试节点8
        assert instance.instance_pool == p  # 测试节点9
    def test_checkAddDescInstance(self):
        """测试通过实例池加入现有实例(instance)（有描述）"""
        p = InstancePool()
        instance = Instance({'desc': "春秋航空"})
        instance = p.add_instance(instance)
        assert p == {0: {'id': 0, 'desc': "春秋航空"}} # 测试节点10
        assert instance.instance_pool == p # 测试节点11
    def test_AddDiffInstanceToOnePool(self):
        """测试一个实例池加入多个不同实例"""
        p = InstancePool()
        i1 = Instance({'desc': "aaa"})
        i2 = Instance({'desc': "bbb"})
        i1 = p.add_instance(i1)
        i2 = p.add_instance(i2)
        assert p == {0: {'id': 0, 'desc': 'aaa'}, 1: {'id': 1, 'desc': 'bbb'}}  # 测试节点12
        assert i1.instance_pool == p  # 测试节点13
        assert i2.instance_pool == p  # 测试节点14
    def test_addinstanceRepeat(self):
        """测试一个实例反复加入一个pool"""
        p = InstancePool()
        instance = Instance({'desc': "测试"})
        instance = p.add_instance(instance)
        with pytest.raises(Exception) as err:
            instance = p.add_instance(instance)
        assert str(err.value) == "Add failed, because the instance has been allocated in this pool"
        assert instance.instance_pool == p
    def test_InstanceToDiffPoll(self):
        """测试一个实例加入多个实例池(i3)(无法加入)（报Exception异常）"""
        p1 = InstancePool()
        p2 = InstancePool()
        instance = Instance({'desc': "测试"})
        instance = p1.add_instance(instance)
        with pytest.raises(Exception) as err:
            p2.add_instance(instance)
        assert str(err.value) == "Add failed, because the instance has been allocated in other pool"
        assert instance.instance_pool == p1

if __name__ == '__main__':
    pytest.main()
