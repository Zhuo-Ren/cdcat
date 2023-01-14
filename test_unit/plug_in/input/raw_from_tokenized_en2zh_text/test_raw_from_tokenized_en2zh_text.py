from nlp_platform.plug_in.input.raw_from_tokenized_en2zh_text import dict_from_tokenized_en2zh_text, raw_from_tokenized_en2zh_text
import os


class TestRawFromTokenizedEn2ZhText:
    """test dict_from_tokenized_en2zh_text(). <ref20221230210752>"""
    def test_dict_from_pure_text(self):
        truth = {
            '1': {
                '1.0': "Another day in Hollywood ; another star in rehab .\n好莱坞的又一天;又一个康复中心的明星。\nPeople said Reid 's representative Jack Ketsoyan confirmed the actress 's stay at Promises .\n《人物》杂志称，里德的经纪人杰克·凯索安证实了她将住在承诺酒店。\n",
                '1.1': {
                    '1.1.0': 'http : / / www . accesshollywood . com / lindsay - lohan - leaves - betty - ford - checks - into - malibu - rehab _ article _ 80744\nhttp : / / www . accesshollywood . com / lindsay - lohan - leaves - betty - ford - checks - into - malibu - rehab _ article _ 80744\nLindsay Lohan Leaves Betty Ford , Checks Into Malibu Rehab\n林赛·罗韩离开贝蒂·福特，入住马里布戒毒所\nFirst Published : June 13 , 2013 4 : 59 PM EDT\n首次发布时间:2013年6月13日美国东部时间下午4:59\n'
                }
            }, 
            '2': {
                '2.1': 'Lawyer : Lindsay Lohan checks into rehab facility\n律师:林赛·罗韩入住康复中心\n',
                '2.2': 'Lindsay Lohan Checks Out Of Rehab . . . To Check Into Different Rehab Centre\n林赛·罗韩从戒毒所出来…入住不同的康复中心\n'
            }
        }
        path = "corpus"
        cur_file_path = os.path.abspath(__file__)
        cur_folder_path = os.path.dirname(cur_file_path)
        path = os.path.join(cur_folder_path, path)
        assert truth == dict_from_tokenized_en2zh_text(path=path, file_suffix=".txt")

    """test dict_from_tokenized_en2zh_text(). <ref20221230210752>"""

    def test_raw_from_tokenized_en2zh_text(self):
        """test raw_from_tokenized_en2zh_text(). <ref20221230213431>"""
        truth = {
            '1': {
                '1.0': "Another day in Hollywood ; another star in rehab .\n好莱坞的又一天;又一个康复中心的明星。\nPeople said Reid 's representative Jack Ketsoyan confirmed the actress 's stay at Promises .\n《人物》杂志称，里德的经纪人杰克·凯索安证实了她将住在承诺酒店。\n",
                '1.1': {
                    '1.1.0': 'http : / / www . accesshollywood . com / lindsay - lohan - leaves - betty - ford - checks - into - malibu - rehab _ article _ 80744\nhttp : / / www . accesshollywood . com / lindsay - lohan - leaves - betty - ford - checks - into - malibu - rehab _ article _ 80744\nLindsay Lohan Leaves Betty Ford , Checks Into Malibu Rehab\n林赛·罗韩离开贝蒂·福特，入住马里布戒毒所\nFirst Published : June 13 , 2013 4 : 59 PM EDT\n首次发布时间:2013年6月13日美国东部时间下午4:59\n'
                }
            },
            '2': {
                '2.1': 'Lawyer : Lindsay Lohan checks into rehab facility\n律师:林赛·罗韩入住康复中心\n',
                '2.2': 'Lindsay Lohan Checks Out Of Rehab . . . To Check Into Different Rehab Centre\n林赛·罗韩从戒毒所出来…入住不同的康复中心\n'
            }
        }
        from nlp_platform.center.raw import Raw
        truth = Raw(truth)
        path = "corpus"
        cur_file_path = os.path.abspath(__file__)
        cur_folder_path = os.path.dirname(cur_file_path)
        path = os.path.join(cur_folder_path, path)
        assert truth == raw_from_tokenized_en2zh_text(path=path, file_suffix=".txt")
