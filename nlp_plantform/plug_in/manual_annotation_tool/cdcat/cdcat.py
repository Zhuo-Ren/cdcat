from flask import Flask, render_template, request, jsonify
from nlp_plantform.center.mytree import mytree
from nlp_plantform.center.instance import Instance
from typing import Dict, List, Tuple, Union  # for type hinting
import logging

def cdcat(root: mytree):
    app = Flask(__name__)

    @app.route('/')
    def init():
        return render_template("main.html", instance_dict=Instance.instance_dict)

    @app.route('/getText', methods=["POST"])
    def getText():
        text_node_position = request.form.get("textNodeId")
        text_unit_list = []
        if text_node_position == "":
            text_node_position = ()
        else:
            text_node_position = text_node_position.split("-")
            text_node_position = (int(i) for i in text_node_position)
        for cur_nleaf in root[text_node_position].all_nleaves():
            p = [str(i) for i in cur_nleaf.position()]
            text_unit_list.append({
                "char": cur_nleaf[0],
                "position": "-".join(p)
            })
        #
        logging.debug("getText->：position=" + str(text_node_position) + "：" + root[text_node_position].text())
        logging.debug("getText<-：" + "(success)" + "：" + str(text_unit_list))
        #
        return jsonify(text_unit_list)

    @app.route('/addNode', methods=["POST"])
    def addNode():
        selected_nleaf_list = request.form.getlist("childrenNodePositionList[]")
        selected_nleaf_list = [i.split("-") for i in selected_nleaf_list]
        selected_nleaf_list = [[int(j) for j in i] for i in selected_nleaf_list]
        logging.debug("addNode->：position=" + str(selected_nleaf_list[0]) + "-" + str(selected_nleaf_list[-1]))
        selected_nleaf_list = [root[i] for i in selected_nleaf_list]
        try:
            anno_node = mytree.add_parent({}, selected_nleaf_list)
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
        start_nleaf_position = request.form.get("start").split("-")
        start_nleaf_position = [int(i) for i in start_nleaf_position]
        end_nleaf_position = request.form.get("end").split("-")
        end_nleaf_position = [int(i) for i in end_nleaf_position]
        #
        anno_node = mytree.is_annotated(root, start_nleaf_position, end_nleaf_position)
        if anno_node is not None:
            anno_info = anno_node.label()
            anno_info["position"] = anno_node.position(output_type="string")
            #
            logging.debug(
                "getNode->：position=" +
                str(start_nleaf_position) + '-' + str(end_nleaf_position) +
                "：" + anno_node.text()
            )
            logging.debug("getNode<-：" + "(success)" + "：" + str(anno_info))
            #
            return jsonify(anno_info)
        else:
            #
            logging.debug("getNode->：position=" + str(start_nleaf_position) + '-' + str(end_nleaf_position))
            logging.debug("getNode<-：" + "(no node)" + "：")
            #
            return ""

    @app.route('/setNode', methods=["POST"])
    def setNode():
        position = request.form.get("position")
        if position == "":
            position = ()
        else:
            position = position.split("-")
            position = tuple(int(i) for i in position)
        node = root[position]
        logging.debug("setNode->：position=" + str(position) + "：" + node.text())
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
            old_instance = node.get_label()["instance"]
            new_instance = Instance.instance_dict[int(request.form.get("instance"))]
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
        output = Instance.getInstanceById(instance_id).output_to_dict()
        logging.debug("getInstance<-：(success)：" + str(output))
        return jsonify(output)

    @app.route('/setInstance', methods=["POST"])
    def setInstance():
        return ""

    app.run()
    print("请在浏览器中打开http://127.0.0.1:5000/ ")
