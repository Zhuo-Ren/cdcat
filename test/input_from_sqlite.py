from nlp_plantform.plug_in.input.input_from_sqlite import input_from_sqlite

response = input_from_sqlite("../main.sqlite", "websiteTabel")  # 爬虫中table笔误写成了tabel
