import pytest

class Test_Raw:

    def test_init_with_default(self):
        from nlp_platform.center.raw import Raw
        r1 = Raw()

    def test_init_with_info(self):
        from nlp_platform.center.raw import Raw
        info = {
            "folder1": {
                "text1.raw.txt": "10日，埃航一架飞机坠毁，事故导致机上150人全部死亡。"
            },
            "text2.raw.txt": "当日，埃航展开事故遇难者的赔偿工作",
            "folder2": {
                "text4.raw.txt": "测试用4",
                "folder21": {
                    "text5.raw.txt": "测试用5",
                    "text6.raw.txt": "测试用6"
                }
            }
        }
        r1 = Raw(info)

    def test_getitem_1(self):
        """
        Raw是dict的子类，所以支持dict式的操作。
        """
        info = {
            "folder1": {
                "text1.raw.txt": "10日，埃航一架飞机坠毁，事故导致机上150人全部死亡。"
            },
            "text2.raw.txt": "当日，埃航展开事故遇难者的赔偿工作",
            "folder2": {
                "text4.raw.txt": "测试用4",
                "folder21": {
                    "text5.raw.txt": "测试用5",
                    "text6.raw.txt": "测试用6"
                }
            }
        }
        from nlp_platform.center.raw import Raw
        r1 = Raw(info)
        f = 0
        assert r1["folder1"] == {"text1.raw.txt": "10日，埃航一架飞机坠毁，事故导致机上150人全部死亡。"}
        assert r1["folder1"]["text1.raw.txt"] == "10日，埃航一架飞机坠毁，事故导致机上150人全部死亡。"

    @pytest.mark.parametrize('node_id, text', [
        ["n:folder1/text1.raw.txt:0-3", "10日"],
        ["n:folder2/folder21/text5.raw.txt:1-3", "试用"],
        # ["n:folder1/text1.raw.txt:1-2;5-7", "0航一"]  暂不支持离散指称<ref20221228234825>
    ])
    def test_getitem_2(self, node_id, text):
        """在dict操作的基础上，定制了__getitem__()函数，使之支持node id式的读取方式。"""
        info = {
            "folder1": {
                "text1.raw.txt": "10日，埃航一架飞机坠毁，事故导致机上150人全部死亡。"
            },
            "text2.raw.txt": "当日，埃航展开事故遇难者的赔偿工作",
            "folder2": {
                "text4.raw.txt": "测试用4",
                "folder21": {
                    "text5.raw.txt": "测试用5",
                    "text6.raw.txt": "测试用6"
                }
            }
        }
        from nlp_platform.center.raw import Raw
        r1 = Raw(info)
        f = 0
        assert r1[node_id] == text
