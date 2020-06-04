from flask import Flask, render_template, request, jsonify
from nlp_plantform.center.mytree import mytree

def cdcat(root: mytree):
    app = Flask(__name__)

    text_unit_list = []
    for cur_nleaf in root.all_nleaves():
        p = [str(i) for i in cur_nleaf.position()]
        text_unit_list.append({
            "char": cur_nleaf[0],
            "position": "-".join(p)
        })

    @app.route('/')
    def fun1():
        return render_template("main.html", text_unit_list=text_unit_list)

    @app.route('/selectChars', methods=["POST"])
    def selectChars():
        print(request.form)
        start_nleaf_position = request.form.get("start").split("-")
        start_nleaf_position = [int(i) for i in start_nleaf_position]
        end_nleaf_position = request.form.get("end").split("-")
        end_nleaf_position = [int(i) for i in end_nleaf_position]
        anno_node = mytree.is_annotated(root, start_nleaf_position, end_nleaf_position)
        if anno_node is not None:
            return jsonify({
                "path": "1-10-3-2",
                "entityType": "people",
                "token": True
            })
        else:
            return ""

    app.run()
    print("请在浏览器中打开http://127.0.0.1:5000/ ")
