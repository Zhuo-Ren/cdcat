from flask import Flask, render_template, request, jsonify
import json
import sys
import os
import logging
#
from nlp_platform.center.nodepool import NodePool
from nlp_platform.center.instance import Instance
from nlp_platform.center.instancepool import InstancePool
from nlp_platform.center.corpus import Corpus
from nlp_platform.center.raw import Raw
from nlp_platform.center.node import Node

def cdcat(
        corpus: Corpus,
        path_to_core_config=None,
        path_to_lang_config=None,
        path_to_label_config=None
) -> None:
    """
    This is a manual annotation tool for cross-document coreference.

    :param corpus:
    :param path_to_core_config:
    :param path_to_lang_config:
    :param path_to_label_config:
    :return:
    """
    # app init
    app = Flask(__name__)
    from datetime import timedelta
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

    # load core config
    if path_to_core_config is None:
        cur_file_path = os.path.abspath(sys.argv[0])
        cur_folder_path = os.path.dirname(cur_file_path)
        path_to_core_config = os.path.join(cur_folder_path, "config_cdcat_core.json")
    with open(path_to_core_config, 'r', encoding='utf8') as f:
        config_core = json.load(f)
        if "save_to" not in config_core:
            config_core["save_to"] = "./corpus"
    # load config_cdcat_label.json
    if path_to_label_config is None:
        cur_file_path = os.path.abspath(sys.argv[0])
        cur_folder_path = os.path.dirname(cur_file_path)
        path_to_label_config = os.path.join(cur_folder_path, "config_cdcat_label.json")
    with open(path_to_label_config, 'r', encoding='utf8') as f:
        config_label = json.load(f)
    # load config_lang.json
    if path_to_lang_config is None:
        cur_file_path = os.path.abspath(__file__)
        cur_folder_path = os.path.dirname(cur_file_path)
        path_to_lang_config = os.path.join(cur_folder_path, "config_lang.json")
    with open(path_to_lang_config, 'r', encoding='utf8') as f:
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
            text_raw = corpus.raw[text_node_position]#
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
                if re.search(config_core["suffix_of_doc_in_raw"], key, flags=0):
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
            from nlp_platform.center.node import Node
            # 获得选中mention的首末position以及file_path
            file_path = request.form.get("file_path")
            info = {}
            # if isinstance(children_node_position_list[0] , str):
            #     children_node_position_list = [i.split("-") for i in children_node_position_list]
            #     children_node_position_first = children_node_position_list[0][0]
            #     children_node_position_last = children_node_position_list[-1][-1]
            #     position = children_node_position_first + "-" + children_node_position_last
            #     # 下面代码有问题，children_node_position_list是嵌套列表
            #     # children_node_position_list = [[int(j) for j in i] for i in children_node_position_list]
            #     # children_node_list = [corpus.np(i) for i in children_node_position_list]
            #     # 将position整理成node_id的形式
            #     node_id = "n:" + file_path + ":" + position
            #     info = {"id": node_id}
            #     # 将mention制作成Node并放入corpus.np里
            #     text = corpus.raw[node_id]
            #     token_id=corpus.raw.to_info(node_id)
            #     info.update({"text": text})
            #     info.update({"token_id": token_id})
            # else:
            #     children_node_index_list=[]
            #     node_list=[]
            #     text = ""
            #     node_id = "n:" + file_path + ":"
            #     for i in children_node_position_list:
            #         for j in i:
            #             children_node_index_list.append(j.split("-"));
            #         node_list.append(children_node_position_list[0][0])
            #         node_list.append(children_node_position_list[-1][-1])
            #         temp_node_id="n:" + file_path + ":"+ node_list.append(children_node_position_list[0][0])+"-"+children_node_position_list[-1][-1]
            #         text = text+corpus.raw[temp_node_id]
            #     position="-".join(node_list)
            #     node_id = "n:" + file_path + ":" + position
            #     info.update({"text": text})
            children_node_position_list = [i.split("-") for i in children_node_position_list]
            position = children_node_position_list[0][0]
            for i in range(0, len(children_node_position_list) - 1):
                if int(children_node_position_list[i][0]) + 1 != int(children_node_position_list[i + 1][0]):
                    position += "-" + children_node_position_list[i][-1] + "-" + children_node_position_list[i + 1][0]
            position += "-" + children_node_position_list[-1][-1]
            text = ""
            token_id = []
            position_list = position.split("-")
            for i in range(0, len(position_list), 2):
                if i < len(position_list) - 2:
                    text += corpus.raw["n:" + file_path + ":" + position_list[i] + "-" + position_list[i + 1]] + " "
                else:
                    text += corpus.raw["n:" + file_path + ":" + position_list[i] + "-" + position_list[i + 1]]
                token_id.append(
                    corpus.raw.to_info("n:" + file_path + ":" + position_list[i] + "-" + position_list[i + 1]))

            # 将position整理成node_id的形式
            node_id = "n:" + file_path + ":" + position
            info = {"id": node_id}
            # 将mention制作成Node并放入corpus.np里
            # text = corpus.raw[node_id]
            # token_id=corpus.raw.to_info(node_id)
            info.update({"text": text})
            # info.update({"token_id": token_id})
            new_node = Node(info=info)
            corpus.np.add(new_node)
            new_node_info = new_node.to_info()

            # new_node_info.update({"text": text})
            logging.debug("addNode<-：" + str(["success", new_node_info]))
            return jsonify(["success", new_node_info])
        except:
            raise RuntimeError(
                "Can not get target node based on a certain position given by param 'childrenNodePositionList'.")
            logging.debug(
                "addNode--:Error: " + "Can not get target node based on a certain position given by param 'childrenNodePositionList'.")
            logging.debug("addNode<-：" + "(failed):" + " ''")

        # except:
        #     raise RuntimeError(
        #         "Can not get target node based on a certain position given by param 'childrenNodePositionList'.")
        #     logging.debug(
        #         "addNode--:Error: " + "Can not get target node based on a certain position given by param 'childrenNodePositionList'.")
        #     logging.debug("addNode<-：" + "(failed):" + " ''")
        #     return ""
        # logging.debug("addNode--：children_node_text=" + str([i.text() for i in children_node_list]))
        # # create new node
        # try:
        #     new_node = corpus.np.add_parent({}, children_node_list)
        # except RuntimeError:
        #     logging.debug("addNode<-Error：" + "can not create the new node.")
        #     logging.debug("addNode<-：" + "(failed):" + " ''")
        #     return ""
        # if new_node is None:
        #     logging.debug("addNode<-Error：" + "can not create the new node.")
        #     logging.debug("addNode<-：" + "(failed):" + " ''")
        #     return ""
        # # ajax out
        # else:
        #     new_node_info = new_node.readable()
        #     new_node_info.update({"test": None})
        #     logging.debug("addNode<-：" + str(["success", new_node_info]))
        #     return jsonify(["success", new_node_info])

    @app.route('/addCurveNode', methods=["POST"])
    def addCurveNode():
        try:
            curve_id = request.form.get("curve_id")
            logging.debug("addCurveNode->：curve_id=" + str(curve_id))
        except:
            raise RuntimeError("lose the param 'childrenNodePositionList'")
            logging.debug("addCurveNode--:Error: " + "lose the param 'childrenNodePositionList'")
            logging.debug("addCurveNode<-：" + "(failed):" + " ''")
            return ""
            # param normalization
        try:
            from nlp_platform.center.node import Node
            # 获得选中mention的首末position以及file_path
            file_path = request.form.get("file_path")
            a_z=request.form.get("a_z")
            b_z=request.form.get("b_z")
            # children_node_position_list = [i.split("-") for i in children_node_position_list]
            # children_node_position_first = children_node_position_list[0][0]
            # children_node_position_last = children_node_position_list[-1][-1]
            # position = children_node_position_first + "-" + children_node_position_last
            # 下面代码有问题，children_node_position_list是嵌套列表
            # children_node_position_list = [[int(j) for j in i] for i in children_node_position_list]
            # children_node_list = [corpus.np(i) for i in children_node_position_list]
            # 将position整理成node_id的形式
            node_id = "n:" + file_path + ":" + curve_id
            info = {"id": node_id}
            # 将mention制作成Node并放入corpus.np里
            text = "curve node"
            token_id = a_z+","+b_z
            info.update({"text": text})
            info.update({"token_id": token_id})
            new_node = Node(info=info)
            corpus.np.add(new_node)
            # new_node.text=text
            # corpus.np[node_id].text=text
            new_node_info = new_node.to_info()
            new_node_info.update({"test": None})
            # new_node_info["text"]= text
            logging.debug("addNode<-：" + str(["success", new_node_info]))
            return jsonify(["success", new_node_info])
        except:
            raise RuntimeError(
                "Can not get target node based on a certain position given by param 'childrenNodePositionList'.")
            logging.debug(
                "addNode--:Error: " + "Can not get target node based on a certain position given by param 'childrenNodePositionList'.")
            logging.debug("addNode<-：" + "(failed):" + " ''")

    @app.route('/getNode', methods=["POST"])
    def getNode():
        # get params(for js function "getNodeByPosition")
        node_id = request.form.get("node_id")
        # get params(for js function "getNodeByChild")
        start_position = request.form.get("start")
        end_position = request.form.get("end")
        file_path = request.form.get("file_path")
        # get node(for js function "getNodeByPositon")
        if node_id:
            logging.debug("getNode->：position=" + str(node_id))
            node = corpus.np[node_id]
        # get node(for js function "getNodeByChild")
        elif start_position and end_position:
            start_position_list = start_position.split('-')
            end_position_list = end_position.split('-')
            position = start_position_list[0] + "-" + end_position_list[1]
            node_id = "n:" + file_path + ":" + position
            logging.debug("getNode->：position=" + str(start_position_list[0]) + '-' + str(end_position_list[1]))
            node = corpus.np.is_annotated(node_id)
        # return(success)
        if node is not None:
            anno_info = node.to_info(text=True)
            logging.debug("getNode<-：" + str(["success", anno_info]))
            return jsonify(["success", anno_info])
        # return(failed)
        else:
            logging.debug("getNode<-:" + str(["failed", "no such node."]))
            #
            return jsonify(["failed", "no such node."])

    @app.route('/setNode', methods=["POST"])
    def setNode():
        node_id = request.form.get("nodeId")
        logging.debug("setNode->：position=" + str(node_id))
        node = corpus.np[node_id]
        if node is None:
            logging.debug("setNode--：no such node")
            logging.debug("getNode<-：\"\"")
            return jsonify("can not find node based on given position.")
        elif isinstance(node, Node):
            cur_labels = node.keys()
            # 对每一个定制标签
            for cur_label_key in node.config["LABELS"].keys():
                # 如果前台修改了当前标签
                if cur_label_key in request.form:
                    cur_label_ajax_parm = request.form.get(cur_label_key)
                    #
                    if cur_label_key not in cur_labels:
                        from nlp_platform.center.labeltypes import label_types
                        for label_key, label_config in node.config["LABELS"].items():
                            if label_key == cur_label_key:
                                label_config["key"] = label_key
                                label_config["PRELIMINARY_CODE"] = node.config["PRELIMINARY_CODE"]
                                node[label_key] = label_types[label_config["type"]](config=label_config, owner=node)
                    cur_label = node[cur_label_key]
                    r = cur_label.ajax_process(cur_label_ajax_parm)
                    if r is not None:
                        return jsonify(["failed", r])
            logging.debug("setNode<-：" + str(["success", node.to_info()]))
            return jsonify(["success", node.to_info()])

    @app.route('/delNode', methods=["POST"])
    def delNode():
        node_id = request.form.get("node_id")
        logging.debug("delNode->：position=" + str(node_id))
        corpus.np.pop(node_id)
        return jsonify(["success", node_id])

    @app.route('/getNodepool', methods=["POST"])
    def getNodepool():
        #
        nodepool=corpus.np
        if nodepool is not None:
            return jsonify(["success",nodepool.to_info()])
        else:
            return jsonify("nodepool is void")

    @app.route('/addInstance', methods=["POST"])
    def addInstance():
        logging.debug("addInstance_empty->：")
        # 创建instance
        new_instance = Instance(info=None, pool=None)
        corpus.ip.add(new_instance)
        logging.debug("addInstance->：" + str(["success", new_instance.to_info()]))
        return jsonify(["success", new_instance.to_info()])

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

    @app.route('/getInstancepool', methods=["POST"])
    def getInstancepool():
        #
        Instancepool = corpus.ip
        if Instancepool is not None:
            return jsonify(["success", Instancepool.to_info()])
        else:
            return jsonify("nodepool is void")

    @app.route('/save', methods=["POST"])
    def save():
        from nlp_platform.plug_in.output.to_files import save
        save(dir="./corpus", corpus=corpus)
        return jsonify({"success": True})

    app.run(debug=True)
    print("请在浏览器中打开http://127.0.0.1:5000/ ")
