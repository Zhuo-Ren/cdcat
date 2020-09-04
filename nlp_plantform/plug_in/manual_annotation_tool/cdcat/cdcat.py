from flask import Flask, render_template, request, jsonify
from nlp_plantform.center.ntree import ntree
from nlp_plantform.center.instance import instance
from nlp_plantform.center.instances import instances
from typing import Dict, List, Tuple, Union  # for type hinting
import nlp_plantform.log_config
import logging

def cdcat(ntree: ntree, instances: instances, unit_level: Dict) -> None :
    """
    This is a manual annotation tool for cross-document coreference.

    :param ntree: nodes info in the form of *center.ntree*.
    :param instances: instances info in the form of *center.instances*.
    :param unit_level:
    """
    app = Flask(__name__)

    @app.route('/')
    def init():
        return render_template("main.html", instance_dict=instances)

    @app.route('/getText', methods=["POST"])
    def getText():
        """
        given the position of a target node. for each leaf node of the target node, return char and position.

        :AjaxIn textNodeId: tid of the node.
        :return: jsonify( [{"char": char of the 0th leaf node, "position": position of the 1th leaf node}, {...}, ...] )
        """
        text_node_position = request.form.get("textNodeId")
        text_node_position = ntree.str_to_position(text_node_position)
        text_unit_list = []
        for cur_nleaf in ntree[text_node_position].all_nleaves():
            p = [str(i) for i in cur_nleaf.position()]
            text_unit_list.append({
                "char": cur_nleaf[0],
                "position": "-".join(p)
            })
        #
        logging.debug("getText->：position=" + str(text_node_position) + "：" + ntree[text_node_position].text())
        logging.debug("getText<-：" + "(success)" + "：" + str(text_unit_list))
        #
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
        selected_nleaf_list = request.form.getlist("childrenNodePositionList[]")
        selected_nleaf_list = [i.split("-") for i in selected_nleaf_list]
        selected_nleaf_list = [[int(j) for j in i] for i in selected_nleaf_list]
        logging.debug("addNode->：position=" + str(selected_nleaf_list[0]) + "-" + str(selected_nleaf_list[-1]))
        selected_nleaf_list = [ntree[i] for i in selected_nleaf_list]
        try:
            anno_node = ntree.add_parent({}, selected_nleaf_list)
        except RuntimeError:
            logging.debug("addNode->：position=" + selected_nleaf_list[0] + "-" + selected_nleaf_list[-1])
            logging.debug("addNode<-：" + "(can not add node)" + "：")
            return ""
        if anno_node is not None:
            anno_info = anno_node.output_to_dict()
            logging.debug("addNode<-：" + "(success)" + "：" + str(anno_info))
            return jsonify(anno_info)

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
            anno_info = node.label()
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
            return ""
        elif isinstance(node, ntree):
            if request.form.get("token"):
                logging.debug("setNode->：token=" + request.form.get("token"))
                if request.form.get("token") == 'false':
                    del node.get_label()["token"]
                elif request.form.get("token") == 'true':
                    node.add_label({"token": True})
            if request.form.get("semanticType"):
                logging.debug("setNode->：semanticType=" + request.form.get("semanticType"))
                if request.form.get("semanticType") == 'none':
                    del node.get_label()["semanticType"]
                else:
                    node.add_label({"semanticType": request.form.get("semanticType")})
            if request.form.get("instance"):
                logging.debug("setNode->：instance=" + request.form.get("instance"))
                if "instance" not in node.get_label():
                    new_instance = Instance.getInstanceById(request.form.get("instance"))
                    node.add_label({"instance": new_instance})
                    new_instance["mention_list"].append([node])
                else:
                    old_instance = node.get_label()["instance"]
                    new_instance = Instance.getInstanceById(request.form.get("instance"))
                    node.add_label({"instance": new_instance})
                    new_instance["mention_list"].append([node])
                    old_instance["mention_list"].remove([node])
            output = node.output_to_dict()
            logging.debug("setNode<-：(success)" + str(output))
            return jsonify(output)

    @app.route('/getInstance', methods=["POST"])
    def getInstance():
        instance_id = request.form.get("instance_id")
        logging.debug("getInstance->：id=" + instance_id)
        output = instances.get_instance(id=instance_id)[0].output_to_dict()
        logging.debug("getInstance<-：(success)：" + str(output))
        return jsonify(output)

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
            # 扩展某个现有的mention_list
            if mention_list_action == 'extent':
                #
                mention_list_index = int(request.form.get('mention_list[mention_list_index]'))
                new_node_position = ntree.str_to_position(request.form.get('mention_list[new_node_position]'))
                #
                instance["mention_list"][mention_list_index].append(ntree[new_node_position])
            # 添加一个新的mention_list
            elif mention_list_action == 'add':
                instance["mention_list"].append([])

        output = instance.output_to_dict()
        logging.debug("getInstance<-：(success)" + str(output))
        return jsonify(output)

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
        return jsonify(instance.output_to_dict())

    app.run(debug=True)
    print("请在浏览器中打开http://127.0.0.1:5000/ ")

def statistic():
    r = {}

    return r
