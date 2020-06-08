from flask import Flask, render_template, request, jsonify
from nlp_plantform.center.mytree import mytree
from nlp_plantform.center.instance import Instance
from typing import Dict, List, Tuple, Union  # for type hinting

def cdcat(root: mytree):
    app = Flask(__name__)

    text_unit_list = []
    for cur_nleaf in root.all_nleaves():
        p = [str(i) for i in cur_nleaf.position()]
        text_unit_list.append({
            "char": cur_nleaf[0],
            "position": "-".join(p)
        })

    # instance_list["mention_position_list"] = [i.position() for i in instance_list["mention_list"]]

    @app.route('/')
    def fun1():
        return render_template("main.html",
                               text_unit_list=text_unit_list,
                               instance_dict=Instance.instance_dict)

    @app.route('/selectChars', methods=["POST"])
    def selectChars():
        print(request.form)
        start_nleaf_position = request.form.get("start").split("-")
        start_nleaf_position = [int(i) for i in start_nleaf_position]
        end_nleaf_position = request.form.get("end").split("-")
        end_nleaf_position = [int(i) for i in end_nleaf_position]
        anno_node = mytree.is_annotated(root, start_nleaf_position, end_nleaf_position)
        anno_info = anno_node.label()
        anno_info["position"] = "-".join(str(i) for i in anno_node.position())
        if anno_node is not None:
            return jsonify(anno_info)
        else:
            return ""

    @app.route('/getInstanceInfo', methods=["POST"])
    def getInstanceInfo():
        instance_id = request.form.get("instance_id")
        instance_id = int(instance_id)
        if instance_id != -1:
            return jsonify(Instance.instance_dict[instance_id])
        else:
            return ""

    app.run()
    print("请在浏览器中打开http://127.0.0.1:5000/ ")
