from nlp_plantform.center.mytree import mytree
from nlp_plantform.plug_in.input.input_from_string_plaintext_form import input_from_string_plaintext_form
from  dbsql.dbsql_sqlite import DbSql

def input_from_sqlite(path: str, table_name: str)-> mytree:
    """ read a sqlite database, and genera the node.

    The database in *path* should have a table named *table_name*.
    And this table should have the following rows:
    * 新闻标题
    * 新闻日期年
    * 新闻日期月
    * 新闻日期日
    * 新闻正文

    This function create a root node, and each line in the database
    corresponds to a child node.

    :param path: The path to sqlite database.
    :return: A node corresponding to the file.
    """
    try:
        # 链接数据库
        DbSql.connectDataBase(path)
        # 从数据库读取语料，得到语料列表
        if not DbSql.isTableExists(table_name):
            raise RuntimeError("there is no table named " + table_name)
        response = DbSql.selectRow(table_name)
    finally:
        DbSql.disconnectDataBase()
    news_list = [{"data":i[16:19], "title":i[15], "source":i[13], "text":i[19]} for i in response]
    """
    语料列表，每一行就是一条新闻。
    """
    # 把语料列表中的每一行，处理成为新闻节点
    news_node_list = []
    for cur_news in news_list:
        # 读取语料，形成新闻节点
        cur_news_node = input_from_string_plaintext_form(cur_news["text"])
        cur_news_node.add_label({"data": cur_news["data"], "source":cur_news["source"]})
        cur_title_node = input_from_string_plaintext_form(cur_news["title"])
        cur_title_node.add_label({"title": True})
        cur_news_node.insert(0,cur_title_node)
        # 新闻节点添加到root节点
        news_node_list.append(cur_news_node)
    #
    root = mytree(label_dict={},children=news_node_list)
    print(1)
    # node = input_from_string_plaintext_form(fileStr)
    # node.add_label({"file": True})


