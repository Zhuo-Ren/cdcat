from flask import Flask, render_template, request, jsonify
#
import logging
#
from nlp_platform.center.nodepool import NodePool
from nlp_platform.center.instance import Instance
from nlp_platform.center.instancepool import InstancePool
from nlp_platform.center.corpus import Corpus
from nlp_platform.center.raw import Raw


def cdcat(corpus: Corpus) -> None:
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
    # 2.2 load config_label.json
    import json
    import sys
    import os
    cur_file_path = os.path.abspath(__file__)
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
            text_raw = corpus.raw[text_node_position]
        except:
            raise RuntimeError(
                "the positin str given by ajax param 'textNodeId' can not convert into a position obj.")
            logging.debug(
                "getText<-：" + "(false)" + "：" + "the positin str given by ajax param 'textNodeId' can not convert into a position obj.")
            return jsonify(
                "the positin str given by ajax param 'textNodeId' can not convert into a position obj.")
        logging.debug("getText--：the raw's text is:" + text_raw)

        text_unit_list = []
        i = 0
        for cur_word in text_raw:
            text_unit_list.append({
                "char": cur_word,
                "id": "%s-%s" % (str(i), str(i+1))
            })
            i += 1
        #
        logging.debug("getText<-：" + "(success)" + "：" + str(text_unit_list))
        return jsonify(text_unit_list)

    @app.route('/getCatalogue', methods=["POST"])
    def getCatalogue(): # 把注释写到这里
        """
        return the catalogue of the corpus.

        The nodes in ntree is divided into 3 category:
            - file node: node which has a label of "article=True". Format: ("node position", "node name, that is the top 6 chars of node string")
            - folder node: the parent node of file node. Format: ["node position", child1, child2, ...]
            - normal node: the child node of normal node.

        The tree structure, which is constructed by folder nodes and file nodes, is considered as a catalogue of file
        nodes. This catalogue will display in CDCAT UI, and user should select one file node to load it and label it.

        A example of content::
            content = [
                  "folder1",
                  [
                   "folder11",
                   ("folder1/folder11/text1.raw.txt", "text11.raw.txt")
                  ],
                  ("folder1/text2.raw.txt", "text2.raw.txt"),
                  [
                   "folder12",
                   ("folder1/folder12/text12.raw.txt", "text12.raw.txt")
                  ]
                ]

        :return: jsonify(content)
        """
        # 迭代函数
        import re
        def walk_to_file(raw, content=None, path_list=[]):
            if content == None:
                content = []
                content.append("raw")
            path = str()
            for key, value in raw.items():
                if re.search("raw.txt", key, flags=0):
                    path = ""
                    for p in path_list:
                        path += "%s/" % p
                    if path is "":
                        content.append((key, key))
                    else:
                        content.append(("%s" % path+key, key))
                else:
                    path_list.append(key)
                    l = []
                    l.append(key)
                    path += "%s" % key
                    walk_to_file(raw[key], content=l, path_list=path_list)
                    content.append(l)
                    path_list.pop()
            return content

        # 获取目录结构
        content = walk_to_file(corpus.raw)
        # 返回目录结构

        return jsonify(content)

    @app.route('/getGroup', methods=["POST"])
    def getGroup():
        groups = corpus.ip.groups
        def f(x):
            if isinstance(x, list):
                # instances的情况
                if len(x) == 3:
                    if x[0] == "instances":
                        r = []
                        r.append(x[0])
                        r.append(x[1])
                        r.append([])
                        r[2] = []
                        for i in x[2]:
                            cur_instance = corpus.ip[i]
                            r[2].append(cur_instance.to_info())
                        return r
                # 其他情况
                r = []
                for i in x:
                    r.append(f(i))
                return r
            else:
                return x
        groups = f(groups)
        return jsonify(["success", groups])

    @app.route('/changeGroupName', methods=["POST"])
    def changeGroupName():
        groupIndexList = eval("[" + request.form.get("groupPath") + "]")
        groupName = request.form.get("groupName")
        curGroup = corpus.ip.groups
        for i in groupIndexList:
            curGroup = curGroup[2][i]
        curGroup[1] = groupName
        return jsonify(["success"])

    @app.route('/prependGroup', methods=["POST"])
    def prependGroup():
        indexTuple = eval("[" + request.form.get("parentPath") + "]")
        curParent = corpus.ip.groups
        for i in indexTuple:
            curParent = curParent[2][i]
        curParent[2].insert(0, ["group", "GName", []])
        return jsonify(["success"])

    @app.route('/prependInstances', methods=["POST"])
    def prependInstances():
        indexTuple = eval("[" + request.form.get("parentPath") + "]")
        curParent = corpus.ip.groups
        for i in indexTuple:
            curParent = curParent[2][i]
        curParent[2].insert(0, ["instances", "EName", []])
        return jsonify(["success"])

    @app.route('/copyInstance', methods=["POST"])
    def copyInstance():
        index_tuple = eval("[" + request.form.get("parentPath") + "]")
        parent = corpus.ip.groups
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
        from_parent = corpus.ip.groups
        for i in from_path[:-1]:
            from_parent = from_parent[2][i]
        child_index = from_path[-1]
        child = from_parent[2][child_index]
        del from_parent[2][child_index]
        #
        to_parent = corpus.ip.groups
        for i in to_path[:-1]:
            to_parent = to_parent[2][i]
        child_index = to_path[-1]
        to_parent[2].insert(child_index, child)
        #
        return jsonify(["success"])

    @app.route('/delLi', methods=["POST"])
    def delLi():
        index_tuple = eval("[" + request.form.get("parentPath") + "]")
        parent = corpus.ip.groups
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
            children_node_list = [corpus.np[i] for i in children_node_position_list]
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
            new_node: NodeTree = corpus.np.add_parent({}, children_node_list)
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
        position = corpus.np.str_to_position(request.form.get("position"))
        # get params(for js function "getNodeByChild")
        start_position = corpus.np.str_to_position(request.form.get("start"))
        end_position = corpus.np.str_to_position(request.form.get("end"))
        # get node(for js function "getNodeByPositon")
        if position:
            logging.debug("getNode->：position=" + str(position))
            node = corpus.np[position]
        # get node(for js function "getNodeByChild")
        elif start_position and end_position:
            logging.debug("getNode->：position=" + str(start_position) + '-' + str(end_position))
            node = corpus.np.is_annotated(corpus.np, start_position, end_position)
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
        position = corpus.np.str_to_position(request.form.get("position"))
        logging.debug("setNode->：position=" + str(position))
        node = corpus.np[position]
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
                    cur_label.ajax_process(cur_label_ajax_parm, corpus.np, corpus.ip)
            logging.debug("setNode<-：" + str(["success", node.readable()]))
            return jsonify(["success", node.readable()])

    @app.route('/delNode', methods=["POST"])
    def delNode():
        pass

    @app.route('/addInstance', methods=["POST"])
    def addInstance():
        position = corpus.np.str_to_position(request.form.get("position"))
        if position:  # 使用快捷键，基于一个node创建instance
            # 因为→键的实现改成了模拟多次点击，所以这一段逻辑暂时用不到了。
            node = corpus.np[position]
            logging.debug("addInstance_node->：position=" + str(position))
            instance = corpus.ip.add_instance({"desc": node.text()})
            if "mention_list" not in instance.labels:
                from nlp_platform.center.labeltypes import labeltypes
                instance.labels["mention_list"] = labeltypes["nodelist"](owner=instance.labels, key="mention_list")
            instance.labels["mention_list"].value.append([node])
            node.add_label({"instance": instance})
        else:  # 单纯创建一个instance
            logging.debug("addInstance_empty->：")
            # 创建instance
            instance = corpus.ip.add_instance()
            # 创建instancelink
            corpus.ip.groups[2][0][2].insert(0, instance)
        logging.debug("addInstance->：" + str(["success", instance.readable()]))
        return jsonify(["success", instance.readable()])

    @app.route('/getInstance', methods=["POST"])
    def getInstance():
        instance_id = request.form.get("instance_id")
        logging.debug("getInstance->：id=" + instance_id)
        target_instance = corpus.ip.get_instance(id=instance_id)[0]
        instance_info = target_instance.to_info()
        logging.debug("getInstance<-：" + str(["success", instance_info]))
        return jsonify(["success", instance_info])

    @app.route('/setInstance', methods=["POST"])
    def setInstance():
        id = request.form.get("id")
        logging.debug("setInstance->：id=" + id)
        instance = corpus.ip.get_instance(id=id)[0]
        if instance is None:
            logging.debug("setInstance--：no such instance")
            logging.debug("setInstance<-：", str(["failed", "no such instance."]))
            return jsonify(["failed", "no such instance."])
        elif isinstance(instance, Instance):
            # # 对固定标签desc
            # if "desc" in request.form:
            #     instance["desc"] = request.form.get("desc")
            # 对每一个定制标签
            cur_labels = instance.keys()
            for cur_label_key in instance.config["LABELS"].keys():
                # 如果前台修改了当前标签
                if cur_label_key in request.form:
                    cur_label_ajax_param = request.form.get(cur_label_key)
                    # 如果前台修改的这个标签还没有创建，要先创建空标签
                    if cur_label_key not in cur_labels:
                        from nlp_platform.center.labeltypes import label_types
                        for label_key, label_config in instance.config["LABELS"].items():
                            if label_key == cur_label_key:
                                label_config["key"] = label_key
                                label_config["PRELIMINARY_CODE"] = instance.config["PRELIMINARY_CODE"]
                                instance[label_key] = label_types[label_config["type"]](config=label_config, owner=instance)
                    # 根据前台信息，修改当前标签
                    cur_label = instance[cur_label_key]
                    r = cur_label.ajax_process(cur_label_ajax_param)
                    if r is not None:
                        logging.debug("setInstance<-：" + str(["failed", r]))
                        return jsonify(["failed", r])

            logging.debug("setInstance<-：" + str(["success", instance.to_info()]))
            return jsonify(["success", instance.to_info()])

        # # 获取参数
        # id = int(request.form.get("id"))
        # desc = request.form.get("desc")
        # kg = request.form.get("kg")
        # mention_list_action = request.form.get("mention_list[action]")
        # #
        # instance = corpus.ip.get_instance(id=id)[0]
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
        instance = corpus.ip.get_instance({"id": instance_id})[0]
        instance.labels.clear()
        del corpus.ip[int(instance_id)]
        # del instancelink
        corpus.ip.del_instancelink(instance)
        return jsonify(["success"])

    @app.route('/save', methods=["POST"])
    def save():
        from nlp_platform.plug_in.output.instances_to_pickle import output_instances_to_pickle
        from nlp_platform.plug_in.output.ntree_to_pickle import output_ntree_to_pickle
        output_ntree_to_pickle(corpus.np)
        output_instances_to_pickle(corpus.ip)
        return jsonify({"success": True})

    app.run(debug=True)
    print("请在浏览器中打开http://127.0.0.1:5000/ ")
