from nlp_platform.plug_in.input.raw_from_pure_text import raw_from_pure_text, dict_from_pure_text
import os

class TestRawFromPureText:
    def test_dict_from_pure_text(self):
        """test dict_from_pure_text(). <ref20221230211037>"""
        truth = {
            'folder1': {
                '测试输入': {
                    'text1.raw.txt': '10日，埃航一架飞机坠毁，事故导致机上150人全部死亡。'
                }
            },
            'folder2': {
                'folder21': {
                    'text5.raw.txt': '测试用5',
                    'text6.raw.txt': '测试用6'
                },
                'text4.raw.txt': '测试用4'
            },
            'text2.raw.txt': '当日，埃航展开事故遇难者的赔偿工作',
            'text3.raw.txt': '测试用3'
        }
        path = "corpus"
        cur_file_path = os.path.abspath(__file__)
        cur_folder_path = os.path.dirname(cur_file_path)
        path = os.path.join(cur_folder_path, path)
        assert truth == dict_from_pure_text(path=path)

    def test_raw_from_pure_text(self):
        """test raw_from_pure_text(). <ref20221230212011>"""
        truth = {
            'folder1': {
                '测试输入': {
                    'text1.raw.txt': '10日，埃航一架飞机坠毁，事故导致机上150人全部死亡。'
                }
            },
            'folder2': {
                'folder21': {
                    'text5.raw.txt': '测试用5',
                    'text6.raw.txt': '测试用6'
                },
                'text4.raw.txt': '测试用4'
            },
            'text2.raw.txt': '当日，埃航展开事故遇难者的赔偿工作',
            'text3.raw.txt': '测试用3'
        }
        from nlp_platform.center.raw import Raw
        truth = Raw(truth)
        path = "corpus"
        cur_file_path = os.path.abspath(__file__)
        cur_folder_path = os.path.dirname(cur_file_path)
        path = os.path.join(cur_folder_path, path)
        assert truth == raw_from_pure_text(path=path, fname_regex=".raw.txt")
