import pytest
import re


class Test_main:
    @pytest.fixture()
    def create_c_a_n_i(self):
        # 读取核心配置load center config
        import os
        center_config_dir = "config_label.json"
        cur_file_path = os.path.abspath(__file__)
        cur_folder_path = os.path.dirname(cur_file_path)
        center_config_dir = os.path.join(cur_folder_path, center_config_dir)
        from nlp_platform.center.config import Config
        Config.load_config(config_name="center_config", config_dir=center_config_dir)

        # create corpus(include Raw, NodePool, InstancePool)
        from nlp_platform.center.corpus import Corpus
        c = Corpus()

        # create raw
        raw = {
            "folder1": {
                "text1.raw.txt": "10日，埃航一架飞机坠毁，事故导致机上150人全部死亡。"
            },
            "text2.raw.txt": "当日，埃航展开事故遇难者的赔偿工作",
            "text3.raw.txt": "测试用3",
            "folder2": {
                "text4.raw.txt": "测试用4",
                "folder21": {
                    "text5.raw.txt": "测试用5",
                    "text6.raw.txt": "测试用6"
                }
            }
        }
        from nlp_platform.center.raw import Raw
        c.raw = Raw(raw)


        from nlp_platform.center.instance import Instance
        i1 = Instance(pool=c.ip)
        i1["desc"]["value"] = "10日"
        i1["type"]["value"] = "entity"
        i1["mentions"]["value"] = ["n:folder1/text1.raw.txt:0-3",
                                   "n:text2.raw.txt:0-2"]
        i2 = Instance()
        c.ip.add(i2)
        i2["desc"]["value"] = "埃航"
        i2["type"]["value"] = "entity"
        i2["mentions"]["value"] = ["n:folder1/text1.raw.txt:4-6",
                                   "n:text2.raw.txt:3-5"]
        i3 = Instance()
        c.ip.add(i3)
        i3["desc"]["value"] = "一架飞机"
        i3["type"]["value"] = "entity"
        i3["mentions"]["value"] = ["n:folder1/text1.raw.txt:6-10",
                                   "n:folder1/text1.raw.txt:17-18"]
        i4 = Instance()
        c.ip.add(i4)
        i4["desc"]["value"] = "坠毁"
        i4["type"]["value"] = "event"
        i4["mentions"]["value"] = ["n:folder1/text1.raw.txt:10-12",
                                   "n:folder1/text1.raw.txt:13-15",
                                   "n:text2.raw.txt:7-9"]
        i5 = Instance()
        c.ip.add(i5)
        i5["desc"]["value"] = "导致"
        i5["type"]["value"] = "event"
        i5["mentions"]["value"] = ["n:folder1/text1.raw.txt:15-17"]
        i6 = Instance()
        c.ip.add(i6)
        i6["desc"]["value"] = "遇难者"
        i6["type"]["value"] = "entity"
        i6["mentions"]["value"] = ["n:folder1/text1.raw.txt:19-23",
                                   "n:text2.raw.txt:9-12"]
        i7 = Instance()
        c.ip.add(i7)
        i7["desc"]["value"] = "死亡"
        i7["type"]["value"] = "event"
        i7["mentions"]["value"] = ["n:folder1/text1.raw.txt:25-27"]
        i8 = Instance()
        c.ip.add(i8)
        i8["desc"]["value"] = "赔偿工作"
        i8["type"]["value"] = "event"
        i8["mentions"]["value"] = ["n:text2.raw.txt:13-17"]

        from nlp_platform.center.node import Node
        n1 = Node()
        c.np.add(n1)
        n1["id"]["value"] = "n:folder1/text1.raw.txt:0-3"
        n1["type"]["value"] = "entity"
        n2 = Node()
        c.np.add(n2)
        n2["id"]["value"] = "n:folder1/text1.raw.txt:4-6"
        n2["type"]["value"] = "entity"
        n3 = Node()
        c.np.add(n3)
        n3["id"]["value"] = "n:folder1/text1.raw.txt:6-10"
        n3["type"]["value"] = "entity"
        n4 = Node()
        c.np.add(n4)
        n4["id"]["value"] = "n:folder1/text1.raw.txt:10-12"
        n4["type"]["value"] = "event"
        n5 = Node()
        c.np.add(n5)
        n5["id"]["value"] = "n:folder1/text1.raw.txt:13-15"
        n5["type"]["value"] = "event"
        n6 = Node()
        c.np.add(n6)
        n6["id"]["value"] = "n:folder1/text1.raw.txt:15-17"
        n6["type"]["value"] = "event"
        n7 = Node()
        c.np.add(n7)
        n7["id"]["value"] = "n:folder1/text1.raw.txt:17-18"
        n7["type"]["value"] = "event"
        n8 = Node()
        c.np.add(n8)
        n8["id"]["value"] = "n:folder1/text1.raw.txt:19-23"
        n8["type"]["value"] = "entity"
        n9 = Node()
        c.np.add(n9)
        n9["id"]["value"] = "n:folder1/text1.raw.txt:25-27"
        n9["type"]["value"] = "event"
        n10 = Node()
        c.np.add(n10)
        n10["id"]["value"] = "n:text2.raw.txt:0-2"
        n10["type"]["value"] = "entity"
        n11 = Node()
        c.np.add(n11)
        n11["id"]["value"] = "n:text2.raw.txt:3-5"
        n11["type"]["value"] = "entity"
        n12 = Node()
        c.np.add(n12)
        n12["id"]["value"] = "n:text2.raw.txt:7-9"
        n12["type"]["value"] = "entity"
        n13 = Node()
        c.np.add(n13)
        n13["id"]["value"] = "n:text2.raw.txt:9-12"
        n13["type"]["value"] = "entity"
        n14 = Node()
        c.np.add(n14)
        n14["id"]["value"] = "n:text2.raw.txt:13-17"
        n14["type"]["value"] = "event"

    def test_value(self, create_c_a_n_i):
        # # 测试
        # print(n1["refer"]["value"])
        # print(i1["mentions"]["value"])
        # print(n1.text)
        # print(n2.text)
        assert True
