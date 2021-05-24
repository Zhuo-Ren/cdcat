from flask import Flask, render_template, request, jsonify
from typing import Dict, List, Tuple, Union  # for type hinting
#
import nlp_platform.log_config
import logging
#
from nlp_platform.center.node import Node
from nlp_platform.center.nodepool import NodePool
from nlp_platform.center.instance import Instance
from nlp_platform.center.instancepool import InstancePool
from nlp_platform.center.relation import Relation
from nlp_platform.center.relationpool import RelationPool


def cdcat(node_pool: NodePool, instance_pool: InstancePool, relation_pool) -> None:
    """
    This is a manual annotation tool for cross-document coreference.

    :param node_pool: nodes info in the form of *center.ntree*.
    :param instance_pool: instances info in the form of *center.instances*.
    """
    # 1. app init
    app = Flask(__name__)
    from datetime import timedelta
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

    # 2. load config files
    # 2.1 load config.py
    from nlp_platform.plug_in.manual_annotation_tool.cdcat import config
    # 2.2 load config_label.json
    import json
    import sys
    import os
    cur_file_path = os.path.abspath(sys.argv[0])
    cur_folder_path = os.path.dirname(cur_file_path)
    config_label_file_path = os.path.join(cur_folder_path, "config_label.json")
    with open(config_label_file_path, 'r', encoding='utf8') as f:
        config_label = json.load(f)
    # 2.3 load config_lang.json
    config_lang_file_path = os.path.join(cur_folder_path, "config_lang.json")
    with open(config_lang_file_path, 'r', encoding='utf8') as f:
        config_lang = json.load(f)


    @app.route('/')
    def init():
        return render_template("main.html",
                               langDict=config_lang,
                               labelSysDict=config_label)

    @app.route('/getText', methods=["POST"])
    def getText():
        """
        given the position of a target node. for each leaf node of the target node, return char and position.

        - AjaxParam: **textNodeId** (str) [required]: postion of the target node.

        :return: jsonify( [{"char": char of the 0th leaf node, "position": position of the 1th leaf node}, {...}, ...] )
        """
        # receive ajax param, type hint, and normalization
        text_node_position = request.form.get("textNodeId")
        logging.debug("getText->：position=" + str(text_node_position))
        if not isinstance(text_node_position, str):
            raise TypeError("ajax param 'textNodeId' should be in str form.")
            logging.debug(
                "getText<-：" + "(false)" + "：" + "ajax param 'textNodeId' should be in str form")
            return jsonify("ajax param 'textNodeId' should be in str form.")
        try:
            text_node_position = node_pool.str_to_position(text_node_position)
        except:
            raise RuntimeError(
                "the positin str given by ajax param 'textNodeId' can not convert into a position obj.")
            logging.debug(
                "getText<-：" + "(false)" + "：" + "the positin str given by ajax param 'textNodeId' can not convert into a position obj.")
            return jsonify(
                "the positin str given by ajax param 'textNodeId' can not convert into a position obj.")
        logging.debug("getText--：the node text is:" + node_pool[text_node_position].text())
        #
        text_unit_list = []
        for cur_nleaf in node_pool[text_node_position].all_nleaves():
            p = [str(i) for i in cur_nleaf.position()]
            text_unit_list.append({
                "char": cur_nleaf[0],
                "position": "-".join(p)
            })
        #
        logging.debug("getText<-：" + "(success)" + "：" + str(text_unit_list))
        return jsonify(text_unit_list)

    @app.route('/getCatalogue', methods=["POST"])
    def getCatalogue():
        """
        return the catalogue of the corpus.

        The nodes in ntree is divided into 3 category:
            - file node: node which has a label of "article=True". Format: ("node position", "node name, that is the top 6 chars of node string")
            - folder node: the parent node of file node. Format: ["node position", child1, child2, ...]
            - normal node: the child node of normal node.

        The tree structure, which is constructed by folder nodes and file nodes, is considered as a catalogue of file
        nodes. This catalogue will display in CDCAT UI, and user should select one file node to load it and label it.

        A example of content::
            content = ["",
                ["0",
                    ["0-0",
                        ("0-0-0", "哈哈哈哈"),
                    ],
                    ("0-1", "嘿嘿嘿")
                ],
                ("1", "嘻嘻嘻"),
                ["2",
                    ["2-0",
                        ("2-0-0", "吼吼吼"),
                        ("2-0-1", "桀桀桀")
                    ],
                    ["2-1",
                        ("2-1-0", "呱呱呱"),
                        ("2-1-1", "汪汪汪")
                    ]
                ]
            ]

        :return: jsonify(content)
        """

        # 迭代函数
        def walk_to_file(node: node_pool):
            content = [node_pool.position_to_str(node.position())]
            for cur_node in node_pool:
                try:
                    if cur_node.get_label()["article"] == True:
                        is_file = True
                    else:
                        is_file = False
                except:
                    is_file = False
                if is_file:
                    content.append((
                        node_pool.position_to_str(cur_node.position()),
                        cur_node.text()[0:7]
                    ))
                else:
                    content.append(walk_to_file(cur_node))
            return content

        # 获取目录结构
        content = walk_to_file(node_pool)
        # 返回目录结构
        return jsonify(content)

    @app.route('/getGroup', methods=["POST"])
    def getGroup():
        return jsonify(["success", instance_pool.groups])

    @app.route('/changeGroupName', methods=["POST"])
    def changeGroupName():
        groupIndexList = eval("[" + request.form.get("groupPath") + "]")
        groupName = request.form.get("groupName")
        curGroup = instance_pool.groups
        for i in groupIndexList:
            curGroup = curGroup[2][i]
        curGroup[1] = groupName
        return jsonify(["success"])

    @app.route('/prependGroup', methods=["POST"])
    def prependGroup():
        indexTuple = eval("[" + request.form.get("parentPath") + "]")
        curParent = instance_pool.groups
        for i in indexTuple:
            curParent = curParent[2][i]
        curParent[2].insert(0, ["group", "GName", []])
        return jsonify(["success"])

    @app.route('/prependInstances', methods=["POST"])
    def prependInstances():
        indexTuple = eval("[" + request.form.get("parentPath") + "]")
        curParent = instance_pool.groups
        for i in indexTuple:
            curParent = curParent[2][i]
        curParent[2].insert(0, ["instances", "EName", []])
        return jsonify(["success"])

    @app.route('/copyInstance', methods=["POST"])
    def copyInstance():
        index_tuple = eval("[" + request.form.get("parentPath") + "]")
        parent = instance_pool.groups
        for i in index_tuple[:-1]:
            parent = parent[2][i]
        child_index = index_tuple[-1]
        child = parent[2][child_index]
        parent[2].insert(child_index, child)
        return jsonify(["success"])

    @app.route('/moveLi', methods=["POST"])
    def moveLi():
        from_path = eval("[" + request.form.get("fromPath") + "]")
        to_path = eval("[" + request.form.get("toPath") + "]")
        #
        from_parent = instance_pool.groups
        for i in from_path[:-1]:
            from_parent = from_parent[2][i]
        child_index = from_path[-1]
        child = from_parent[2][child_index]
        del from_parent[2][child_index]
        #
        to_parent = instance_pool.groups
        for i in to_path[:-1]:
            to_parent = to_parent[2][i]
        child_index = to_path[-1]
        to_parent[2].insert(child_index, child)
        #
        return jsonify(["success"])

    @app.route('/delLi', methods=["POST"])
    def delLi():
        index_tuple = eval("[" + request.form.get("parentPath") + "]")
        parent = instance_pool.groups
        for i in index_tuple[:-1]:
            parent = parent[2][i]
        child_index = index_tuple[-1]
        del parent[2][child_index]
        return jsonify(["success"])

    @app.route('/addNode', methods=["POST"])
    def addNode():
        """
        Given a position list of a range of child nodes, this function create a parent node for those child nodes.

        - AjaxParam: **childrenNodePositionList** (List[str]) [required]: position list of a range of child nodes.

        :return:
        """
        # ajax in
        try:
            children_node_position_list = request.form.getlist("childrenNodePositionList[]")
            logging.debug("addNode->：childrenNodePositionList=" + str(children_node_position_list))
        except:
            raise RuntimeError("lose the param 'childrenNodePositionList'")
            logging.debug("addNode--:Error: " + "lose the param 'childrenNodePositionList'")
            logging.debug("addNode<-：" + "(failed):" + " ''")
            return ""
        # param normalization
        try:
            children_node_position_list = [i.split("-") for i in children_node_position_list]
            children_node_position_list = [[int(j) for j in i] for i in children_node_position_list]
            children_node_list = [node_pool[i] for i in children_node_position_list]
        except:
            raise RuntimeError(
                "Can not get target node based on a certain position given by param 'childrenNodePositionList'.")
            logging.debug(
                "addNode--:Error: " + "Can not get target node based on a certain position given by param 'childrenNodePositionList'.")
            logging.debug("addNode<-：" + "(failed):" + " ''")
            return ""
        logging.debug("addNode--：children_node_text=" + str([i.text() for i in children_node_list]))
        # create new node
        try:
            new_node: NodeTree = node_pool.add_parent({}, children_node_list)
        except RuntimeError:
            logging.debug("addNode<-Error：" + "can not create the new node.")
            logging.debug("addNode<-：" + "(failed):" + " ''")
            return ""
        if new_node is None:
            logging.debug("addNode<-Error：" + "can not create the new node.")
            logging.debug("addNode<-：" + "(failed):" + " ''")
            return ""
        # ajax out
        else:
            new_node_info = new_node.readable()
            new_node_info.update({"test": None})
            logging.debug("addNode<-：" + str(["success", new_node_info]))
            return jsonify(["success", new_node_info])

    @app.route('/getNode', methods=["POST"])
    def getNode():
        # get params(for js function "getNodeByPosition")
        position = node_pool.str_to_position(request.form.get("position"))
        # get params(for js function "getNodeByChild")
        start_position = node_pool.str_to_position(request.form.get("start"))
        end_position = node_pool.str_to_position(request.form.get("end"))
        # get node(for js function "getNodeByPositon")
        if position:
            logging.debug("getNode->：position=" + str(position))
            node = node_pool[position]
        # get node(for js function "getNodeByChild")
        elif start_position and end_position:
            logging.debug("getNode->：position=" + str(start_position) + '-' + str(end_position))
            node = node_pool.is_annotated(node_pool, start_position, end_position)
        # return(success)
        if node is not None:
            logging.debug("getNode--：get the input node:" + node.text())
            anno_info = node.readable()
            anno_info["position"] = node.position(output_type="string")
            logging.debug("getNode<-：" + str(["success", anno_info]))
            return jsonify(["success", anno_info])
        # return(failed)
        else:
            logging.debug("getNode<-:" + str(["failed", "no such node."]))
            #
            return jsonify(["failed", "no such node."])

    @app.route('/setNode', methods=["POST"])
    def setNode():
        position = node_pool.str_to_position(request.form.get("position"))
        logging.debug("setNode->：position=" + str(position))
        node = node_pool[position]
        if node is None:
            logging.debug("setNode--：no such node")
            logging.debug("getNode<-：\"\"")
            return jsonify("can not find node based on given position.")
        elif isinstance(node, NodeTree):
            cur_labels = node.labels
            # 对每一个定制标签
            for cur_label_key in cur_labels.config.keys():
                # 如果前台修改了当前标签
                if cur_label_key in request.form:
                    cur_label_ajax_parm = request.form.get(cur_label_key)
                    #
                    if cur_label_key not in cur_labels:
                        from nlp_platform.center.labeltypes import labeltypes
                        cur_labels[cur_label_key] = labeltypes[cur_labels.config[cur_label_key]["value_type"]](owner=cur_labels, key=cur_label_key, value=None)
                    cur_label = cur_labels[cur_label_key]
                    cur_label.ajax_process(cur_label_ajax_parm, node_pool, instance_pool)
            logging.debug("setNode<-：" + str(["success", node.readable()]))
            return jsonify(["success", node.readable()])

    @app.route('/delNode', methods=["POST"])
    def delNode():
        pass

    @app.route('/addInstance', methods=["POST"])
    def addInstance():
        position = node_pool.str_to_position(request.form.get("position"))
        if position:  # 使用快捷键，基于一个node创建instance
            # 因为→键的实现改成了模拟多次点击，所以这一段逻辑暂时用不到了。
            node = node_pool[position]
            logging.debug("addInstance_node->：position=" + str(position))
            instance = instance_pool.add_instance({"desc": node.text()})
            if "mention_list" not in instance.labels:
                from nlp_platform.center.labeltypes import labeltypes
                instance.labels["mention_list"] = labeltypes["nodelist"](owner=instance.labels, key="mention_list")
            instance.labels["mention_list"].value.append([node])
            node.add_label({"instance": instance})
        else:  # 单纯创建一个instance
            logging.debug("addInstance_empty->：")
            # 创建instance
            instance = instance_pool.add_instance()
            # 创建instancelink
            instance_pool.groups[2][0][2].insert(0, instance)
        logging.debug("addInstance->：" + str(["success", instance.readable()]))
        return jsonify(["success", instance.readable()])

    @app.route('/getInstance', methods=["POST"])
    def getInstance():
        instance_id = request.form.get("instance_id")
        logging.debug("getInstance->：id=" + instance_id)
        target_instance = instance_pool.get_instance(info_dict={"id":instance_id})[0]
        instance_info = target_instance.readable()
        logging.debug("getInstance<-：" + str(["success", instance_info]))
        return jsonify(["success", instance_info])

    @app.route('/setInstance', methods=["POST"])
    def setInstance():
        id = request.form.get("id")
        logging.debug("setInstance->：id=" + id)

        id = int(id)
        instance = instance_pool.get_instance(info_dict={"id": id})[0]
        if instance is None:
            logging.debug("setInstance--：no such instance")
            logging.debug("setInstance<-：", str(["failed", "no such instance."]))
            return jsonify(["failed", "no such instance."])
        elif isinstance(instance, Instance):
            # 对固定标签desc
            if "desc" in request.form:
                instance["desc"] = request.form.get("desc")
            # 对每一个定制标签
            cur_labels = instance.labels
            for cur_label_key in cur_labels.config.keys():
                # 如果前台修改了当前标签
                if cur_label_key in request.form:
                    cur_label_ajax_param = request.form.get(cur_label_key)
                    # 如果前台修改的这个标签还没有创建，要先创建空标签
                    if cur_label_key not in cur_labels:
                        from nlp_platform.center.labeltypes import labeltypes
                        cur_label_class = labeltypes[cur_labels.config[cur_label_key]["value_type"]]
                        cur_labels[cur_label_key] = cur_label_class(owner=cur_labels, key=cur_label_key, value=None)
                    # 根据前台信息，修改当前标签
                    cur_label = cur_labels[cur_label_key]
                    r = cur_label.ajax_process(cur_label_ajax_param, node_pool, instance_pool)
                    if r is not None:
                        logging.debug("setInstance<-：" + str(["failed", r]))
                        return jsonify(["failed", r])

            logging.debug("setInstance<-：" + str(["success", instance.readable()]))
            return jsonify(["success", instance.readable()])

        # # 获取参数
        # id = int(request.form.get("id"))
        # desc = request.form.get("desc")
        # kg = request.form.get("kg")
        # mention_list_action = request.form.get("mention_list[action]")
        # #
        # instance = instance_pool.get_instance(id=id)[0]
        # logging.debug("setInstance->：id=" + str(id) + "：" + instance["desc"])
        # #
        # if desc:
        #     logging.debug("getInstance->：desc=" + desc)
        #     instance["desc"] = desc
        # if kg:
        #     logging.debug("getInstance->：kg=" + kg)
        #     instance["kg"] = kg
        # if mention_list_action:
        #     if mention_list_action == 'del mention':
        #         # edit instance
        #         mention_list_index = int(request.form.get('mention_list[mention_list_index]'))
        #         mention_index = int(request.form.get('mention_list[mention_index]'))
        #         deletedNode = instance["mention_list"][mention_list_index][mention_index]
        #         del instance["mention_list"][mention_list_index][mention_index]
        #         # if instance["mention_list"][mention_list_index] == []:  # 删除空mentionList
        #         #     if len(instance["mention_list"]) > 1:  # 如果空mentionList是最后一个mentionList，就不删
        #         #         del instance["mention_list"][mention_list_index]
        #         # edit node
        #         deletedNode.del_label("instance")
        #     elif mention_list_action == 'append mention':
        #         mention_list_index = int(request.form.get('mention_list[mention_list_index]'))
        #         cur_node_position = request.form.get('mention_list[new_node_position]')
        #         cur_node_position = root_node.str_to_position(cur_node_position)
        #         cur_node = root_node[cur_node_position]
        #         new_instance = instance
        #         # 操作合理性检测（node原来的instance是否和新instance一致）
        #         if "instance" in cur_node.get_label():  # 如果node的instance标签原先有值，那么还要修改这个instance的mentionList
        #             old_instance = cur_node.get_label()["instance"]
        #             if old_instance == new_instance:
        #                 return jsonify(
        #                     "can not build a reference relation between cur node and cur instance, because is already existing.")
        #         # edit new instance
        #         instance["mention_list"][mention_list_index].append(cur_node)
        #         # edit old instance
        #         if "instance" in cur_node.get_label():  # 如果node的instance标签原先有值，那么还要修改这个instance的mentionList
        #             old_instance = cur_node.get_label()["instance"]
        #             mentionLists = old_instance["mention_list"]
        #             for mentionList in mentionLists:
        #                 if cur_node in mentionList:
        #                     mentionList.remove(cur_node)
        #             old_instance["mention_list"] = mentionLists
        #         # edit node
        #         cur_node.add_label({'instance': instance})
        #     elif mention_list_action == 'del mentionList':
        #         mention_list_index = int(request.form.get('mention_list[mention_list_index]'))
        #         del instance["mention_list"][mention_list_index]
        #     elif mention_list_action == 'append mentionList':
        #         instance["mention_list"].append([])
        # logging.debug("setInstance<-：(success)")
        # return jsonify("success")

    @app.route('/delInstance', methods=["POST"])
    def delInstance():
        instance_id = request.form.get("instance_id")
        logging.debug("delInstance->：id=" + instance_id)
        instance = instance_pool.get_instance({"id": instance_id})[0]
        instance.labels.clear()
        del instance_pool[int(instance_id)]
        # del instancelink
        instance_pool.del_instancelink(instance)
        return jsonify(["success"])

    @app.route('/save', methods=["POST"])
    def save():
        from nlp_platform.plug_in.output.instances_to_pickle import output_instances_to_pickle
        from nlp_platform.plug_in.output.ntree_to_pickle import output_ntree_to_pickle
        output_ntree_to_pickle(node_pool)
        output_instances_to_pickle(instance_pool)
        return jsonify({"success": True})

    app.run(debug=True)
    print("请在浏览器中打开http://127.0.0.1:5000/ ")