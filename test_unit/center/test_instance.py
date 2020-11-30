from nlp_plantform.center.instance import Instance
from nlp_plantform.center.instancepool import InstancePool
import pytest


def setup_module():
    print("Setup module test_all")


def teardown_module():
    print("Teardown module test_all")


class TestInstance():
    def setup(self):
        print("Start testing a unit of instance")
    def teardown(self):
        print("Complete testing a unit of instance")

    # 测试__init__()
    def test_01(self):
        """测试Instance.__init__()，输入空"""
        i001 = Instance()
        assert i001 == {'id': None, 'desc': None}
        assert i001.instance_pool == None
    def test_02(self):
        """测试Instance.__init__()，输入空字典"""
        i002 = Instance({})
        assert i002 == {'id': None, 'desc': None}
        assert i002.instance_pool == None
    def test_03(self):
        """测试Instance.__init__(), 输入有desc的字典"""
        i003 = Instance({'desc': '东方航空'})
        assert i003 == {'id': None, 'desc': '东方航空'}
        assert i003.instance_pool == None
    def test_04(self):
        """测试Instance.__init__(), 输入有id的字典"""
        """输入的id应该无效，instance的id是由instancePool自动赋予的。"""
        i004 = Instance({'id': '888', 'desc': '厦门航空'})
        assert i004 == {'id': None, 'desc': '厦门航空'}
        assert i004.instance_pool == None


if __name__ == '__main__':
    pytest.main()
