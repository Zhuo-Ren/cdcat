from typing import Dict, List, Tuple, Union  # for type hinting
from nlp_platform.center.nodetree import NodeTree
from nlp_platform.plug_in.input.ntree_from_string_plaintext_form import input_from_string_plaintext_form
from dbsql.dbsql_sqlite import DbSql
import nlp_platform.log_config


def input_ntree_from_sqlite(path: str, table_name: str)-> NodeTree:
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

    # 读取每一行中的指定列
    news_list : List[Dict]= [{"date":i[16:19], "title":i[15], "source":i[13], "text":i[19]} for i in response]
    """
    语料列表，每一行就是一条新闻。
    """

    # 按行读取语料列表，生成新闻节点列表
    news_node_list = []
    for cur_news in news_list:
        # 形成新闻节点
        cur_news_node = input_from_string_plaintext_form(cur_news["text"])
        cur_news_node.labels.update({"date": cur_news["date"], "source": cur_news["source"]})
        cur_news_node.labels.update({"article": True})   # 表示这个一个文章，在cdcat中单独显示。
        # 形成标题节点
        cur_title_node = input_from_string_plaintext_form(cur_news["title"]+"\n")
        cur_title_node.labels.update({"title": True})
        # 把标题节点添加到新闻节点
        cur_news_node.insert(0, cur_title_node)
        # 新闻节点添加到新闻节点列表
        news_node_list.append(cur_news_node)
    #
    root = NodeTree(labels_dict={}, children=news_node_list)
    return root

