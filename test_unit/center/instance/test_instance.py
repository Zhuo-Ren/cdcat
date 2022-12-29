import pytest
import re


class TestInstance:
    @pytest.fixture()
    def import_config(self):
        """ 读取核心配置load center config """
        import os
        center_config_dir = "config_label.json"
        cur_file_path = os.path.abspath(__file__)
        cur_folder_path = os.path.dirname(cur_file_path)
        center_config_dir = os.path.join(cur_folder_path, center_config_dir)
        from nlp_platform.center.config import Config
        Config.load_config(config_name="center_config", config_dir=center_config_dir)

    def test_import_success(self, import_config):
        """ 测试正确import instance.py """
        # 必须先导入center config，才能import Instance
        "通过fixture：import_config导入配置"
        #
        from nlp_platform.center.instance import Instance
        # 不报错就算import成功
        assert True

    def test_init_with_default(self, import_config):
        from nlp_platform.center.instance import Instance
        i1 = Instance()
        f = 0
        if i1.pool is not None:
            f = 1
        if re.match('i:[0-9]{19}', i1['id']['value']) is None:
            f = 1
        if i1['id']['value'] != i1['desc']['value']:
            f = 1
        if i1['type']['value'] != 'none':
            f = 1
        #
        assert f == 0

    def test_init_with_info(self, import_config):
        from nlp_platform.center.instance import Instance
        from nlp_platform.center.instancepool import InstancePool
        from nlp_platform.center.corpus import Corpus
        info = {
            "id": "1",
            "desc": "2",
            "type": "event"
        }
        ip = InstancePool()
        i1 = Instance(pool=ip, info=info)
        f = 0
        if i1.pool != ip:
            f = 1
        if i1["id"]["value"] != '1':
            f = 2
        if i1['desc']['value'] != '2':
            f = 3
        if i1['type']['value'] != 'event':
            f = 4
        #
        assert f == 0

    def test_register_1(self, import_config):
        """
        把instance_obj注册到instancepool_obj的方法1：
        `Instance(pool=instancepool_obj)`，可以维护双向关系。
        """
        from nlp_platform.center.instance import Instance
        from nlp_platform.center.instancepool import InstancePool
        ip = InstancePool()
        i1 = Instance(pool=ip, info={"id": 'Frank'})
        assert (('Frank' in i1.pool) and (i1.pool == ip))

    def test_register_2(self, import_config):
        """
        把instance_obj注册到instancepool_obj的方法2：
        `instance_obj.pool=instancepool_obj`，只维护instance_obj向instancepool_obj的关系。
        """
        from nlp_platform.center.instance import Instance
        from nlp_platform.center.instancepool import InstancePool
        ip = InstancePool()
        i1 = Instance(info={"id": 'Frank'})
        i1.pool = ip
        assert ('Frank' not in i1.pool) and (i1.pool == ip)

    def test_register_3(self, import_config):
        """把instance_obj注册到instancepool_obj的方法3：`instancepool_obj.add(instance_obj)`，可以维护双向关系。"""
        from nlp_platform.center.instance import Instance
        from nlp_platform.center.instancepool import InstancePool
        ip = InstancePool()
        i1 = Instance(info={"id": 'Frank'})
        ip.add(i1)
        assert (('Frank' in i1.pool) and (i1.pool == ip))