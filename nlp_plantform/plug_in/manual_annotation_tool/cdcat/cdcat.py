from flask import Flask, render_template, request, jsonify
from typing import Dict, List, Tuple, Union  # for type hinting
import nlp_plantform.log_config
import json
import logging
from nlp_plantform.plug_in.manual_annotation_tool.cdcat import config
from nlp_plantform.center.nodetree import NodeTree
from nlp_plantform.center.instance import Instance
from nlp_plantform.center.instances import Instances
from nlp_plantform.plug_in.output.instances_to_pickle import output_instances_to_pickle
from nlp_plantform.plug_in.output.ntree_to_pickle import output_ntree_to_pickle
from nlp_plantform.plug_in.manual_annotation_tool.cdcat.label_sys import labelTemplate

def cdcat(ntree: NodeTree, instances: Instances, unit_level: Dict) -> None :
    """
    This is a manual annotation tool for cross-document coreference.

    :param ntree: nodes info in the form of *center.ntree*.
    :param instances: instances info in the form of *center.instances*.
    :param unit_level:
    """
    app = Flask(__name__)

    with open(config.lang_dict_path, 'r', encoding='utf8') as langf:
        lang_dict = json.load(langf)

    with open(config.label_sys_dict_path, 'r', encoding='utf8') as labelf:
        label_sys_dict = json.load(labelf)

    @app.route('/')
    def init():
        return render_template("main.html",
                               instance_dict=instances,
                               langDict=lang_dict,
                               labelSysDict=label_sys_dict)

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
            logging.debug("getText<-：" + "(false)" + "：" + "ajax param 'textNodeId' should be in str form")
            return jsonify("ajax param 'textNodeId' should be in str form.")
        try:
            text_node_position = ntree.str_to_position(text_node_position)
        except:
            raise RuntimeError("the positin str given by ajax param 'textNodeId' can not convert into a position obj.")
            logging.debug("getText<-：" + "(false)" + "：" + "the positin str given by ajax param 'textNodeId' can not convert into a position obj.")
            return jsonify("the positin str given by ajax param 'textNodeId' can not convert into a position obj.")
        logging.debug("getText--：the node text is:" + ntree[text_node_position].text())
        #
        text_unit_list = []
        for cur_nleaf in ntree[text_node_position].all_nleaves():
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
        def walk_to_file(node: ntree):
            content = [ntree.position_to_str(node.position())]
            for cur_node in ntree:
                try:
                    if cur_node.get_label()["article"] == True:
                        is_file = True
                    else:
                        is_file = False
                except:
                    is_file = False
                if is_file :
                    content.append((
                        ntree.position_to_str(cur_node.position()),
                        cur_node.text()[0:7]
                    ))
                else:
                    content.append(walk_to_file(cur_node))
            return content
        # 获取目录结构
        content = walk_to_file(ntree)
        # 返回目录结构
        return jsonify(content)

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
            children_node_list = [ntree[i] for i in children_node_position_list]
        except:
            raise RuntimeError("Can not get target node based on a certain position given by param 'childrenNodePositionList'.")
            logging.debug("addNode--:Error: " + "Can not get target node based on a certain position given by param 'childrenNodePositionList'.")
            logging.debug("addNode<-：" + "(failed):" + " ''")
            return ""
        logging.debug("addNode--：children_node_text=" + str([i.text() for i in children_node_list]))
        # create new node
        try:
            new_node: NodeTree = ntree.add_parent({}, children_node_list)
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
            new_node_info = new_node.labels.readable()
            logging.debug("addNode<-：" + "(success):" + str(new_node_info))
            return jsonify(new_node_info)

    @app.route('/getNode', methods=["POST"])
    def getNode():
        # get params(for js function "getNodeByPositon")
        position = ntree.str_to_position(request.form.get("position"))
        # get params(for js function "getNodeByChild")
        start_position = ntree.str_to_position(request.form.get("start"))
        end_position = ntree.str_to_position(request.form.get("end"))
        # get node(for js function "getNodeByPositon")
        if position:
            logging.debug("getNode->：position=" + str(position))
            node = ntree[position]
        # get node(for js function "getNodeByChild")
        elif start_position and end_position:
            logging.debug("getNode->：position=" + str(start_position) + '-' + str(end_position))
            node = ntree.is_annotated(ntree, start_position, end_position)
        # return(success)
        if node is not None:
            logging.debug("getNode--：get the input node:" + node.text())
            anno_info = node.labels.readable()
            anno_info["position"] = node.position(output_type="string")
            logging.debug("getNode<-：" + str(anno_info))
            return jsonify(anno_info)
        # return(failed)
        else:
            logging.debug("getNode--：no such node.")
            logging.debug("getNode<-：\"\"")
            #
            return ""

    @app.route('/setNode', methods=["POST"])
    def setNode():
        position = ntree.str_to_position(request.form.get("position"))
        logging.debug("setNode->：position=" + str(position))
        node = ntree[position]
        if node is None:
            logging.debug("setNode--：no such node")
            logging.debug("getNode<-：\"\"")
            return jsonify("can not find node based on given position.")
        elif isinstance(node, NodeTree):
            for cur_label_dict in label_sys_dict["node"]:
                if cur_label_dict["key"] in request.form:
                    cur_label_new_value = request.form.get(cur_label_dict["key"])
                    cur_label_set_value_func = labelTemplate[cur_label_dict["value_type"]]
                    cur_label_set_value_func(node, cur_label_dict["key"])
            if request.form.get("token")!=None:
                logging.debug("setNode->：token=" + request.form.get("token"))
                if request.form.get("token") == 'false':
                    del node.get_label()["token"]
                elif request.form.get("token") == 'true':
                    node.add_label({"token": True})
            if request.form.get("type")!=None:
                logging.debug("setNode->：type=" + request.form.get("type"))
                if request.form.get("type") == 'none':
                    del node.get_label()["type"]
                else:
                    node.add_label({"type": request.form.get("type")})
            if request.form.get("instance")!=None:
                logging.debug("setNode->：instance=" + request.form.get("instance"))
                new_instance = instances.get_instance(id=request.form.get("instance"))[0]
                # 操作合理性检测（node原来的instance是否和新instance一致）
                if "instance" in node.get_label():  # 如果node的instance标签原先有值，那么还要修改这个instance的mentionList
                    old_instance = node.get_label()["instance"]
                    if old_instance == new_instance:
                        return jsonify("can not build a reference relation between cur node and cur instance, because is already existing.")
                if "instance" not in node.get_label():
                    node.add_label({"instance": new_instance})
                    new_instance["mention_list"].append([node])
                else:
                    # edit old instance
                    old_instance = node.get_label()["instance"]
                    mentionLists = old_instance["mention_list"]
                    for mentionList in mentionLists:
                        if node in mentionList:
                            mentionList.remove(node)
                    old_instance["mention_list"] = mentionLists
                    if request.form.get("instance")=="":
                        # edit node
                        node.del_label("instance")
                    else:
                        # edit new instance
                        new_instance = instances.get_instance(id=request.form.get("instance"))[0]
                        new_instance["mention_list"].append([node])
                        # edit node
                        node.add_label({"instance": new_instance})
            logging.debug("setNode<-：(success)")
            return jsonify("success")

    @app.route('/delNode', methods=["POST"])
    def delNode():
        pass

    @app.route('/addInstance', methods=["POST"])
    def addInstance():
        position = ntree.str_to_position(request.form.get("position"))
        if position:  # 使用快捷键，基于一个node创建instance
            node = ntree[position]
            logging.debug("addInstance_node->：position=" + str(position))
            instance = instances.add_instance(desc=node.text())
            instance["mention_list"].append([node])
            node.add_label({"instance": instance})
        else:  # 单纯创建一个instance
            logging.debug("addInstance_empty->：")
            instance = instances.add_instance()
        return jsonify(instance.labels.readable())

    @app.route('/getInstance', methods=["POST"])
    def getInstance():
        instance_id = request.form.get("instance_id")
        logging.debug("getInstance->：id=" + instance_id)
        target_instance = instances.get_instance(id=instance_id)[0]
        instance_info = target_instance.labels.readable()
        logging.debug("getInstance<-：(success)：" + str(instance_info))
        return jsonify(instance_info)

    @app.route('/setInstance', methods=["POST"])
    def setInstance():
        # 获取参数
        id = int(request.form.get("id"))
        desc = request.form.get("desc")
        kg = request.form.get("kg")
        mention_list_action = request.form.get("mention_list[action]")
        #
        instance = instances.get_instance(id=id)[0]
        logging.debug("setInstance->：id=" + str(id) + "：" + instance["desc"])
        #
        if desc:
            logging.debug("getInstance->：desc=" + desc)
            instance["desc"] = desc
        if kg:
            logging.debug("getInstance->：kg=" + kg)
            instance["kg"] = kg
        if mention_list_action:
            if mention_list_action == 'del mention':
                # edit instance
                mention_list_index = int(request.form.get('mention_list[mention_list_index]'))
                mention_index = int(request.form.get('mention_list[mention_index]'))
                deletedNode = instance["mention_list"][mention_list_index][mention_index]
                del instance["mention_list"][mention_list_index][mention_index]
                # if instance["mention_list"][mention_list_index] == []:  # 删除空mentionList
                #     if len(instance["mention_list"]) > 1:  # 如果空mentionList是最后一个mentionList，就不删
                #         del instance["mention_list"][mention_list_index]
                # edit node
                deletedNode.del_label("instance")
            elif mention_list_action == 'append mention':
                mention_list_index = int(request.form.get('mention_list[mention_list_index]'))
                cur_node_position = request.form.get('mention_list[new_node_position]')
                cur_node_position = ntree.str_to_position(cur_node_position)
                cur_node = ntree[cur_node_position]
                new_instance = instance
                # 操作合理性检测（node原来的instance是否和新instance一致）
                if "instance" in cur_node.get_label():  # 如果node的instance标签原先有值，那么还要修改这个instance的mentionList
                    old_instance = cur_node.get_label()["instance"]
                    if old_instance == new_instance:
                        return jsonify("can not build a reference relation between cur node and cur instance, because is already existing.")
                # edit new instance
                instance["mention_list"][mention_list_index].append(cur_node)
                # edit old instance
                if "instance" in cur_node.get_label():  # 如果node的instance标签原先有值，那么还要修改这个instance的mentionList
                    old_instance = cur_node.get_label()["instance"]
                    mentionLists = old_instance["mention_list"]
                    for mentionList in mentionLists:
                        if cur_node in mentionList:
                            mentionList.remove(cur_node)
                    old_instance["mention_list"] = mentionLists
                # edit node
                cur_node.add_label({'instance': instance})
            elif mention_list_action == 'del mentionList':
                mention_list_index = int(request.form.get('mention_list[mention_list_index]'))
                del instance["mention_list"][mention_list_index]
            elif mention_list_action == 'append mentionList':
                instance["mention_list"].append([])
        logging.debug("setInstance<-：(success)" )
        return jsonify("success")

    @app.route('/delInstance', methods=["POST"])
    def delInstance():
        instance_id = request.form.get("instance_id")
        logging.debug("delInstance->：id=" + instance_id)
        instance = instances.get_instance(id=instance_id)[0]
        del instances[int(instance_id)]

    @app.route('/save', methods=["POST"])
    def save():
        output_ntree_to_pickle(ntree)
        output_instances_to_pickle(instances)
        return jsonify({"success": True})

    app.run(debug=True)
    print("请在浏览器中打开http://127.0.0.1:5000/ ")

