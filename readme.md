此程序包含一个平台和诸多插件。平台负责维护数据，插件负责处理数据和IO。

主要的一个插件是CDCAT，一个共指标注软件。CDCAT对输入的文本进行人工标注。运行示例程序`cdcat/test_unit/plug_in/manual_annotation_tool/cacat/cdcat_from_db.py`。此程序会读取`cdcat/data/main.sqlite`数据库中的文本，并打开cdcat标注软件。这是基于web的软件，在浏览器中访问127.0.0.1:5000即可。