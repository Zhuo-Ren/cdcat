// 全局变量。array of html elements。选中的文本所对应的元素的数组。
// var selectedElements = 0;
// var selectedIndex = undefined;
var svgNS = 'http://www.w3.org/2000/svg';
var SelectedElementIndexList  = undefined;
// var selectedElementsBefore= undefined;
var wrap_list=[];
var void_list=[];
var node_label_list=[];
var colorMap={};
//当前选中的节点，用于删除当点节点
var cur_Node=undefined;
var cur_Node_Z=0;
var new_Node_Z=0;
var color_index=0;


// 设置ajax不要异步执行
$.ajaxSetup({
    async : false
});

function PythonStyleToJsStyle(data){
    if (!(data instanceof Object)){
        alert(langDict("Data is not a js Object"))
    }
    for(let key in data){
        if (data[key] instanceof Object){
            data[key] = PythonStyleToJsStyle(data[key])
        }else{
            if (data[key] == null){
                data[key] = undefined
            }
        }
    }
    return data
}

// ui interface
{
    // catalogueWindow
    {
        /**
         *  In catalogueWindow, scroll to the given element.
         *
         */
        function catalogueWindow_scroll() {
        }

        /**
         * In catalogueWindow, set content based on *contentArray*.
         */
        function catalogueWindow_updateContent(contentArray) {
            //
            catalogueWindow = $("#catalogueWindow")
            catalogueWindow.empty();
            // 创建根目录
            var contentRoot = $("<ul></ul>");
            contentRoot.attr("id", "browser");
            contentRoot.addClass("filetree");
            catalogueWindow.append(contentRoot);

            // 添加目录到根目录
            /**
             * Add the content to a <ul> element.
             * @param parentUl The <ul> element.
             * @param contentArray content array.
             */
            function addContentElement(parentUl, contentArray) {
                flag1 = (typeof contentArray[0] == "string");
                flag2 = (typeof contentArray[1] == "string");
                isLeaf = (flag1 && flag2);
                // 添加当前节点
                curLi = $("<li></li>");
                parentUl.append(curLi);
                curSpan = $("<span></span>")
                curLi.append(curSpan);
                curSpan.attr("id", contentArray[0]);
                curSpan.css("white-space", "nowrap")
                positionString = contentArray[0];
                if (positionString === "") {
                    index = "root";
                } else {
                    positionList = positionString.split("-");
                    index = positionList[positionList.length - 1];
                }
                if (isLeaf) {
                    // 当前是叶子节点（文件）
                    curSpan.html(contentArray[1]);
                    curSpan.addClass("file");
                    // 为目录添加单击事件
                    curSpan.click(function () {
                        //加载文本与空节点空格
                        getText(
                            this.id,
                            function (returnData, status, requireData) {
                                majorTextWindow_setCurArticleNodePosition(requireData["textNodeId"]);
                                majorTextWindow_updateText(returnData);
                                majorTextWindow_show(returnData);
                            }
                        );
                         TextWindow_initNodes();
                        //再重新加载文本
                        getText(
                            this.id,
                            function (returnData, status, requireData) {
                                majorTextWindow_setCurArticleNodePosition(requireData["textNodeId"]);
                                majorTextWindow_updateText(returnData);
                                majorTextWindow_show(returnData);
                            }
                        );
                        //渲染svg（underline，curve，margin）
                        majorTextWindow_redrawSvg();

                    });
                } else {
                    // 当前是枝干节点（文件夹）
                    curSpan.html(index);
                    curSpan.addClass("folder");
                    let curUl = $("<ul></ul>");
                    curLi.append(curUl);

                    // 遍历直接孩子
                    for (let i = 1; i < contentArray.length; i++) {
                        addContentElement(curUl, contentArray[i]);
                    }
                }
            }

            addContentElement(contentRoot, contentArray);
            // 为目录添加样式
            $("#browser").treeview({
                toggle: function () {
                    console.log("%s was toggled.", $(this).find(">span").text());
                }
            });
            $("#add").click(function () {

                var branches = $("<li><span class='folder'>New Sublist</span><ul>" +
                    "<li><span class='file'>Item1</span></li>" +
                    "<li><span class='file'>Item2</span></li></ul></li>").appendTo("#browser");
                $("#browser").treeview({
                    add: branches
                });
            });
        }
    }

    // textWindow
    {
        /**
        Load the node list and void node list according to the nodepool, and
         initializethe newline node according to the head and tail positions of the node
         */
        function TextWindow_initNodes()
        {
            node_label_list=[];
            void_list=[];
            wrap_list=[];
            //获取所有node的id
            let node= getNodepool();
            //根据节点id长度排序，排列结果形如[1-2,3-4,1-2-3-4]
            node.sort(function(a,b){
                let a_len=a.split("-").length;
                let b_len=b.split("-").length;
                if(a_len!=b_len)
                    return a_len-b_len;
                else {
                    let a_num=parseInt(a.split("-")[a_len-1]);
                    let b_num=parseInt(b.split("-")[b_len-1]);
                    if(a_num!=b_num)
                        return a_num-b_num;
                    else
                    {
                        let node_a=a.split(":")[2];
                        let node_b=b.split(":")[2];
                        return parseInt(node_a.split("-")[0])-parseInt(node_b.split("-")[0])
                    }
                }
            });
            for(const k in node) {
                node_label_list.push(node[k]);
                let node_list=node[k];
                //判斷是否为空节点，类似于形式为9-9
                node_list=node_list.split(":");
                let node_id=node_list[node_list.length-1];
                let file_name=node_list[1];
                node_id=node_id.split("-");
                let node_id_head=node_id[0];
                let node_id_tail=node_id[node_id.length-1];
                if(node_id_head==node_id_tail)
                    void_list.push(file_name+":"+node_id_head);
            }
             //判断是否有换行节点
            for (const k in node_label_list) {
                let node_list = node_label_list[k];
                //
                node_list = node_list.split(":");
                let node_id = node_list[node_list.length - 1];
                let file_name = node_list[1];
                if (doc_id != file_name)
                    continue;
                node_id = node_id.split("-");
                if (node_id.length > 2)
                    continue;
                let node_id_head = node_id[0] + "-" + String(Number(node_id[0]) + 1);
                let node_id_tail = String(Number(node_id[node_id.length - 1]) - 1) + "-" + node_id[node_id.length - 1];
                if ($("#" + node_id_head).offset().top != $("#" + node_id_tail).offset().top) {
                    // console.log($("#"+node_id_head).offset().top,$("#"+node_id_tail).offset().top);
                    let new_line_id = file_name + ":" + String(Number(node_id[0]) - 1);
                    //判断是否是一个新的跨行节点
                    let id = 0;
                    while (id < wrap_list.length) {
                        if (wrap_list[id] == new_line_id)
                            break;
                        id++;
                    }
                    if (id == wrap_list.length)
                        wrap_list.push(file_name + ":" + String(Number(node_id[0]) - 1));
                    //当出现跨行节点时可能会影响后面的节点是否会跨行，所以要冲新加载文本
                    getText(
                    majorTextWindow_getCurArticleNodePosition(),
                    function (returnData, status, requireData) {
                        majorTextWindow_setCurArticleNodePosition(requireData["textNodeId"]);
                        majorTextWindow_updateText(returnData);
                        majorTextWindow_show(returnData);
                        }
                    );
                }
            }
        }

        /**
         * In majorTextWindow, user can select a range of chars. This function return a list of index of those chars.
         * @return {Array} ["index string of the 1th selected char", "index string of the 2th selected char", ...]
         */
        function majorTextWindow_getSelectedIndexFromGui() {
            // 如果没选中任何内容
            if (window.getSelection().toString() === "") {
                return undefined
            }
            // 如果选中了某些内容
            else {
                var selected = window.getSelection();
                var curRange = selected.getRangeAt(0);
                // 获取anchor
                var startDiv = curRange.startContainer.parentNode;
                if (startDiv.className.indexOf("ui-layout-content") !== -1) {
                    startDiv = startDiv.children[0].children[0]
                } else if (startDiv.className.indexOf("textTab") !== -1) {
                    startDiv = startDiv.childNodes[0]
                } else if (startDiv.className.indexOf("char") !== -1) {
                    //
                } else if (startDiv.id === "") {
                    startDiv = startDiv.parentNode;
                } else if (startDiv.id === undefined) {
                    startDiv = startDiv.parentNode.parentNode
                } else {
                    alert(langDict["Error: can not get Anchor of the selected area."]);
                }
                // 获取curve
                var endDiv = curRange.endContainer.parentNode;
                if (endDiv.className.indexOf("ui-layout-content") !== -1) {
                    endDiv = endDiv.children[0].children[0]
                } else if (endDiv.className.indexOf("textTab") !== -1) {
                    endDiv = endDiv.childNodes[0]
                } else if (endDiv.className.indexOf("char") !== -1) {
                    //
                } else if (endDiv.id === "") {
                    endDiv = endDiv.parentNode;
                } else if (endDiv.id === undefined) {
                    endDiv = endDiv.parentNode.parentNode
                } else {
                    alert(langDict["Error: can not get Curve of the selected area."]);
                }

                // 识别anchor和curve的顺序，得到start和end
                function idCompare(a, b) {
                    a = a.split('-').map(Number)
                    b = b.split('-').map(Number)
                    var r = 0;
                    for (var i = 0; i < Math.min(a.length, b.length); i++) {
                        if (a[i] != b[i]) {
                            r = (a[i] > b[i]);
                            break;
                        }
                    }
                    if ((r == 0) && (a.length == b.length)) {
                        r = false
                    }
                }

                if (idCompare(startDiv.id, endDiv.id)) {
                    t = endDiv;
                    endDiv = startDiv;
                    startDiv = t;
                }
                // 遍历选区，得到element列表
                let selectedElements = new Array(0);
                var selectedText = "";
                var curDiv = startDiv;
                while (true) {
                    selectedElements.push(curDiv);
                    selectedText = selectedText + curDiv.childNodes[0].textContent;
                    if (curDiv !== endDiv) {
                        curDiv = curDiv.nextElementSibling;
                    } else {
                        break;
                    }
                }
                // 解决start和end的空选问题
                s = selected.toString().replace(/[\n\r]/g, "")
                if (s[0] !== selectedText[0]) {
                    selectedElements.shift();
                    selectedText = selectedText.slice(1, selectedText.length);
                }
                if (s[s.length - 1] !== selectedText[selectedText.length - 1]) {
                    selectedElements.pop();
                    selectedText = selectedText.slice(0, selectedText.length - 1);
                }
                // translate selectedElements to SelectedElementIndexList.
                // It is because after the reloading of majorTextWindow, the elements in selectedElements are disabled.
                let selectedElementIndexList = [];
                for (i = 0; i < selectedElements.length; i++) {
                    curElement = selectedElements[i];
                    index = $(curElement.parentElement).children().index(curElement);
                    selectedElementIndexList.push(index);
                }
                return selectedElementIndexList
            }
        }

        /**
         * Given a list of indexs, this function return a list of jquery.HtmlElements corresponding to the indexs. This
         * function will not check whether the given index belong to current article. So, the global variable that records
         * the selected index should be cleaned when changing the article.
         * @param {Array} selectedElementIndexList:["0-0-1", "0-0-2", ...]
         * @return {Array} A list of jquery.HtmlElements corresponding to the given indexs.
         */
        function majorTextWindow_getSelectedElementFromIndex(selectedElementIndexList) {
            let selectedElementList = [];
            for (var i = 0; i < selectedElementIndexList.length; i++) {
                let curElement = $("#textTab1").children()[selectedElementIndexList[i]];
                selectedElementList.push($(curElement));
            }
            return selectedElementList
        }

        /**
             * Given a list of jquery.HtmlElement in majorTextWindow, this function highlights them.
             * This function will not check whether the given elements really belong to majorTextWindow. The elements will be
             * highlighted as long as they are existing. This function is used to add effects when adding nodes
         *
         * @param elementList
         */
        function majorTextWindow_hightlightElement(elementList) {
            for (var i = 0; i < elementList.length; i++) {
                // console.log(elementList[i][0]);
                elementList[i][0].style = "color:rgb(255,255,255);background-color:red; opacity:0.4";
            }
        }

         /**
          * Update colour_tree when init And update colorMap by instance pool
         */
        function add_color_list()
        {
            //颜色映射
            color_tree=[];
            //颜色映射计算过程列表
            color_list = [];
            //当前所要选取的color_tree id
            // color_index=0;
            let len = 255;
            //采用二分法在rgb颜色空间均匀选取颜色
            let right = 255;
            let left = 0;
            let pi=Math.PI;
            let pi_1_3 = Math.PI / 3;
            let pi_2_3 = Math.PI * 2 / 3;
            let mid = parseInt((left + right) / 2);
            color_list.push(left);
            color_list.push(mid);
            color_list.push(right);
            let t=(0.5 - mid/255) * pi;
            // let t=(mid/255) * pi;
            let x=undefined;
            color_tree.push("rgb("+parseInt(255 * (x = Math.sin(t)) * x)+','
                               +parseInt(255 * (x = Math.sin(t + pi_1_3)) * x)+','
                               +parseInt(255 * (x = Math.sin(t + pi_2_3)) * x)+')');

            let i = 1;
            while (i < len) {
                let list_len=color_list.length - 1
                for (let j = 0; j < list_len; j++) {
                    let m=parseInt((color_list[j]+color_list[j+1])/2);
                    color_list.push(m);
                    t=(0.5 - m/255) * pi;
                    // t=(m/255) * pi;
                    color_tree.push("rgb("+parseInt(255 * (x = Math.sin(t)) * x)+','
                               +parseInt(255 * (x = Math.sin(t + pi_1_3)) * x)+','
                               +parseInt(255 * (x = Math.sin(t + pi_2_3)) * x)+')');
                    i++;
                    if(i>len)
                        break;
                }
                color_list.sort(function (a, b) {
                        return a-b;
                        });
            }
            //初始化colormap
            let ip_list=getInstancepool();
            for(const k in ip_list)
            {
                colorMap[ip_list[k]]=color_tree[color_index++];
                color_index=color_index%255;
            }
        }
        /**
         Draw a line between two div elements with the given id
         @param {z} ["int"] Underline hierarchy
         */
        function addunderline(a,b,id,color,z=0)
        {
            if(a[0]!='#')
                a="#"+a;
            if(b[0]!='#')
                b="#"+b;
            z=parseInt(z);
            let file_id = $("#textTab1").attr("name");
            let node_id="n:"+file_id+":"+id.split("_")[0];

            let svg = $(document.createElementNS(svgNS, 'svg'));
            let path = $(document.createElementNS(svgNS, 'path'));
            let a_x=parseInt($(a).offset().left);
            let a_y=parseInt($(a).offset().top + $(a).height());
            let b_x = parseInt($(b).offset().left+$(b).width());
            let b_y = parseInt($(b).offset().top + $(b).height());
            if(parseInt(a_y) != parseInt(b_y))
                return;
            let x = Math.min(a_x, b_x)-$(textTab1).offset().left+11;
            let y = Math.min(a_y, b_y)-$(textTab1).offset().top+8;
            let width = Math.abs(a_x-b_x)-1;
            let height = 4;
            let d=undefined;
            if(width<4)
                d = "M 0 2 "+"L "+String(parseInt(width))+" "+String(2);
            else
                d = "M 1 2 "+"L "+String(parseInt(width)-2)+" "+String(2);

            // d = "M 0 "+String(8)+" "+"L 10 8";
            path.attr("d", d);
            path.attr("stroke-width", "2");
            path.attr("fill", "none");
            path.attr("id", id);
            // path.attr("stroke", color);
            // svg.attr("class",doc_id);
            svg.attr("id", id);
            // svg.attr("stroke-width", "3");
            svg.attr("stroke", color);
            svg.attr("z",z);
            svg.attr("fill", "none");
            svg.click(function () {
                let slotNum = $(".slot").length;
                if (slotNum == 0) {
                    // 重新加载文本
                    getText(
                        majorTextWindow_getCurArticleNodePosition(),
                        function (returnData, status, requireData) {
                            majorTextWindow_setCurArticleNodePosition(requireData["textNodeId"]);
                            majorTextWindow_updateText(returnData, 0);
                            majorTextWindow_show(returnData);
                        }
                    );
                    nodeInfoWindow_showSvgNode(node_id);
                    // majorTextWindow_redrawSvg();
                    changeSVGcolor(id, "red");
                    cur_Node = node_id;
                    cur_Node_Z = z;
                }
            })
            svg.css("position", "absolute")
            svg.css("top", y+z*6);
            svg.css("left", x);
            svg.css("height", height);
            svg.css("width", width);
            svg.css("z-index", 150);
            svg.append(path);
            $(textTab1).append(svg);
        }
        /**
            Set the svg element with the specified id to the specified stroke
          @param: id:选中svg的id
          @param: color
         */
        function changeSVGcolor(id,color) {
            if (id[0] != "#")
                id = "#" + id;
            $(id).attr("stroke", color);
        }
        /**
            Set the svg element with the specified id to the specified stroke
           @param: elementList
         */
        function majorTextWindow_addunderline(elementList){
            // elementList[i][0].style = "text-decoration: underline;text-decoration-color: red";
            //处理换行节点
            if(elementList[0].offset().top != elementList[elementList.length-1].offset().top)
            {
                let selectedElementID=elementList[0].attr("id");
                selectedElementID = selectedElementID.split('-')[1];
                // console.log(selectedElementID);
                selectedElementID=Number(selectedElementID)-2;

                wrap_list.push(doc_id+":"+String(selectedElementID));
                getText(
                    majorTextWindow_getCurArticleNodePosition(),
                    function (returnData, status, requireData) {
                        majorTextWindow_setCurArticleNodePosition(requireData["textNodeId"]);
                        majorTextWindow_updateText(returnData);
                        majorTextWindow_show(returnData);
                        }
                    );
                majorTextWindow_redrawSvg();
                for(const k in SelectedElementIndexList)
                    {
                        SelectedElementIndexList[k]=SelectedElementIndexList[k]+2;
                    }
                    let selectedElement1 = majorTextWindow_getSelectedElementFromIndex(SelectedElementIndexList);
                    majorTextWindow_hightlightElement(selectedElement1);
            }
            //处理重合节点
            let node_z=0;
            let cur_head=elementList[0].attr("id").split("-")[0];
            let cur_tail=elementList[elementList.length-1].attr("id").split("-")[1];
            let nodeID=cur_head+"-"+cur_tail;
            let node_list=node_label_list;
            for(const k in node_list)
            {
                let file_id=node_list[k].split(":")[1];
                if(doc_id!=file_id)
                    continue;
                let node_pre=node_list[k].split(":")[0]+":"+node_list[k].split(":")[1]+":";
                let created_node=node_list[k].split(":")[2];
                created_node=created_node.split("-");
                if(created_node.length>2)
                    continue;
                let created_node_head=created_node[0];
                let created_node_tail=created_node[1];
                //如果要添加的节点包含已有的节点
                if(created_node_head==cur_head && created_node_tail==cur_tail)
                    continue;
                if((parseInt(created_node_head)>=parseInt(cur_head) && parseInt(created_node_tail)<=parseInt(cur_tail))
                || (parseInt(created_node_head)<=parseInt(cur_head) && parseInt(created_node_tail)>=parseInt(cur_head)))
                {

                    if($("#"+created_node_head+"-"+created_node_tail+"_1").length!=0)
                        node_z=2;
                    else
                        node_z=1;
                }
                if((parseInt(created_node_head)<=parseInt(cur_head) && parseInt(created_node_tail)>=parseInt(cur_tail))
                    || (parseInt(created_node_head)<=parseInt(cur_tail) && parseInt(created_node_tail)>=parseInt(cur_tail)))
                {
                    //  let r=getNodeById(node_pre+node_list[k].split(":")[2]);
                    // if(r[0]=="success")
                    // {
                    //     delNode(r[1]["id"]);
                    // }
                    //  if(node_list[k].match(nodeID)!=null) {
                    //     for (const id in node_label_list) {
                    //         delNode(node_list[k]);
                    //     }
                    // }
                    // majorTextWindow_redrawSvg();
                }
            }
            let svgid=elementList[0].attr("id").split("-")[0]+"-"+elementList[elementList.length-1].attr("id").split("-")[1];
            if (document.getElementById(svgid + "_0") === null){
                addunderline(elementList[0].attr("id"),elementList[elementList.length-1].attr("id"),svgid+"_0","black",node_z);
            }

        }

         /**
            Return the node z-index according to the node overlap relationship
          @param {} nodeID
          @return {z} ["int"]
         */
        function get_node_z(nodeID)
        {
            let z=0;
            let node_pre=nodeID.split(":")[0]+":"+nodeID.split(":")[1]+":";
            //node_list为node_label_list副本
            let node_list=node_label_list;
            nodeID=nodeID.split(":")[2];
            let cur_head=nodeID.split("-")[0];
            let cur_tail=nodeID.split("-")[1];
            if(cur_head == cur_head)
            {
                return 0;
            }
            for(const k in node_list)
            {
                let file_id=node_list[k].split(":")[1];
                if(doc_id!=file_id)
                    continue;
                let created_node=node_list[k].split(":")[2];
                created_node=created_node.split("-");
                if(created_node.length>2)
                    continue;
                let created_node_head=created_node[0];
                let created_node_tail=created_node[1];
                //如果要添加的节点包含已有的节点
                if(created_node_head == cur_head && created_node_tail == cur_tail)
                {
                    continue;
                }
                //如果k是空节点
                if(created_node_head == created_node_tail)
                {
                    continue;
                }
                //如果要添加的节点包含已有的节点
                if((parseInt(created_node_head)<=parseInt(cur_head) && parseInt(created_node_tail)>=parseInt(cur_tail))
                    || (parseInt(created_node_head)<=parseInt(cur_tail) && parseInt(created_node_tail)>=parseInt(cur_tail)))
                {
                    //  let r=getNodeById(node_pre+node_list[k].split(":")[2]);
                    // if(r[0]=="success")
                    // {
                    //     let refers=r[1]["refer"];
                    //     for(const d in refers)
                    //     {
                    //         // console.log(node_pre+nodeID+"-"+refers[d].split(":")[2])
                    //         let test=delNode(node_pre+node_list[k].split(":")[2]+"-"+refers[d].split(":")[2])
                    //
                    //         TextWindow_initNodes();
                    //     }
                    // }
                    // if(node_list[k].match(nodeID)!=null) {
                    //     for (const id in node_label_list) {
                    //         delNode(node_list[k]);
                    //     }
                    // }
                    continue;
                }
                //如果与前面的节点重合
                if((parseInt(created_node_head)>=parseInt(cur_head) && parseInt(created_node_tail)-1<=parseInt(cur_tail)-1))
                {
                    // console.log(cur_head,cur_tail,created_node_head,created_node_tail);
                    if($("#"+created_node_head+"-"+created_node_tail+"_1").length!=0)
                        z=2;
                    else
                        z=1;
                   continue;

                }
                if(parseInt(created_node_head)<=parseInt(cur_head) && parseInt(created_node_tail)-1>=parseInt(cur_head))
                {

                    let pre_z=get_node_z(node_list[k]);
                    if(pre_z==0){
                        if($("#"+created_node_head+"-"+created_node_tail+"_1").length!=0)
                            z=2;
                        else
                            z=1;
                       continue;
                    }else {
                        z=0;
                    }
                }
            }

            return parseInt(z);
        }
        /**
            Given a list of jquery.HtmlElement in majorTextWindow, this function setting borders for void nodes
         @param elementList
         */
        function majorTextWindow_addmargin(elementList){
            // for (var i = 0; i < elementList.length; i++) {
            //     elementList[i][0].style = "border: 1px solid black";
            //
            // }
            let svgid = "#" + elementList[0].attr("id");
            let svg = $(document.createElementNS(svgNS, 'svg'));
            let path = $(document.createElementNS(svgNS, 'path'));
            let x = $(svgid).offset().left - $(textTab1).offset().left + 10;
            let y = $(svgid).offset().top - $(textTab1).offset().top + 10;
            let width = 8;
            let height = 18;
            // d = "M 0 0 L 0 10 L 8 10 L 8 0 L 0 0";
            d = "M 0 0 L 0 17 L 6 17 L 6 0 L 0 0";
            path.attr("d", d);
            // path.attr("stroke", color);
            path.attr("stroke-width", "1");
            path.attr("fill", "none");

            svg.attr("id", elementList[0].attr("id")+"_0");
            // svg.attr("class",doc_id);
            svg.attr("stroke", "black");
            svg.css("position", "absolute")
            svg.css("top", y+2);
            svg.css("left", x);
            svg.css("height", height);
            svg.css("width", width);
            svg.css("z-index", 148);
            svg.append(path);
            $(textTab1).append(svg);
        }

        function changeColor(evt) {
            var rect = evt.target;
            rect.setAttributeNS(null, "stroke", "yellow");
        }
        /**
            Setting curve for nodes
         @param div_a:div元素。for example：#1-2
         @param a_z: 0 or 1。for example:node1与另一个节点有重叠时，则为1
         @param node1:id靠前的节点id。for example: n:doc:14-20,
         */
        function addCurve(div_a, div_b, id, color,a_z=0,b_z=0,node1=" ",node2=" "){

            let node_list1=node1.split("-");
            let node_list2=node2.split("-");
            let node1_len=node_list1.length;
            let node2_len=node_list2.length;
            // console.log(node1,node2,id);
            if(div_a[0]!='#')
                div_a="#"+div_a;
            if(div_b[0]!='#')
                div_b="#"+div_b;
            a_z=parseInt(a_z);
            b_z=parseInt(b_z);
            //添加curve_node
            let file_id = $("#textTab1").attr("name");
            let have=0;
            let node_id="n:"+file_id+":"+id;
            for(const k in node_label_list) {
                if (node_id == node_label_list[k])
                    have = 1;
            }
            if(have==0) {
                //当前节点id的形式必须为1-2-3-4的数字递增形式
                // console.log(id, file_id,node1,node2,a_z,b_z);
                let r = addNodeByCurve(id, file_id,node1,node2,a_z,b_z);
                node_id = r[1]["id"];
                node_label_list.push(node_id);

            }

            let svg = $(document.createElementNS(svgNS, 'svg'));
            let path = $(document.createElementNS(svgNS, 'path'));
            //计算a,b相对于textTab1的偏移坐标
            let a_x = $(div_a).offset().left-$(textTab1).offset().left+12;
            let a_y = $(div_a).offset().top + $(div_a).height()-$(textTab1).offset().top+8;
            let b_x = $(div_b).offset().left-$(textTab1).offset().left+12;
            let b_y = $(div_b).offset().top + $(div_b).height()-$(textTab1).offset().top+8;

            //如若是curve node则起点或终点更改为曲线中点
            if(node1_len>2)
            {
                let curve=$("#"+node1);
                a_x=parseInt(Number(curve.attr("mid_x"))+0.5);
                a_y=parseInt(Number(curve.attr("mid_y"))+0.5);
            }
             if(node2_len>2)
            {
                let curve=$("#"+node2);
                b_x=parseInt(Number(curve.attr("mid_x"))+0.5);
                b_y=parseInt(Number(curve.attr("mid_y"))+0.5);
            }

            //计算svg的位置相关属性
            let x = Math.min(a_x, b_x);
            let y = Math.min(a_y, b_y);

            //width+3与后面的下划线连接
            let width = Math.abs(a_x-b_x)+3;
            let height = Math.abs(a_y-b_y);

            //贝塞尔曲线控制点，svg位置的相对坐标
            let control_x = undefined;
            let control_y = undefined;
            if(height==0) {
                if(width>24) {
                    control_x = width / 2;
                    control_y = height + 24;
                }else {
                    control_x = width / 2;
                    control_y = height + 14;
                }
            }
            else
            {
                //当a在b的左下角
                if((a_x<b_x && a_y>b_y)||(a_x>b_x && a_y<b_y)){
                    let mid_x = width / 2;
                    let mid_y = height / 2;
                    let arc = Math.atan(height / width);
                    let l = parseInt(Math.pow(Math.pow(width, 2) + Math.pow(height, 2), 0.5));
                    let h = 0.25*l;
                    control_x = mid_x + h * Math.sin(arc);
                    control_y = mid_y + h * Math.cos(arc);
                }
                else {
                    let mid_x = width / 2;
                    let mid_y = height / 2;
                    let arc = Math.atan(height / width);
                    let l = parseInt(Math.pow(Math.pow(width, 2) + Math.pow(height, 2), 0.5));
                    let h = 0.25*l;
                    control_x = mid_x - h * Math.sin(arc);
                    control_y = mid_y + h * Math.cos(arc);
                }
            }
            //path是带一个控制点的贝塞尔曲线，计算t=0.5时的点作为曲线中点
            //转化为绝对坐标
            let svg_mid_x=x+control_x;
            let svg_mid_y=y+control_y;

            //a与控制点的中点
            let a_svgmid_mid_x=(a_x+svg_mid_x)/2;
            let a_svgmid_mid_y=(a_y+a_z+svg_mid_y)/2;

            //b与控制点的中点
            let b_svgmid_mid_x=(b_x+svg_mid_x)/2;
            let b_svgmid_mid_y=(b_y+b_z+svg_mid_y)/2;

            //path中点
            let path_mid_x=(a_svgmid_mid_x+b_svgmid_mid_x)/2;
            let path_mid_y=(a_svgmid_mid_y+b_svgmid_mid_y)/2;
            let d= undefined;

            //如果a的位置在b的左下角或b在a的左下角
            // if(a_x<b_x)//当a在b的左下角
            if((a_x<b_x && a_y>b_y)||(a_x>b_x && a_y<b_y)) {
                let temp=a_z;
                a_z=b_z;
                b_z=temp;

                // d = "M " + "0 " + String(height + a_z * 7) + " Q " + String(width / 2) + " " + String(height + 24) + " " + String(width) + " " + String( b_z * 7);
                if (control_x>width)
                {
                     d = "M 0 " + String(height + a_z * 7) + " Q " + String(control_x) + " " + String(control_y) + " " + String(width) + " " + String( b_z * 7);
                     width=control_x;
                }else {
                    d = "M 0 " + String(height + a_z * 7) + " Q " + String(control_x) + " " + String(control_y) + " " + String(width) + " " + String(b_z * 7);
                }
            }
            else {
                // d = "M 0 " + String(a_z * 7) + " Q " + String(width / 2) + " " + String(height + 24) + " " + String(width) + " " + String(height + b_z * 7);
                if(control_x<0)
                {
                     d = "M " +  String(-control_x)+" "+ String(a_z * 7) + " Q " + "0" + " " + String(control_y) + " " + String(width-control_x) + " " + String(height + b_z * 7);
                     x = x +control_x;
                     width=width-control_x;
                }
                else {

                    d = "M 0 " + String(a_z * 7) + " Q " + String(control_x) + " " + String(control_y) + " " + String(width) + " " + String(height + b_z * 7);
                }
            }//

            path.attr("d", d);
            path.attr("stroke-width", "2");
            path.attr("visibility","visible");
            path.attr("fill", "none");
            path.click(function ()
            {
                 let slotNum = $(".slot").length;
                 if (slotNum == 0) {
                     // 重新加载文本
                     getText(
                         majorTextWindow_getCurArticleNodePosition(),
                         function (returnData, status, requireData) {
                             majorTextWindow_setCurArticleNodePosition(requireData["textNodeId"]);
                             majorTextWindow_updateText(returnData, 0);
                             majorTextWindow_show(returnData);
                         }
                     );
                     nodeInfoWindow_showSvgNode(node_id);
                     // majorTextWindow_redrawSvg();
                     //点击curve颜色改为红色
                     changeSVGcolor(id, "red");
                     cur_Node = node_id;
                     cur_Node_Z=0;
                 }
            });
            svg.attr("stroke", color);
            svg.attr("id", id);
            svg.attr("class",doc_id);
            svg.attr("mid_x",path_mid_x);
            svg.attr("mid_y",path_mid_y);

            //抗锯齿
            // svg.css("shape-rendering","optimizeSpeed")
            svg.css("shape-rendering","geometricPrecision")
            // 当svg中的某个元素可见，并且当其fill 不是none 时，指针在fill区域，该事件能够被捕捉到，当其 troke不是none时，stroke目标事件能够被捕捉到，visibility为hidden事件不可捕获。
            svg.css("pointer-events","visiblePainted")
            svg.css("visibility","hidden");
            svg.css("position", "absolute")
            //y+1与下划线连接
            svg.css("top", y+1);
            svg.css("left", x);
            //根据控制点位置决定svg高度
            if (control_y>height)
                svg.css("height", control_y+Math.abs(a_z*6-b_z*6));
            else
                svg.css("height", height+Math.abs(a_z*6-b_z*6));
            svg.css("width", width+4);
            //
            svg.css("z-index", 148);
            svg.append(path);
            $(textTab1).append(svg);
        }
        /**
         According to the curve node ID returns the head node and tail node of the curve
         @param nodeID
         @return {array} [from_node,to_node]
         */
        function get_from_node_to_node(nodeID)
        {
            nodeID = nodeID.split(":");
            let node_pre=nodeID[0]+":"+nodeID[1]+":";
            nodeID = nodeID[nodeID.length - 1];
            nodeID = nodeID.split("-");
            let nodeID_len=nodeID.length;
            let from_node="";
            let to_node="";
            let node_list=[];
            //获取普通节点的头尾div
            if(nodeID_len<=2) {
               return node_list;
            }
            //curve节点的头尾div
            else if(nodeID_len==4){
                 from_node=nodeID[0]+"-"+nodeID[1];
                 to_node=nodeID[2]+"-"+nodeID[3];
            }
            //获取连接curve节点与普通节点的curve头尾div与头尾id
             else if(nodeID_len==6){
                //通过遍历节点列表找到头尾节点
                let temp_curve_node_id="";
                for(let i=0;i<4;i++)
                {
                    temp_curve_node_id=temp_curve_node_id+nodeID[i];
                    if(i<3)
                        temp_curve_node_id=temp_curve_node_id+"-";
                }
                for(let i=0;i<node_label_list.length;i++)
                {
                    if(temp_curve_node_id==node_label_list[i].split(":")[2]) {
                        from_node = temp_curve_node_id;
                        to_node=nodeID[4]+"-"+nodeID[5];
                    }
                }
                if(from_node.search("-")==-1)
                {
                     from_node = nodeID[0]+"-"+nodeID[1];
                     to_node=nodeID[2]+"-"+nodeID[3]+"-"+nodeID[4]+"-"+nodeID[5];
                }
            }
             //
             else if(nodeID_len==8){
                let temp_curve_node_id1="";
                let temp_curve_node_id2="";
                for(let i=0;i<6;i++)
                {
                    temp_curve_node_id1=temp_curve_node_id1+nodeID[i];
                    temp_curve_node_id2=temp_curve_node_id2+nodeID[i+2];
                    if(i<5) {
                        temp_curve_node_id1 = temp_curve_node_id1 + "-";
                        temp_curve_node_id2 = temp_curve_node_id2 + "-";
                    }
                }
                for(let i=0;i<node_label_list.length;i++)
                {
                    if(temp_curve_node_id1==node_label_list[i].split(":")[2]) {
                        from_node = temp_curve_node_id1;
                        to_node=nodeID[6]+"-"+nodeID[7];
                    }
                    if(temp_curve_node_id2==node_label_list[i].split(":")[2]) {
                        from_node = nodeID[0]+"-"+nodeID[1];
                        to_node=temp_curve_node_id2;
                    }
                }
                if(from_node.search("-")==-1 && to_node.search("-")==-1)
                {
                    from_node = nodeID[0]+"-"+nodeID[1]+"-"+nodeID[2]+"-"+nodeID[3];
                    to_node = nodeID[4]+"-"+nodeID[5]+"-"+nodeID[6]+"-"+nodeID[7];
                }
            }else {
                let temp_curve_node_id1 = "";
                let temp_curve_node_id2 = "";
                for(let i=0;i<nodeID.length-2;i++)
                {
                    temp_curve_node_id1=temp_curve_node_id1+nodeID[i];
                    temp_curve_node_id2=temp_curve_node_id2+nodeID[i+2];
                    if(i<nodeID.length-3) {
                        temp_curve_node_id1 = temp_curve_node_id1 + "-";
                        temp_curve_node_id2 = temp_curve_node_id2 + "-";
                    }
                }
                for(let i=0;i<node_label_list.length;i++)
                {
                    if(temp_curve_node_id1==node_label_list[i].split(":")[2]) {
                        from_node = temp_curve_node_id1;
                        to_node=nodeID[nodeID.length-2]+"-"+nodeID[nodeID.length-1];
                    }
                    if(temp_curve_node_id2==node_label_list[i].split(":")[2]) {
                        from_node = nodeID[0]+"-"+nodeID[1];
                        to_node=temp_curve_node_id2;
                    }
                }
            }
             let r=getNodeById(node_pre+from_node);
             if(r[0] =="success")
             {
                 let refers = r[1]["refer"];
                 if(refers!==undefined || refers!==null) {
                     for (let cur_id = 0; cur_id < refers.length; cur_id++) {
                         let newID = refers[cur_id];
                         if (newID[0] == "i") {
                             continue;
                         }
                         newID = newID.split(":");
                         newID = newID[newID.length - 1];
                         if (newID == to_node) {
                             node_list.push(node_pre + from_node);
                             node_list.push(node_pre + to_node);
                         }
                     }
                 }
             }
             r=getNodeById(node_pre+to_node);
             if(r[0] =="success") {
                 let refers = r[1]["refer"];
                 for (let cur_id = 0; cur_id < refers.length; cur_id++) {
                     let newID = refers[cur_id];
                     if (newID[0] == "i") {
                         continue;
                     }
                     newID = newID.split(":");
                     newID = newID[newID.length - 1];
                     if (newID == from_node) {
                         node_list.push(node_pre + to_node);
                         node_list.push(node_pre + from_node);
                     }
                 }
             }
             return node_list;
        }
        /**
          For one node draw svg
           @param nodeInfo： A node info dict.
           @param {int} nodeupdate： 0 or 1, 如是在redraw_svg中调用为0，还如是在update_refer中调用为1
         */
        function majorTextWindow_updateRefer(nodeInfo, nodeupdate = 0) {
            // get the label data ready
            let newValue = nodeInfo["refer"];
            let refer_tos = [];
            let nodeID = nodeInfo["id"];
            nodeID = nodeID.split(":");
            nodeID = nodeID[nodeID.length - 1];
            let cursvgID = nodeID;

            nodeID = nodeID.split("-");
            let nodeID_len = nodeID.length;
            //对于普通node,curID_head是当前选中node节点的第一个div元素的name
            //对于普通node,curID_tail是当前选中node节点的最后一个div元素的name
            let curID_head = nodeID[0];
            let curID_tail = nodeID[1];
            //节点的头div,用于后面处理节点间关系是确定头部
            let svg_id_head;
            //curve node的头尾node_id
            let from_node = "";
            let to_node = "";
            //对于curve node的前后node:a,b的z,如果前后节点a或b为curve,则z为0
            let a_z = 0;
            let b_z = 0;
            //对于普通node的下划线的z,如果覆盖了前面的节点，则node_z为1或2
            let node_z = 0;
            //获取普通节点的头尾div
            if (nodeID_len <= 2) {
                node_z = get_node_z(nodeInfo["id"]);
                node_z = parseInt(node_z);
                if (curID_head == curID_tail) {
                    curID_head = curID_head + "-" + curID_tail;
                    curID_tail = curID_head;
                    svg_id_head = Number(nodeID[0]);
                } else {
                    curID_head = Number(curID_head);
                    svg_id_head = curID_head;
                    curID_head = String(curID_head) + "-" + String(curID_head + 1);
                    curID_tail = Number(curID_tail);
                    curID_tail = String(curID_tail - 1) + "-" + String(curID_tail);
                }
            }
            //curve节点的头尾div
            else if (nodeID_len == 4) {
                //curve node的头node头div为curID_head
                //curve node的尾node头div为curID_tail
                curID_tail = nodeID[nodeID.length - 2];

                from_node = nodeID[0] + "-" + nodeID[1];
                to_node = nodeID[2] + "-" + nodeID[3];

                a_z = parseInt(nodeInfo["token_id"].split(",")[0]);
                b_z = parseInt(nodeInfo["token_id"].split(",")[1]);
                //考虑空节点
                if (nodeID[0] == nodeID[1]) {
                    curID_head = nodeID[0] + "-" + nodeID[1];
                    svg_id_head = Number(nodeID[0]);
                } else {
                    curID_head = Number(curID_head);
                    svg_id_head = curID_head;
                    curID_head = String(curID_head) + "-" + String(curID_head + 1);
                }
                if (nodeID[2] == nodeID[3]) {
                    curID_tail = nodeID[2] + "-" + nodeID[3];
                } else {
                    curID_tail = Number(curID_tail);
                    curID_tail = String(curID_tail) + "-" + String(curID_tail + 1);
                }
            }
            //获取连接curve节点与普通节点的curve头尾div与头尾id
            else if (nodeID_len == 6) {
                //curID_head，curID_tail是curve头尾节点的div
                //通过遍历节点列表找到头尾节点
                let temp_curve_node_id = "";
                for (let i = 0; i < 4; i++) {
                    temp_curve_node_id = temp_curve_node_id + nodeID[i];
                    if (i < 3)
                        temp_curve_node_id = temp_curve_node_id + "-";
                }
                for (let i = 0; i < node_label_list.length; i++) {
                    if (temp_curve_node_id == node_label_list[i].split(":")[2]) {
                        from_node = temp_curve_node_id;
                        to_node = nodeID[4] + "-" + nodeID[5];
                        b_z = parseInt(nodeInfo["token_id"].split(",")[1]);
                    }
                }
                if (from_node.search("-") == -1) {
                    from_node = nodeID[0] + "-" + nodeID[1];
                    a_z = parseInt(nodeInfo["token_id"].split(",")[0]);
                    to_node = nodeID[2] + "-" + nodeID[3] + "-" + nodeID[4] + "-" + nodeID[5];
                }
                //curve node的头node头div为curID_head
                //curve node的尾node头div为curID_tail
                curID_tail = to_node.split("-")[0];
                // 考虑空节点
                if (nodeID[0] == nodeID[1]) {
                    curID_head = nodeID[0] + "-" + nodeID[1];
                    svg_id_head = Number(nodeID[0]);
                } else {
                    curID_head = Number(curID_head);
                    svg_id_head = curID_head;
                    curID_head = String(curID_head) + "-" + String(curID_head + 1);
                }
                if (to_node.split("-")[0] == to_node.split("-")[1]) {
                    curID_tail = to_node.split("-")[0] + "-" + to_node.split("-")[1];
                } else {
                    curID_tail = Number(curID_tail);
                    curID_tail = String(curID_tail) + "-" + String(curID_tail + 1);
                }
            }
            //
            else if (nodeID_len == 8) {
                //curID_head，curID_tail是curve头尾节点的div
                let temp_curve_node_id1 = "";
                let temp_curve_node_id2 = "";
                for (let i = 0; i < 6; i++) {
                    temp_curve_node_id1 = temp_curve_node_id1 + nodeID[i];
                    temp_curve_node_id2 = temp_curve_node_id2 + nodeID[i + 2];
                    if (i < 5) {
                        temp_curve_node_id1 = temp_curve_node_id1 + "-";
                        temp_curve_node_id2 = temp_curve_node_id2 + "-";
                    }
                }
                for (let i = 0; i < node_label_list.length; i++) {
                    if (temp_curve_node_id1 == node_label_list[i].split(":")[2]) {
                        from_node = temp_curve_node_id1;
                        to_node = nodeID[6] + "-" + nodeID[7];
                        b_z = parseInt(nodeInfo["token_id"].split(",")[1]);
                    }
                    if (temp_curve_node_id2 == node_label_list[i].split(":")[2]) {
                        from_node = nodeID[0] + "-" + nodeID[1];
                        a_z = parseInt(nodeInfo["token_id"].split(",")[0]);
                        to_node = temp_curve_node_id2;
                    }
                }
                if (from_node.search("-") == -1 && to_node.search("-") == -1) {
                    from_node = nodeID[0] + "-" + nodeID[1] + "-" + nodeID[2] + "-" + nodeID[3];
                    to_node = nodeID[4] + "-" + nodeID[5] + "-" + nodeID[6] + "-" + nodeID[7];
                }
                //curve node的头node头div为curID_head
                //curve node的尾node头div为curID_tail
                curID_tail = to_node.split("-")[0];
                // 考虑空节点
                if (nodeID[0] == nodeID[1]) {
                    curID_head = nodeID[0] + "-" + nodeID[1];
                    svg_id_head = Number(nodeID[0]);
                } else {
                    curID_head = Number(curID_head);
                    svg_id_head = curID_head;
                    curID_head = String(curID_head) + "-" + String(curID_head + 1);
                }
                if (to_node.split("-")[0] == to_node.split("-")[1]) {
                    curID_tail = to_node.split("-")[0] + "-" + to_node.split("-")[1];
                } else {
                    curID_tail = Number(curID_tail);
                    curID_tail = String(curID_tail) + "-" + String(curID_tail + 1);
                }
            } else {
                let temp_curve_node_id1 = "";
                let temp_curve_node_id2 = "";
                for (let i = 0; i < nodeID.length - 2; i++) {
                    temp_curve_node_id1 = temp_curve_node_id1 + nodeID[i];
                    temp_curve_node_id2 = temp_curve_node_id2 + nodeID[i + 2];
                    if (i < nodeID.length - 3) {
                        temp_curve_node_id1 = temp_curve_node_id1 + "-";
                        temp_curve_node_id2 = temp_curve_node_id2 + "-";
                    }
                }
                for (let i = 0; i < node_label_list.length; i++) {
                    if (temp_curve_node_id1 == node_label_list[i].split(":")[2]) {
                        from_node = temp_curve_node_id1;
                        to_node = nodeID[nodeID.length - 2] + "-" + nodeID[nodeID.length - 1];
                    }
                    if (temp_curve_node_id2 == node_label_list[i].split(":")[2]) {
                        from_node = nodeID[0] + "-" + nodeID[1];
                        to_node = temp_curve_node_id2;
                    }
                }
                curID_tail = to_node.split("-")[0];
                // 考虑空节点
                if (nodeID[0] == nodeID[1]) {
                    curID_head = nodeID[0] + "-" + nodeID[1];
                    svg_id_head = Number(nodeID[0]);
                } else {
                    curID_head = Number(curID_head);
                    svg_id_head = curID_head;
                    curID_head = String(curID_head) + "-" + String(curID_head + 1);
                }
                if (to_node.split("-")[0] == to_node.split("-")[1]) {
                    curID_tail = to_node.split("-")[0] + "-" + to_node.split("-")[1];
                } else {
                    curID_tail = Number(curID_tail);
                    curID_tail = String(curID_tail) + "-" + String(curID_tail + 1);
                }
            }
            //接下来先处理refer的节点，在处理有refer的节点
            //对于无refer节点
            if (newValue.length === 0) {
                //对于普通节点
                if (nodeID_len <= 2) {
                    if (document.getElementById(cursvgID + "_0") === null && nodeID[0] != nodeID[1]) {
                        addunderline(curID_head, curID_tail, cursvgID + "_0", "black", node_z);
                    }
                }
                //对于curve节点
                else {
                    if (document.getElementById(cursvgID) != null) {
                        $("#" + cursvgID).remove();
                    }
                    addCurve(curID_head, curID_tail, cursvgID, "black", a_z, b_z, from_node, to_node);
                }
            }
            //对于refer节点
            else {
                let instance_sum = 0;
                for (let cur_now_id = 0; cur_now_id < newValue.length; cur_now_id++) {
                    let newID = newValue[cur_now_id];
                    if (newID[0] == "i") {
                        //颜色映射
                        // <script src="http://d3js.org/d3.v5.min.js"></script>
                        //color = d3.scaleDiverging(d3.interpolateRainbow)//设置颜色函数，将rgb值根据节点数目进行映射
                        //         .domain([0, nodes.length - 1])
                        refer_tos.push(newID);
                        if (!colorMap.hasOwnProperty(newID)) {
                            //随机颜色分配
                            // let r = parseInt(Math.random() * 255);
                            // let g = parseInt(Math.random() * 255);
                            // let b = parseInt(Math.random() * 255);
                            // let curcolor = "rgb(" + String(r) + "," + String(g) + "," + String(b) + ")";
                            let curcolor = color_tree[color_index++];
                            color_index = color_index % 255;
                            colorMap[newID] = curcolor;
                        }
                        // changeSVGcolor(cursvgID + "_0", colorMap[refer_to]);
                        //如果节点下划线不存在，则添加，否则设置其为实例应有的颜色
                        instance_sum = instance_sum + 1;
                    }
                }
                //如果该node没有指向instance
                if (refer_tos.length == 0) {
                    //如果是普通节点
                    if (nodeID_len <= 2 && nodeID[0] != nodeID[1]) {
                        if (document.getElementById(cursvgID + "_" + 0) === null)
                            addunderline(curID_head, curID_tail, cursvgID + "_0", "black", node_z);
                    }
                    //如果是曲线节点
                    if (nodeID_len > 2) {
                        if (document.getElementById(cursvgID) != null) {
                            $("#" + cursvgID).remove();
                        }
                        addCurve(curID_head, curID_tail, cursvgID, "black", a_z, b_z, from_node, to_node);
                    }
                }
                //如果node指向了instance,修改其颜色
                for (const k in refer_tos) {
                    let refer_to = refer_tos[k];
                    if (nodeID_len <= 2 && nodeID[0] != nodeID[1]) {
                        if (colorMap.hasOwnProperty(refer_to)) {
                            if (document.getElementById(cursvgID + "_" + k) === null)
                                addunderline(curID_head, curID_tail, cursvgID + "_" + k, colorMap[refer_to], node_z + parseInt(k));
                            else
                                changeSVGcolor(cursvgID + "_" + k, colorMap[refer_to]);
                        } else {
                            if (document.getElementById(cursvgID + "_" + k) === null)
                                addunderline(curID_head, curID_tail, cursvgID + "_" + k, "black", node_z + parseInt(k));
                        }
                    } else if (nodeID_len <= 2 && nodeID[0] == nodeID[1]) {
                        if (document.getElementById(cursvgID + "_" + k) != null)
                            changeSVGcolor(cursvgID + "_" + k, colorMap[refer_to]);
                    }
                    //如果是曲线节点
                    else {
                        if (document.getElementById(cursvgID) != null)
                            $("#" + cursvgID).remove();
                        if (colorMap.hasOwnProperty(refer_to)) {
                            addCurve(curID_head, curID_tail, cursvgID, colorMap[refer_to], a_z, b_z, from_node, to_node);
                        } else {
                            addCurve(curID_head, curID_tail, cursvgID, "black", a_z, b_z, from_node, to_node);
                        }
                    }
                }

                //在标注时执行，因为全局变量cur_node_z只对当前节点有效，在初始化运行时不执行,
                //处理节点间curve关系
                //先暂存这几个变量，因为在循环中可能改变
                let [temp_a, temp_b, temp_c, temp_d] = [cursvgID, cur_Node_Z, curID_head, node_z];
                for (let cur_now_id = 0; cur_now_id < newValue.length; cur_now_id++) {
                    [cursvgID, cur_Node_Z, curID_head, node_z] = [temp_a, temp_b, temp_c, temp_d];
                    let newID = newValue[cur_now_id];
                    if (newID[0] == "i") {
                        continue;
                    }
                    let new_node_z = 0;
                    new_node_z = get_node_z(newID);
                    newID = newID.split(":");
                    newID = newID[newID.length - 1];
                    let newsvgID = newID;
                    newID = newID.split("-");
                    let newID_len = newID.length;
                    //newID是当前节点指向的节点
                    let newID_head = newID[0];
                    let newID_tail = newID[1];
                    let svg_id_tail = Number(newID[0]);
                    if (newID_head == newID_tail) {
                        newID_head = newID_head + "-" + newID_head;
                    } else {
                        newID_head = Number(newID_head);
                        // svg_id_tail = newID_head;
                        newID_head = String(newID_head) + "-" + String(newID_head + 1);
                        newID_tail = Number(newID_tail);
                        newID_tail = String(newID_tail - 1) + "-" + String(newID_tail);
                    }

                    //添加节点间连线
                    //svg_id为curve的id
                    let svg_id;
                    // console.log(svg_id_head , svg_id_tail);
                    if (svg_id_head > svg_id_tail) {
                        [cursvgID, newsvgID] = [newsvgID, cursvgID];
                        [cur_Node_Z, new_Node_Z] = [new_Node_Z, cur_Node_Z];
                        [curID_head, newID_head] = [newID_head, curID_head];
                        [node_z, new_node_z] = [new_node_z, node_z];
                    }
                    svg_id = cursvgID + "-" + newsvgID;
                    //将curve设置为何curid相同的颜色
                    // if (colorMap.hasOwnProperty(refer_to)) {
                    //     if (document.getElementById(svg_id) === null)
                    //         addCurve(curID_head, newID_head, svg_id, colorMap[refer_to], a_z, b_z);
                    //     else
                    //         changeSVGcolor(svg_id, colorMap[refer_to]);
                    // } else {
                    //     if (document.getElementById(svg_id) === null)
                    //         addCurve(curID_head, newID_head, svg_id, "black", a_z, b_z);
                    // }
                    if (nodeupdate == 1) {
                        //如果指向自己
                        if (newID_head == curID_head) {
                            // if (document.getElementById(newsvgID + "_1") != null)
                            //     addunderline(curID_head, curID_tail, cursvgID + "_1", "black", 1);
                            //
                            //  addCurve(curID_head, newID_head, svg_id, "black", 0, 1, cursvgID, newsvgID);
                        } else {
                            if (document.getElementById(svg_id) === null) {
                                // console.log(nodeInfo["id"], newValue);
                                // $("#"+svg_id).remove();
                                addCurve(curID_head, newID_head, svg_id, "black", cur_Node_Z, new_Node_Z, cursvgID, newsvgID);
                            }
                        }
                        // for (const k in refer_tos) {
                        //     let refer_to = refer_tos[k];
                        // if (nodeID_len <= 2) {
                        //     //如果节点下划线不存在，则添加，否则设置其为实例应有的颜色
                        //     if (colorMap.hasOwnProperty(refer_to)) {
                        //         if (document.getElementById(cursvgID + "_0") === null)
                        //             addunderline(curID_head, curID_tail, cursvgID + "_0", colorMap[refer_to]);
                        //         else
                        //             changeSVGcolor(cursvgID + "_0", colorMap[refer_to]);
                        //     } else {
                        //         if (document.getElementById(cursvgID + "_0") === null)
                        //             addunderline(curID_head, curID_tail, cursvgID + "_0", "black");
                        //     }
                        // }

                        //如果指向节点下划线不存在，则添加，否则设置其为实例应有的颜色
                        // if (newID_len<= 2) {
                        //     if (colorMap.hasOwnProperty(refer_to)) {
                        //         if (document.getElementById(newsvgID + "_0") === null)
                        //             addunderline(newID_head, newID_tail, newsvgID + "_0", colorMap[refer_to]);
                        //         else
                        //             changeSVGcolor(newsvgID + "_0", colorMap[refer_to]);
                        //     } else {
                        //         if (document.getElementById(newsvgID + "_0") === null)
                        //             addunderline(newID_head, newID_tail, newsvgID + "_0", "black");
                        //     }
                        // }

                        // }
                    } else {
                        //如果指向自己
                        if (newID_head == curID_head) {
                            // if (document.getElementById(newsvgID + "_1") != null)
                            //     addunderline(curID_head, curID_tail, cursvgID + "_1", "black", 1);
                            //
                            //  addCurve(curID_head, newID_head, svg_id, "black", 0, 1, cursvgID, newsvgID);
                        } else {
                            if (document.getElementById(svg_id) === null) {
                                // $("#"+svg_id).remove();
                                if (a_z < node_z)
                                    a_z = node_z + a_z;
                                if (b_z < new_node_z)
                                    b_z = new_node_z + b_z;
                                addCurve(curID_head, newID_head, svg_id, "black", a_z, b_z, cursvgID, newsvgID);
                            }
                        }
                    }
                }
            }
        }

        /**
         * If majorTextWindow shows the chars of a nodeu, the name of majorTextWindow is the position of this node. If
         * majorTextWindow shows nothing, the name of majorTextWindow is "notext". This function set the name of
         * majorTextWindow (the position of node whose string is going to be shown in majorTextWindow).
         *
         * @param {string} curNodePosition: the position of the node that is going to be shown in majorTextWindow.
         */
        function majorTextWindow_setCurArticleNodePosition(curNodePosition) {
            let majorTextWindow = $("#textTab1");
            majorTextWindow.attr("name", curNodePosition);
        }

        /**
         * If majorTextWindow shows the chars of a node, the name of majorTextWindow is the position of this node. If
         * majorTextWindow shows nothing, the name of majorTextWindow is "notext". This function get the name of
         * majorTextWindow (the position of node whose string is shown in majorTextWindow).
         *
         * @returns {string}
         */
        function majorTextWindow_getCurArticleNodePosition() {
            let majorTextWindow = $("#textTab1");
            return majorTextWindow.attr("name");
        }
        /**
        * Load the svg of each node
         */
        function majorTextWindow_redrawSvg()
        {
            $("svg").remove();
            //为空节点添加边框
            for (let id = 0; id < void_list.length; id++) {
                let Element = [];
                let id_list=void_list[id].split(':');

                let file_id=id_list[0];
                let ElementPosition = id_list[1];

                if(doc_id!=file_id)
                    continue;
                Element.push($("#" + ElementPosition + "-" + ElementPosition));
                majorTextWindow_addmargin(Element);
                // majorTextWindow_addunderline(Element);
            }
            // 对每个节点画下划线或曲线
            for (let id = 0; id < node_label_list.length; id++) {
                 // let id_name=node_label_list[id].split(":")[1].split(".")[0].replace("/","-");
                 let file_id=node_label_list[id].split(":")[1];

                 if(doc_id!=file_id)
                     continue;
                 let r = getNodeById(node_label_list[id]);
                 let nodeInfo=r[1];
                 majorTextWindow_updateRefer(nodeInfo);
             }
        }
         /**
         *
         * @param data The Array of every chair
         * @param scroll
         */
        function majorTextWindow_updateText(data,scroll=0) {
            doc_id=$("#textTab1").attr("name");
            // doc_id=doc_id.replace("/","-");
            // doc_id=doc_id.split('.')[0];

            let majorTextWindow = $("#textTab1");
            majorTextWindow.empty();
            // add html element for each char.
            for (let i = 0; i < data.length; i++) {
                let elementText = "";

                if (data[i]["char"] != " " && data[i]["char"] != "'") {
                    elementText += "<div " +
                        "id=" + data[i]["id"] +
                        " " +
                        "desc=" + data[i]["char"] +
                        " " +
                        "class='char'" +
                        ">";
                }
                if (data[i]["char"] == "'") {
                    elementText += "<div " +
                        "id=" + data[i]["id"] +
                        " " +
                        "desc=" + "`" +
                        " " +
                        "class='char'" +
                        ">";
                }
                if (data[i]["char"] === " ") {
                    elementText += "<div " +
                        "id=" + data[i]["id"] +
                        " " +
                        "desc=' '"
                        +
                        "class='char'" +
                        ">";
                    elementText += "<div>&nbsp</div>";
                }
                if (data[i]["char"] === "\n") {
                    elementText += "<div>\n</div> ";
                    elementText += "</div>";
                    elementText += "<br style='clear:both;'>";
                } else if (data[i]["char"] === "\r") {
                    elementText += "<div>\\r</div>";
                    elementText += "</div>";
                    elementText += "<br style='clear:both;'>";
                } else {
                    elementText += "<div>" + data[i]["char"] + "</div>";
                    elementText += "</div>";
                }
                //对跨行节点，在节点前添加换行
                for(let id=0;id<wrap_list.length;id++)
                {
                    if (doc_id+":"+String(i) == wrap_list[id]) {

                        elementText += "<div>\n</div> ";
                        elementText += "</div>";
                        elementText += "<br style='clear:both;'>";
                    }
                }
                //对空节点添加空格
                for(let id=0;id<void_list.length;id++)
                {
                    if (doc_id+":"+String(i+1) == void_list[id]) {
                        let voidID= i+1;
                        voidID=String(voidID)+"-"+String(voidID);
                        elementText += "<div " +
                        "id=" + voidID +
                        " " +
                        "desc=' '"
                        +
                        "class='char'" +
                        ">";
                        elementText += "<div>&nbsp&nbsp</div>";
                    }
                }
                let charElement = $(elementText);
                //
                majorTextWindow.append(charElement);

            }
        }

        function majorTextWindow_show() {
            $("#ui-id-1").click();
        }

        function minorTextWindow_updateText(data, scroll) {

        }

        function minorTextWindow_show() {
            $("#ui-id-2").click();
        }
    }

    // nodeInfoWindow
    {
        function nodeInfoWindow_showNoSelect() {
            $("#nodeInfo-noSelect").css("display", "block");
            $("#nodeInfo-noNode").css("display", "none");
            $("#nodeInfo-selectedNode").css("display", "none");
        }

        function nodeInfoWindow_showNoNode() {
            $("#nodeInfo-noSelect").css("display", "none");
                $("#nodeInfo-noNode").css("display", "block");
            $("#nodeInfo-selectedNode").css("display", "none");
        }

        function nodeInfoWindow_showNodeInfo() {
            $("#nodeInfo-noSelect").css("display", "none");
            $("#nodeInfo-noNode").css("display", "none");
            $("#nodeInfo-selectedNode").css("display", "block");
        }

        function nodeInfoWindow_addLabels() {
            // add labels
            for (let curLabelIndex = 0; curLabelIndex < labelSysDict["node"].length; curLabelIndex++) {
                let curLabelDict = labelSysDict["node"][curLabelIndex];
                //generate label obj
                let curLabelObj = labelTemplate[curLabelDict["value_type"]]["generateLabelObj_func"](curLabelDict);
                $("#nodeInfo-selectedNode").append(curLabelObj);
            }
        }

        //获取curve node的text，形式为Hello⊕world
        function get_curve_node_text(curItem) {
            let nodeID = curItem["id"].split(":");
            let node_id_pre = "";
            let Text="";
            for (let noed_id_compoment = 0; noed_id_compoment < [nodeID.length - 1]; noed_id_compoment++) {
                node_id_pre = node_id_pre + nodeID[noed_id_compoment] + ":";
            }
            nodeID = nodeID[nodeID.length - 1];
            let node_element_list = nodeID.split("-");
            //如果是普通节点
            if (node_element_list.length <= 2)
                Text = curItem["text"];
            //如果是普通curve node
            else {
                //inputText为组成curve的node的text
                let curve_node_text = "";
                for (let node_element = 0; node_element < node_element_list.length; node_element += 2) {
                    let node = node_id_pre + node_element_list[node_element] + "-" + node_element_list[node_element + 1];
                    let temp_text = "";
                    // console.log(node);
                    let r = getNodeById(node);
                    if (r[0] == "success") {
                        temp_text = r[1]["text"];
                    }
                    if (node_element < node_element_list.length - 2)
                        curve_node_text = curve_node_text + temp_text + "⊕";
                    else
                        curve_node_text = curve_node_text + temp_text;
                }
                Text=curve_node_text;
            }
            return Text;
        }

        function nodeInfoWindow_showCannotAddNode() {
            alert(langDict["can not add node based on current mention."])
        }

        /**
         * This function update the info in nodeInfoWindow.
         *and redraw svg and update this node's curve node
         * @param nodeInfo: A node info dict. Each item is a property or a label.
         *   The disappear of a label in the dict means annotators never label the label.
         *   Also,{"label_key": undefined} means annotators never label the label.
         */
        function nodeInfoWindow_updateNodeInfo(nodeInfo) {

            majorTextWindow_updateRefer(nodeInfo,1);
            majorTextWindow_redrawSvg();
            if(nodeInfo["id"].split("-").length>2)
            {
                nodeInfo["text"]="curve node";
                nodeInfo["token_id"]="0";
            }
            for (let curLabelIndex = 0; curLabelIndex < labelSysDict["node"].length; curLabelIndex++) {
                // get the label data ready
                let curLabelConfig = labelSysDict["node"][curLabelIndex];
                let newValue = undefined;
                if (curLabelConfig["key"] in nodeInfo) {
                    newValue = nodeInfo[curLabelConfig["key"]];
                }
                // generate a new label obj based on new value
                let curLabelTypeDict = labelTemplate[curLabelConfig["value_type"]];
                let labelObj = curLabelTypeDict["generateLabelObj_func"](curLabelConfig, newValue);
                // replace the old label obj
                $("#nodeInfo-selectedNode div[name='labelInfo-" + curLabelConfig["key"] + "']").replaceWith(labelObj);
            }


        }

        function nodeInfoWindow_refresh() {
            if ($("#nodeInfo-selectedNode").css("display") == "block") {
                // prepare ajax data
                let nodeId = $("#idValue").text();
                // ajax to background
                let r = getNodeById(nodeId);
                // display the new node info in GUI
                if (r[0] != "success") {
                    nodeInfoWindow_showNoNode();
                } else {
                    let nodeInfo = r[1];
                    nodeInfoWindow_updateNodeInfo(nodeInfo);
                }
            }
        }
        /**
         displaying node information when clicking svg.
         */
        function nodeInfoWindow_showSvgNode(svg_id)
        {
            // let file_id=$("#textTab1").attr("name");
            let r=getNodeById(svg_id);
            // 区分是否为标注对象
            if (r[0] != "success") {
                nodeInfoWindow_showCannotAddNode();
                alert(langDict[r[1]])
            } else {
                let newNodeInfo = r[1]
                // 更新标注信息
                // if(svg_id.split("-").length>2)
                nodeInfoWindow_updateNodeInfo(newNodeInfo);
                // 显示标注信息
                nodeInfoWindow_showNodeInfo();

            }
        }
    }

    // instanceSelectWindow
    {
        function instanceSelectWindow_showInstancePool() {
            let r = getGroup();
            if (r[0] != "success") {
                alert(langDict["instance pool loading failed"]);
                return
            }
            // 生成新dom元素
            let groupTupleOfInstancePool = r[1];
            let instancePoolObj = generateGroup(groupTupleOfInstancePool);
            // 添加新dom元素
            $("#allInstanceDiv").append(instancePoolObj);
            // 向jquery UI sortable 注册新dom元素
            $(".group").sortable({
                connectWith: ".group",
                start: sortStartFunction,
                stop: sortEndFunction
            }).disableSelection();
            $(".instances").sortable({
                connectWith: ".instances",
                start: sortStartFunction,
                stop: sortEndFunction
            }).disableSelection();
        }

        /**
         * 如果data指定的instance已经存在，那么更新；如果不存在，那么创建新instancelink
         * @param data
         */
        function instanceSelectWindow_updateOneInstance(data) {
            let targetElement = $(".instance[name='" + data["id"] + "']");
            // create a new instancelink
            if (targetElement.length == 0) {
                let liObj = generateInstancelink(data)
                let fixedObj = $("#allInstanceDiv ul").children(":first").children(":first").children(":first"); // 默认新instancelink都是添加到第一个fixed instances中去。
                fixedObj.prepend(liObj);
            }
            // update a existing instancelink
            else {
                targetElement.text(data["desc"]);
            }
            // // 删除旧节点Elemn
            // instanceSelectWindow_delOneInstanceObj(data);
            // // 创建新节点
            // let newInstanceObj = instanceSelectWindow_createOneInstanceObj(data);
            // // 添加新节点
            // $("#allInstanceDiv").prepend(newInstanceObj);
        }

        /**
         * delate one instance。
         * @param {Object} data: {"id"}
         */
        function instanceSelectWindow_delOneInstanceObj(data) {
            let oldInstanceObj = $("#allInstanceDiv [name=" + data['id'].toString() + "]")
            if (oldInstanceObj.length > 0) {
                oldInstanceObj.remove();
            }
        }

        /**
         * This function return a index list from *#allInstanceDiv* to *curLi*
         *
         * @param {jquery DOM element} curLi: li element in allInstanceDiv.
         * @return {[]} a index list that comes from *#allInstanceDiv* to *curLi*
         */
        function getLiPath(curLi) {
            // param check
            if (!((curLi.hasClass("group_li")) || (curLi.hasClass("instances_li")))) {
                alert("参数类型错误");
            }
            //
            let curPath = [];
            while (true) {
                let curUl = curLi.parent();
                let curIndex = curUl.children().index(curLi);
                curPath = [curIndex, ...curPath];
                // 检查退出
                if (curUl.parent().attr("id") == "allInstanceDiv") {
                    return curPath;
                }
                // ++
                if (curLi.hasClass("group_li")) {
                    curLi = curUl.parent();
                } else if (curLi.hasClass("instances_li")) {
                    curLi = curUl.parent().parent();
                }
            }
        }

        function sortStartFunction(e, ui) {
            window.sPath = getLiPath(ui["helper"]);
        }

        function sortEndFunction(e, ui) {
            window.ePath = getLiPath(ui["item"]);
            if (window.sPath.toString() !== window.ePath.toString()) {
                console.log(window.sPath, "-", window.ePath);
                moveLi(window.sPath, window.ePath);
            }
        }

        function generateInstancelink(curInstancelink) {
            // build DOC element
            let liObj = $("<li class='instances_li'></li>");
            // add attr
            liObj.attr('name', curInstancelink['id']);
            liObj.addClass('instance');
            if (curInstancelink['desc'] !== undefined) {
                if (curInstancelink['desc'] !== "") {
                    liObj.text(curInstancelink['desc']);
                } else {
                    liObj.text('　');
                }
            } else {
                liObj.text('　');
            }


            // shift拖拉：复制元素
            liObj.mousedown(function (e) {
                if (e.shiftKey) {
                    // ajax to background
                    let parentPath = getLiPath($(this));
                    let r = copyInstance(parentPath);
                    if (r[0] != "success") {
                        alert(langDict[r[1]]);
                        return
                    }
                    // update fontground
                    let newObj = $(this).clone(true);
                    $(this).after(newObj);
                }
            });
            // 左键
            liObj.click(function (e) {
                let slotObj = $(".slot");
                // 防止点击事件冒泡到父元素
                e.stopPropagation();
                // 如果是单纯点击
                if ((slotObj.length == 0) && (!e.altKey)) {
                    let instanceIdStr = $(this).attr("name");
                    let r = getInstanceById(instanceIdStr);
                    if (r[0] != "success") {
                        alert(langDict[r[1]]);
                    } else {
                        let instanceInfo = r[1]
                        instanceInfoWindow_updateInstanceInfo(instanceInfo);
                        instanceInfoWindow_showInstanceInfo();
                        instanceSelectWindow_updateOneInstance(instanceInfo);
                    }
                }
                // 如果是Alt点击：删除实例
                else if ((slotObj.length == 0) && (e.altKey)) {
                    if ($("li[name=" + curInstancelink["id"] + "]").length == 1) {
                        alert(langDict["Can not delete this instance button, because this is the last button of this instance. You must use the delKey in instanceInfoWindow to delete a instance."]);
                    } else {
                        // ajax to background
                        let parentPath = getLiPath($(this));
                        let r = delLi(parentPath);
                        if (r[0] != "success") {
                            alert(langDict[r[1]]);
                            return
                        }
                        // update fontground
                        $(this).remove();
                    }
                }
                // 如果是槽填充
                else if (slotObj.length == 1) {
                    let instanceIdStr = $(this).attr("name");
                    slotObj[0].fillSlot(instanceIdStr);
                }
                // 如果都不是，那有毛病
                else {
                    alert(langDict["A wrong num of slots."])
                }
            });
            return liObj
        }

        function generateInstances(instancesTuple){
            let instancesType = instancesTuple[0];
            let instancesName = instancesTuple[1];
            let instancesInfo = instancesTuple[2];
            // param check
            if (instancesType != "instances") {
                alert("error");
                return
            }
            let div = $("<div></div>");
            let ulObj = $("<ul class='instances'></ul>");
            div.append(ulObj);
            for (let curInstanceIndex = 0; curInstanceIndex < instancesInfo.length; curInstanceIndex++) {
                let curInstancelink = instancesInfo[curInstanceIndex];
                ulObj.append(generateInstancelink(curInstancelink));
            }
            return div;
        }

        /**
         * This function generate DOM element for group.
         * The group has a title only when the group has a name. The title includes a group name span and two "+" button.
         * The group has a ul element which corresponding to the content of the group.
         * @example::
         * groupTulple = ["group", "GName", [
         ["instances", "EName", [
         instance_pool.add_instance(),
         instance_pool.add_instance()
         ]],
         ["instances", "EName", [
         instance_pool.add_instance()
         ]],
         ["group", "GName", [
         ["instances", "EName", [
         instance_pool.add_instance(),
         instance_pool.add_instance()
         ]]
         ]]
         ]]
         *
         * @param {Array} groupTuple: A array with 3 items: type, name, info.
         * @return {Array<jqueryDomElement>} return [ul] when *instancesName* == undefined; [group name span, add group button, add instances button, ul] otherwise.
         */
        function generateGroup(groupTuple) {
            let groupType = groupTuple[0];
            let groupName = groupTuple[1];
            let groupInfo = groupTuple[2];
            //一开始groupinfo 是一个array（2），分别是["instances","Ename",array(xxx)]\[""group","Gname","array(xxx)"]
            // param check
            if (groupType !== "group") {
                alert("出错了");
                return
            }
            //
            let r = [];
            // group title
            if (groupName !== null) {
                // span
                {
                    let curGroupItemKeyObj = $("<span>" + groupName + "</span>");
                    curGroupItemKeyObj.click(function () {
                        let inputObj = $("<input type='text'>");
                        inputObj.attr("value", $(this).text());
                        $(this).after(inputObj);
                        $(this).remove();
                        inputObj.change(function () {
                            let newGroupName = $(this).val();
                            // ajax to background
                            let groupPath = getLiPath($(this).parent());
                            let r = changeGroupName(groupPath, newGroupName);
                            // update fontground
                            let spanObj = $("<span></span>");
                            spanObj.text(newGroupName);
                            $(this).after(spanObj);
                            $(this).remove();
                        });
                    });
                    r.push(curGroupItemKeyObj);
                }
                // add group button
                {
                    let addGroupButtonObj = $("<button style='background: #c5c5c5'>+</button>");
                    addGroupButtonObj.click(function () {
                        // ajax to background
                        let thisPath = getLiPath($(this).parent());
                        let r = prependGroup(thisPath);
                        if (r[0] !== "success") {
                            alert(langDict(r[1]));
                            return;
                        }
                        // update fontground
                        let liObj = $("<li class='group_li'></li>");
                        liObj.append(generateGroup(["group", "GName", []]));
                        $(this).next().next().prepend(liObj);
                        $(".group").sortable({
                            connectWith: ".group"
                        }).disableSelection();
                        $(".instances").sortable({
                            connectWith: ".instances"
                        }).disableSelection();
                    });
                    r.push(addGroupButtonObj);
                }
                // add items button
                {
                    let addItemsButtonObj = $("<button style='background: #dddddd'>+</button>");
                    addItemsButtonObj.click(function () {
                        // ajax to background
                        let thisPath = getLiPath($(this).parent());
                        let r = prependInstances(thisPath);
                        if (r[0] !== "success") {
                            alert(langDict(r[1]));
                            return;
                        }
                        // update fontground
                        let liObj = $("<li class='group_li'></li>");
                        liObj.append(generateInstances(["instances", "EName", []]));
                        $(this).next().prepend(liObj);
                        $(".group").sortable({
                            connectWith: ".group"
                        }).disableSelection();
                        $(".instances").sortable({
                            connectWith: ".instances"
                        }).disableSelection();
                    });
                    r.push(addItemsButtonObj);
                }
            }
            // group ul
            let ulObj = $("<ul class='group'></ul>");
            for (let curItemIndex = 0; curItemIndex < groupInfo.length; curItemIndex++) {
                let liObj = $("<li class='group_li'></li>");
                ulObj.append(liObj);
                {
                    let curItemTuple = groupInfo[curItemIndex];
                    let curItemObj = undefined;
                    if (curItemTuple[0] == "instances") {
                        curItemObj = generateInstances(curItemTuple);
                    } else if (curItemTuple[0] == "group") {
                        curItemObj = generateGroup(curItemTuple);
                    } else {
                        alert(langDict["typeError"])
                        return
                    }
                    liObj.append(curItemObj);
                }

                liObj.click(function (e) {
                    // 防止点击事件冒泡到父元素
                    e.stopPropagation();
                    // Alt + 左键 ： 删除
                    if (e.altKey) {
                        // ajax to background
                        let parentPath = getLiPath($(this));
                        let r = delLi(parentPath);
                        if (r[0] != "success") {
                            alert(langDict[r[1]]);
                            return
                        }
                        // update fontground
                        $(this).remove();
                    }
                });
            }
            r.push(ulObj);
            return r;
        }
    }

    // instanceInfoWindow
    {
        function instanceInfoWindow_showInstanceInfo() {
            $("#instanceInfo-noInstance").css("display", "none");
            $("#instanceInfo-selectedInstance").css("display", "block");
        }

        function instanceInfoWindow_showNoInstance() {
            $("#instanceInfo-noInstance").css("display", "block");
            $("#instanceInfo-selectedInstance").css("display", "none");
        }

        function instanceInfoWindow_addLabels() {
            for (let curLabelIndex = 0; curLabelIndex < labelSysDict["instance"].length; curLabelIndex++) {
                // 注意：这里的获取字典的内容是无序的
                let curLabelDict = labelSysDict["instance"][curLabelIndex];
                //generate label obj
                let curLabelObj = labelTemplate[curLabelDict["value_type"]]["generateLabelObj_func"](curLabelDict);
                $("#instanceInfo-selectedInstance").append(curLabelObj);
            }
        }

        function instanceInfoWindow_updateInstanceInfo(instanceInfo) {
            // update labels
            for (let curLabelIndex = 0; curLabelIndex < labelSysDict["instance"].length; curLabelIndex++) {
                // get the label data ready
                let curLabelDict = labelSysDict["instance"][curLabelIndex];
                let newValue = undefined;
                if (curLabelDict["key"] in instanceInfo) {
                    newValue = instanceInfo[curLabelDict["key"]];
                } else {
                    newValue = undefined;
                }
                let curLabelTypeDict = labelTemplate[curLabelDict["value_type"]];
                // generate a new label obj based on new value

                let labelObj = curLabelTypeDict["generateLabelObj_func"](curLabelDict, newValue);
                // replace the old label obj
                $("#instanceInfo-selectedInstance div[name='labelInfo-" + curLabelDict["key"] + "']").replaceWith(labelObj);
            }
        }

        function instanceInfoWindow_generateIdObj(id) {
            // idObj <div>
            let idObj = undefined;
            {
                idObj = $(" <div id='instanceInfo-id'></div>");
                idObj.css("padding-left", "10px");
                // keyObj <span>
                {
                    let keyObj = $("<span id='idKey'>id: </span>");
                    idObj.append(keyObj);
                }
                // valueObj <span>
                {
                    let valueObj = $("<span id='idValue'></span>");
                    let innerText = undefined;
                    if ((id == undefined) || (id == null) || (id == "")) {
                        innerText = "XXXX";
                    } else {
                        innerText = id
                    }
                    valueObj.text(innerText);
                    idObj.append(valueObj);
                }
            }
            //
            return idObj
        }

        function instanceInfoWindow_generateDescObj(desc) {
            let labelObj = undefined;
            // labelObj <div>
            {
                labelObj = $(" <div id='instanceInfo-desc'></div>");
                labelObj.css("padding-left", "10px");
                // keyObj <span>
                {
                    let keyObj = $("<span id='descKey'>desc: </span>");
                    labelObj.append(keyObj);
                }
                // valueObj <span>
                {
                    let valueObj = $("<input id='descValue' type='text'></input>");
                    labelObj.append(valueObj);
                    // display the label value
                    {
                        let inputText = undefined;
                        // if given a value, display the value
                        if (desc != undefined) {
                            inputText = desc;
                        }
                        // // if no value given, display the default value
                        // else if (labelDict["value_default"] != undefined){
                        //     inputText = labelDict["value_default"];
                        // }
                        // // if no given value and no default value
                        // else{
                        //     inputText = "";
                        // }
                        valueObj.attr("value", inputText);
                    }
                    // add change event
                    valueObj.change(function () {
                        // prepare ajax data
                        let id = $("#idValue").text();
                        let value = $("#descValue")[0].value;
                        // ajax to background
                        let r = setInstance(id, {"desc": value});
                        if (r[0] != "success") {
                            alert(langDict[r[1]]);
                            return;
                        } else {
                            // refresh nodeInfoWindow
                            nodeInfoWindow_refresh();
                            // refresh instanceInfoWindow
                            instanceInfoWindow_refresh();
                            // update the instancelink in instanceSelectWindow
                            instanceSelectWindow_updateOneInstance(r[1])
                        }
                    });
                }

            }
            // return
            return labelObj
        }

        function instanceInfoWindow_refresh() {
            if ($("#instanceInfo-selectedInstance").css("display") == "block") {
                // prepare ajax data
                let instanceId = $($($($("#instanceInfo-selectedInstance").children())[1]).children()[1]).text();
                // ajax to background
                let r = getInstanceById(instanceId);
                // display the new instance info in GUI
                if (r[0] != "success") {
                    instanceInfoWindow_showNoInstance();
                    alert(langDict[r[1]]);
                } else {
                    let instanceInfo = r[1];
                    instanceInfoWindow_updateInstanceInfo(instanceInfo);
                }
            }
        }
    }
}

// flask interface
{
    /**
     * flask interface. Given the position of a node, request the text of the node.
     *
     * @param nodePosition {string} Position string of the node.
     * @param callback {function} The call back function. This callback function has the following params: *data* is the
     * return data of the ajax require. *status* means whether the ajax require is success or not. *requireData* is a
     * array that includes the data which is send to server within the ajax require.
     */
    function getText(nodePosition, callback){
        requireData = {
            textNodeId: nodePosition
        };
        $("body").css("pointer-events", "none");
        $.post(
            "/getText",
            {
                textNodeId: nodePosition,
            },
            function (data, status) {
                $("body").css("pointer-events", "auto");
                callback(data, status, requireData);
            }
        );

    }

    /**
     * flask interface. request the content of corpora.
     *
     * @param callback {function} The call back function.
     *   The return value *data* of the POST request is given as the first param of the call back function.
     */
    function getCatalogue(){
        let contentInfo = undefined;
        $("body").css("pointer-events", "none");
        $.post(
            "/getCatalogue",
            { },
            function (data, status) {
                $("body").css("pointer-events", "auto");
                contentInfo = data;
            }
        );
        return contentInfo;
    }

    // group
    {
        function getGroup() {
            let r = undefined;
            $("body").css("pointer-events", "none");
            $.post(
                "/getGroup",
                {},
                function (data, status) {
                    $("body").css("pointer-events", "auto");
                    r = data;
                }
            );
            return r
        }

        function changeGroupName(groupPath, groupName){
            let r = undefined;
            $("body").css("pointer-events", "none");
            $.post(
                "/changeGroupName",
                {
                    "groupPath": String(groupPath ),
                    "groupName": groupName
                },
                function (data, status) {
                    $("body").css("pointer-events", "auto");
                    r = data;
                }
            );
            return r
        }

        function prependGroup(parentPath) {
            let r = undefined;
            $("body").css("pointer-events", "none");
            $.post(
                "/prependGroup",
                {"parentPath": String(parentPath)},
                function (data, status) {
                    $("body").css("pointer-events", "auto");
                    r = data;
                }
            );
            return r
        }

        function prependInstances(parentPath) {
            let r = undefined;
            $("body").css("pointer-events", "none");
            $.post(
                "/prependInstances",
                {"parentPath": String(parentPath)},
                function (data, status) {
                    $("body").css("pointer-events", "auto");
                    r = data;
                }
            );
            return r
        }

        function delLi(parentPath) {
            let r = undefined;
            $("body").css("pointer-events", "none");
            $.post(
                "/delLi",
                {"parentPath": String(parentPath)},
                function (data, status) {
                    $("body").css("pointer-events", "auto");
                    r = data;
                }
            );
            return r
        }

        function copyInstance(parentPath) {
            let r = undefined;
            $("body").css("pointer-events", "none");
            $.post(
                "/copyInstance",
                {"parentPath": String(parentPath)},
                function (data, status) {
                    $("body").css("pointer-events", "auto");
                    r = data;
                }
            );
            return r
        }

        function moveLi(fromPath, toPath){
            let r = undefined;
            $("body").css("pointer-events", "none");
            $.post(
                "/moveLi",
                {
                    "fromPath": String(fromPath),
                    "toPath": String(toPath)
                },
                function (data, status) {
                    $("body").css("pointer-events", "auto");
                    r = data;
                }
            );
            return r
        }
    }

    // node
    {
        /**
         * flask interface. Given the position of a node, request the info of the node.
         *
         * @param nodeId {string} Id string of the node.
         *   The return value *data* of the POST request is given as the first param of the call back function.
         */
        function getNodeById(nodeId) {
            let nodeInfo = undefined;
            $("body").css("pointer-events", "none");
            $.post(
                "/getNode",
                {
                    node_id: nodeId,
                },
                function (data, status) {
                    $("body").css("pointer-events", "auto");
                    nodeInfo = data;
                }
            );
            return nodeInfo
        }

        /**
         * flask interface. Given a range of nodes, check if those nodes correspond to a father node.
         *
         * @param startNodePosition {string} Position string of the first node.
         * @param endNodePosition {string} Position string of the last node.
         *   The return value *data* of the POST request is given as the first param of the call back function.
         */
        function getNodeByChildren(startNodePosition, endNodePosition, file_path) {
            let r = undefined;
            $("body").css("pointer-events", "none");
            $.post(
                "/getNode",
                {
                    start: startNodePosition,
                    end: endNodePosition,
                    file_path: file_path
                },
                function (data, status) {
                    $("body").css("pointer-events", "auto");
                    r = data;
                }
            );
            return r
        }

        function setNode(id, newValueDict) {
            let nodeInfo = undefined;
            newValueDict["nodeId"] = id;
            $("body").css("pointer-events", "none");
            $.post(
                "/setNode",
                newValueDict,
                function (data, status) {
                    $("body").css("pointer-events", "auto");
                    nodeInfo = data;
                }
            );
            return nodeInfo;
        }

        function delNode(nodeId)
        {
             let id = undefined;
            $("body").css("pointer-events", "none");
            $.post(
                "/delNode",
                {
                    node_id: nodeId,
                },
                function (data, status) {
                    $("body").css("pointer-events", "auto");
                    id = data;
                }
            );
            return id;
        }
        function addNodeByChildren(childrenNodePositionList, file_path) {
           // console.log(childrenNodePositionList)
            let r = undefined
            $("body").css("pointer-events", "none");
            $.post(
                "/addNode",
                {
                    childrenNodePositionList: childrenNodePositionList,
                    file_path: file_path
                },
                function (data, status) {
                    $("body").css("pointer-events", "auto");
                    r = data;
                }
            );
            if (r[0] == "success") {
                r[1] = PythonStyleToJsStyle(r[1])
            }
            return r
        }
        /**
         * flask interface. Add curve node according to the refer relationship of nodes
         */
        function addNodeByCurve(curve_id, file_path,from_node,to_node,a_z,b_z)
        {
            let r = undefined
            $("body").css("pointer-events", "none");
            $.post(
                "/addCurveNode",
                {
                    curve_id: curve_id,
                    file_path: file_path,
                    a_z:a_z,
                    b_z:b_z
                },
                function (data, status) {
                    $("body").css("pointer-events", "auto");
                    r = data;
                }
            );
            if (r[0] == "success") {
                r[1] = PythonStyleToJsStyle(r[1])
            }
            return r
        }
         /**
         * flask interface. get node list
         */
        function getNodepool(){
            let NodepoolInfo = undefined;
            let NodeList=[];
            $("body").css("pointer-events", "none");
            $.post(
                "/getNodepool",
                { },
                function (data, status) {
                    $("body").css("pointer-events", "auto");
                    NodepoolInfo = data;
                }
            );
            if(NodepoolInfo[0]=="success") {
                NodepoolInfo = NodepoolInfo[1];
                for (const key in NodepoolInfo) {
                    NodeList.push(key);
                }
            }
            return NodeList;
        }

    }

    // instance
    {
        function getInstanceById(id) {
            let r = undefined;
            $("body").css("pointer-events", "none");
            $.post(
                "/getInstance",
                {instance_id: id},
                function (data, status) {
                    // instanceInfoWindow_showInstanceInfo(data);
                    // instanceSelectWindow_updateOneInstance(data);
                    $("body").css("pointer-events", "auto");
                    r = data;
                }
            );
            return r
        }

        function setInstance(instanceId, infoDict) {
            let r = undefined;
            infoDict["id"] = instanceId;
            $("body").css("pointer-events", "none");
            $.post(
                "/setInstance",
                infoDict,
                function (data, status) {
                    $("body").css("pointer-events", "auto");
                    r = data;
                }
            );
            return r;
        }

        function addInstance_empty() {
            let r = undefined;
            $("body").css("pointer-events", "none");
            $.post(
                "/addInstance",
                {},
                function (data, status) {
                    $("body").css("pointer-events", "auto");
                    r = data;
                }
            );
            return r;
        }

        function addInstance_node(callback) {
            $("body").css("pointer-events", "none");
            $.post(
                "/addInstance",
                {
                    "position": $("#idValue").text()
                },
                function (data, status) {
                    $("body").css("pointer-events", "auto");
                    callback(data);
                }
            );
        }

        function delInstance(id){
            let r = undefined;
            $("body").css("pointer-events", "none");
            $.post(
                "/delInstance",
                {"instance_id": id},
                function (data, status) {
                    $("body").css("pointer-events", "auto");
                    r = data;
                }
            );
            return r;
        }

        function getInstancepool(){
            let InstanceInfo = undefined;
            let InstanceList=[];
            $("body").css("pointer-events", "none");
            $.post(
                "/getInstancepool",
                { },
                function (data, status) {
                    $("body").css("pointer-events", "auto");
                    InstanceInfo = data;
                }
            );
            if(InstanceInfo[0]=="success") {
               InstanceInfo = InstanceInfo[1];
                for (const key in InstanceInfo) {
                    InstanceList.push(key);
                }
            }
            return InstanceList;
        }

        function save() {
            $("body").css("pointer-events", "none");
            $.post(
                "/save",
                {},
                function (data, status) {
                    $("body").css("pointer-events", "auto");
                    if (data["success"] == true) {
                        alert(langDict["saved success!"])
                    }
                }
            );
        }
    }
}

// event logic
{
    // textWindow: 选中一段文本
    function textMouseup() {
        let slotNum = $(".slot").length
        // just select a mention
        if (slotNum == 0) {
            if(majorTextWindow_getSelectedIndexFromGui()!== undefined) {
                if (SelectedElementIndexList !== undefined) {
                    // 清除上次的选区效果
                    // if (select === undefined) {
                    //     selectedElementsBefore = undefined;
                    // } else {
                    //     selectedElementsBefore = majorTextWindow_getSelectedElementFromIndex(SelectedElementIndexList);
                    // }
                    // // console.log(selectedElementsBefore)
                    // l = selectedElementsBefore.length;
                    // if (selectedElementsBefore !== undefined) {
                    //     // majorTextWindow_hightlightElement2(selectedElementsBefore);
                    // }
                    // 清除上次推荐的instances
                    $("#rcmWindowOutput").empty();
                    $("#best_rcmWindowOutput").empty();
                }
                // 获取这次的选区，并更新全局变量
                SelectedElementIndexList = majorTextWindow_getSelectedIndexFromGui();
                // 如果没选中任何内容
                if (SelectedElementIndexList === undefined) {
                    nodeInfoWindow_showNoSelect();
                }
                // 如果选中了某些内容
                else {
                    // 把选区的index转换成element，因为用起来方便
                    let selectedElementsNow = majorTextWindow_getSelectedElementFromIndex(SelectedElementIndexList);

                    // 请求注释信息，并显示
                    let r = getNodeByChildren(
                        selectedElementsNow[0].attr("id"),
                        selectedElementsNow[selectedElementsNow.length - 1].attr("id"),
                        $("#textTab1").attr("name")
                    );
                    // 基于选中内容推荐instances
                let w =$(".instances_li")
                let index_list = []
                let find_element_list = []
                let desc_simple_list = []
                let desc_complex_list = []
                let text_pool = []
                let str_text_pool = []
                for(i=0; i<w.length; i++)
                {
                    index_list[i] = $(w[i]).attr("name")
                }
                for(i=0 ; i<index_list.length; i++)
                {
                    find_element_list[i] = getInstanceById(index_list[i])
                    //注意find_element_list[i][1]["mention_list"]取得的是里面的字典，有的只有一个，有的好几个
                    if (find_element_list[i][1]["mentions"] != null) {
                        desc_complex_list[i] = find_element_list[i][1]["mentions"]
                    }
                    else {
                        desc_complex_list[i] = ""
                    }
                    desc_simple_list[i] = find_element_list[i][1]["desc"]
                }


                for(i=0; i<desc_complex_list.length; i++)
                {
                    if(desc_complex_list[i].length != 1){
                        text_pool[i] = new Array();
                        for( k=0; k<desc_complex_list[i].length; k++)
                        {
                            if (desc_complex_list[i][k] == null) {
                                text_pool[i][k] = ""
                            }
                            else {
                                text_pool[i][k] = desc_complex_list[i][k].toString();
                            }
                            text_pool[i] = text_pool[i].concat(desc_simple_list[i]);
                            str_text_pool[i] = text_pool[i].join("");
                        }
                    }
                    if(desc_complex_list[i].length == 1){
                        text_pool[i] = desc_complex_list[i][0].toString();
                        str_text_pool[i] = text_pool[i];
                    }
                }
                // 区分是否为标注对象
                if (r[0] != "success") {
                    //节点不存在的情况下，r返回的列表为{"failed","no such node"};
                    nodeInfoWindow_showNoNode();
                    let mark_mouseip_list = [];
                    let mark_merge_list = [];
                    for(i=0; i<selectedElementsNow.length; i++)
                    {
                        mark_mouseip_list[i] = selectedElementsNow[i].prop("innerText")
                    }
                    mark_merge_list = mark_mouseip_list.join("")
                    for(i=0; i<str_text_pool.length; i++)
                    {
                        // console.log(desc_simple_list[i].split(" ").join(""))
                        // console.log(mark_merge_list.split(" ").join(""))
                        if((desc_simple_list[i] != mark_merge_list)&&(desc_simple_list[i].match(mark_merge_list))){
                            let q = $(w[i]).clone(true);
                            $("#rcmWindowOutput").append(q);
                         }
                         else if(desc_simple_list[i].split(" ").join("")== mark_merge_list.split(" ").join("")){
                            let q = $(w[i]).clone(true);
                            $("#best_rcmWindowOutput").append(q);
                         }
                    }
                }
                else {
                    //节点存在的情况下，以下功能已实现
                    cur_Node=r[1]["id"];
                    cur_Node_Z= get_node_z(r[1]["id"]);

                    // 重新加载文本
                    getText(
                        majorTextWindow_getCurArticleNodePosition(),
                        function (returnData, status, requireData) {
                            majorTextWindow_setCurArticleNodePosition(requireData["textNodeId"]);
                            majorTextWindow_updateText(returnData, 0);
                            majorTextWindow_show(returnData);
                        }
                    );
                    // majorTextWindow_redrawSvg();
                    nodeInfoWindow_updateNodeInfo(r[1]);
                    nodeInfoWindow_showNodeInfo();
                    // 高亮选中文本并添加下划线
                    if (SelectedElementIndexList != undefined) {
                        let selectedElement = majorTextWindow_getSelectedElementFromIndex(SelectedElementIndexList);
                        majorTextWindow_addunderline(selectedElement);
                        majorTextWindow_hightlightElement(selectedElement);
                    }
                    for(let i=0; i<str_text_pool.length; i++)
                    {
                        if(str_text_pool[i]===undefined)
                            continue;
                        if((str_text_pool[i].match(r[1]["text"]))&&(desc_simple_list[i] != r[1]["text"])){
                            let q = $(w[i]).clone(true);
                            $("#rcmWindowOutput").append(q);
                         }
                        else if(desc_simple_list[i] == r[1]["text"]){
                            let q = $(w[i]).clone(true);
                            $("#best_rcmWindowOutput").append(q);
                            }
                    }

                }
                }
            }
        }
        // select a mention, get the corresponding node, and fill current slot with the node.
        else if (slotNum == 1) {
            // 获取这次的选区，并更新全局变量
            let curSelectedIndex = majorTextWindow_getSelectedIndexFromGui();
            // 如果没选中任何内容
            if (curSelectedIndex === undefined) {
                return
            }
            // 如果选中了某些内容
            else {
                // 尝试获取选区对应的node
                let selectedElements = majorTextWindow_getSelectedElementFromIndex(curSelectedIndex);
                let r = getNodeByChildren(
                    selectedElements[0].attr("id"),
                    selectedElements[selectedElements.length - 1].attr("id"),
                    $("#textTab1").attr("name")
                );
                // 如果获取到了node，就调用slot元素的处理函数
                if (r[0] == "success") {
                    new_Node_Z=get_node_z(r[1]["id"]);
                    $(".slot")[0].fillSlot(r[1]["id"]);
                } else {
                    alert(langDict[r[1]]);
                    return;
                }
            }

        } else {
            alert(langDict["Error: More than one slots are to be filled."])
        }

    }
    // textClick: 点击svg
    function textClick(e)
    {
         let slotNum = $(".slot").length;
          if (slotNum == 0)
          {
             // 获取这次的选区
           let curSelectedelement = document.elementFromPoint(e.clientX,e.clientY);
            // 如果没选中任何内容
            if (curSelectedelement === undefined) {
                return;
            }
            // 如果选中了某些内容
            else {
                // 获取点击元素的id
                let curSelectedelementid = curSelectedelement.id;
                if (curSelectedelementid === undefined || curSelectedelementid.split("-").length<=2)
                    return;
                 // 重新加载文本
                // getText(
                //     majorTextWindow_getCurArticleNodePosition(),
                //     function (returnData, status, requireData) {
                //         majorTextWindow_setCurArticleNodePosition(requireData["textNodeId"]);
                //         majorTextWindow_updateText(returnData, 0);
                //         majorTextWindow_show(returnData);
                //     }
                // );
                // majorTextWindow_redrawSvg();
                // changeSVGcolor(curSelectedelementid,"red");

            }
          }else if (slotNum == 1) {
            // 获取这次的选区
           let curSelectedelement = document.elementFromPoint(e.clientX,e.clientY);
            // 如果没选中任何内容
            if (curSelectedelement === undefined) {
                return
            }
            // 如果选中了某些内容
            else {
                // 获取点击元素的id

                let curSelectedelementid = curSelectedelement.id;
                // console.log(curSelectedelementid);
                if (curSelectedelementid === undefined || curSelectedelementid===null || curSelectedelementid==="textTab1" || curSelectedelementid.length==0)
                    return;
                // 尝试获取选区对应的node
                // console.log(curSelectedelementid);
                let file_id = $("#textTab1").attr("name");
                if(curSelectedelementid.split("-")>2) {
                    let curSelectednode = "n:" + file_id + ":" + curSelectedelementid;
                    let r = getNodeById(curSelectednode);
                    // 如果获取到了node，就调用slot元素的处理函数
                    if (r[0] == "success") {
                        $(".slot")[0].fillSlot(r[1]["id"]);
                    } else {
                        alert(langDict[r[1]]);
                    }
                }else {
                     new_Node_Z=parseInt($("#"+curSelectedelementid).attr("z"));
                    curSelectedelementid=curSelectedelementid.split("_")
                    let curSelectednode = "n:" + file_id + ":" + curSelectedelementid[0];
                    // new_Node_Z=parseInt(curSelectedelementid[1]);
                    let r = getNodeById(curSelectednode);
                    // 如果获取到了node，就调用slot元素的处理函数
                    if(r===undefined)
                         return;
                    if (r[0] == "success") {
                        $(".slot")[0].fillSlot(r[1]["id"]);
                    } else {
                        alert(langDict[r[1]]);
                    }
                }
            }

          } else {
            alert(langDict["Error: More than one slots are to be filled."])
        }
    }
    // nodeInfoWindow: 单击“添加标注对象”按钮
    function addNodeButtonClick() {
        // 当前有选中某个指称
        if (SelectedElementIndexList !== undefined) {
            // 把选区的index转换成position（因为flask接口要求position）
            let selectedElementPositionList = [];
            let selectedElement = majorTextWindow_getSelectedElementFromIndex(SelectedElementIndexList);
            for (let i = 0; i < selectedElement.length; i++) {
                selectedElementPositionList[i] = selectedElement[i].attr("id");
            }
            // 向后台发送操作请求
            let r = addNodeByChildren(selectedElementPositionList, $("#textTab1").attr("name"));
            // 区分是否为标注对象
            if (r[0] != "success") {
                nodeInfoWindow_showCannotAddNode();
                alert(langDict[r[1]])
            } else {
                let newNodeInfo = r[1]

                //加入节点列表
                node_label_list.push(newNodeInfo["id"]);
                // 重新加载文本,因为要清除之前的选中效果
                getText(
                    majorTextWindow_getCurArticleNodePosition(),
                    function (returnData, status, requireData) {
                        majorTextWindow_setCurArticleNodePosition(requireData["textNodeId"]);
                        majorTextWindow_updateText(returnData, 0);
                        majorTextWindow_show(returnData);
                    }
                );
                // majorTextWindow_redrawSvg();

                cur_Node=newNodeInfo["id"];
                cur_Node_Z=0;
                  // 更新标注信息
                nodeInfoWindow_updateNodeInfo(newNodeInfo);
                // 显示标注信息
                nodeInfoWindow_showNodeInfo(newNodeInfo);
                // 高亮选中文本并添加下划线
                if (SelectedElementIndexList != undefined) {
                    let selectedElement = majorTextWindow_getSelectedElementFromIndex(SelectedElementIndexList);
                    majorTextWindow_hightlightElement(selectedElement);
                    //需要判断是否有跨行节点
                    majorTextWindow_addunderline(selectedElement);
                }
            }
        }
        // 当前没有选中任何指称
        else {
            alert(langDict["Can not create node, because no mention is selected."]);
        }
    }
    // nodeInfoWindow: 单击“添加空节点”按钮
    function addVoidNodeButtonClick(){
        // 当前有选中某个指称
        if (SelectedElementIndexList !== undefined) {
            let selectedElement = majorTextWindow_getSelectedElementFromIndex(SelectedElementIndexList);
            let selectedElementPosition = selectedElement[selectedElement.length-1].attr("id");
            selectedElementPosition = selectedElementPosition.split('-')[1];

            let temp_selectedElementPosition=selectedElementPosition;
            void_list.push(doc_id+":"+String(temp_selectedElementPosition));
            getText(
                    majorTextWindow_getCurArticleNodePosition(),
                    function (returnData, status, requireData) {
                        majorTextWindow_setCurArticleNodePosition(requireData["textNodeId"]);
                        majorTextWindow_updateText(returnData, selectedElementPosition);
                        majorTextWindow_show(returnData);
                        }
                    );
            majorTextWindow_redrawSvg();

            // 把选区的index转换成position（因为flask接口要求position）
            let selectedElementPositionList = [];
            // for (let i = 0; i < selectedElement.length; i++) {
            //     selectedElementPositionList[i] = selectedElement[i].attr("id");
            // }
             selectedElementPositionList.push(selectedElementPosition+"-"+selectedElementPosition);

            // 向后台发送操作请求
            let r = addNodeByChildren(selectedElementPositionList, $("#textTab1").attr("name"));
            // 区分是否为标注对象
            if (r[0] != "success") {
                nodeInfoWindow_showCannotAddNode();
                alert(langDict[r[1]])
            } else {
                let newNodeInfo = r[1]

                //加入节点列表
                node_label_list.push(newNodeInfo["id"]);
                cur_Node=newNodeInfo["id"];
                cur_Node_Z=0;
                 // 更新标注信息
                nodeInfoWindow_updateNodeInfo(newNodeInfo);
                // 显示标注信息
                nodeInfoWindow_showNodeInfo(newNodeInfo);
                // 标记选中文本
                if (SelectedElementIndexList != undefined) {
                    let selectedElement =[];
                    selectedElement.push($("#"+selectedElementPosition+"-"+selectedElementPosition));
                    let selected_margin=selectedElementPosition+"-"+selectedElementPosition;

                    majorTextWindow_hightlightElement(selectedElement)
                    // majorTextWindow_addmargin(selectedElement);
                    // majorTextWindow_addunderline(selectedElement);
                }
            }
        }
        // 当前没有选中任何指称
        else {
            alert(langDict["Can not create node, because no mention is selected."]);
        }
    }
     // nodeInfoWindow： 单击“x”按钮 删除节点
    function nodeInfodelClick(){
        if(cur_Node===undefined)
            return;
        //如果是curve node要删除该节点,并删除from node 的refer
        if(cur_Node.split("-").length>2)
        {
            let label=get_from_node_to_node(cur_Node);
            let [from_node,to_node]=[label[0],label[1]];
            let r=undefined;
            // r=getNodeById(to_node);
            // if(r[[0]=="success"]) {
            //     let cur_noed_refers = r[1]["refer"];
            //     for(const k in cur_noed_refers)
            //     {
            //         if(cur_noed_refers==from_node)
            //         {
            //             [from_node,to_node]=[to_node,from_node];
            //             break;
            //         }
            //     }
            // }
             r=getNodeById(from_node);
             //调用nodeinfo_window refer #del_node按钮
             nodeInfoWindow_updateNodeInfo(r[1]);
             nodeInfoWindow_showNodeInfo();
             //删除refer关系
             $("#del_node_"+to_node.split(":")[2]).click();
              nodeInfoWindow_showNoNode();
        }
        //如果是普通节点
        else {
             //先依次删除与node指向的curve node与instetance关系
             let r=getNodeById(cur_Node);
             if(r[0]=="success")
            {
               let refers= r[1]["refer"];
               for(const k in refers)
               {
                   if(refers[k][0]=="n")
                   {
                        $("#del_node_"+refers[k].split(":")[2]).click();
                   }
                   if(refers[k][0]=="i")
                   {
                       $("#del_instance_"+refers[k].split(":")[1]).click();
                   }
               }
            }
            // 删除该节点
            delNode(cur_Node);
            nodeInfoWindow_showNoNode();
            //重新初始化node list
            TextWindow_initNodes();
            getText(
                majorTextWindow_getCurArticleNodePosition(),
                function (returnData, status, requireData) {
                    majorTextWindow_setCurArticleNodePosition(requireData["textNodeId"]);
                    majorTextWindow_updateText(returnData);
                    majorTextWindow_show(returnData);
                }
            );
            majorTextWindow_redrawSvg();
        }
     }
    // instanceSelectWindow: 单击“+”按钮
    function addInstancePlusButtonClick() {
        // ajax to background
        let r = addInstance_empty();
        if (r[0] != "success") {
            alert(langDict[r[1]])
            return
        } else {
            let instanceInfo = r[1]
            // add instance obj in instanceSelectWindow
            instanceSelectWindow_updateOneInstance(instanceInfo);
            // show instance info in instanceInfoWindow
            instanceInfoWindow_showInstanceInfo();
            instanceInfoWindow_updateInstanceInfo(instanceInfo);
        }
    }

    // instanceSelectWindow: 单击“→”按钮
    function addInstanceArrowButtonClick() {
        // 如果curNode不存在
        if ($("#nodeInfo-selectedNode").css("display") == "none") {
            // 如果有选中一个mention，只差创建node
            if ($("#nodeInfo-noNode").css("display") == "block") {
                $("#addNodeButton").click();
            }
            // 如果连mention都没选
            else {
                alert(langDict["you should select a mention at first."]);
                return;
            }
        }
        // 现在curNode存在了
        {
            // 先新建instance
            $("#addInstancePlus").click();
            // 再把curNode指向curInstance
            $("#mention_listValue").children("div").children(":last").prev().prev().click();
            // 初始化curInstance的desc
            let r = getNodeById($("#idValue").text());
            // let nodeText = r[1]["text"];
            let nodeText = get_curve_node_text(r[1]);
            $("#descValue").attr("value", nodeText);
            $("#descValue").change();
            //referCI,让node指向instance
            $("#referCI").click();
        }
    }

    // // instanceSelectWindow: 单击实例
    function instanceClick(instanceElement) {
        let isHaveInstanceSlotActive = undefined;
        if ($(".curInstanceSlot").length == 0) {
            isHaveInstanceSlotActive = false;
        } else {
            isHaveInstanceSlotActive = true;
        }
        // 用此实例填充槽
        if (isHaveInstanceSlotActive) {
            // 数据准备
            var slot = curTriggerInstanceSlot;
            let instanceSlot = $(".curInstanceSlot");
            if (slot.parentElement.parentElement.getAttribute("id") === "nodeInfoWindow") {
                var slotType = "node";
                var position = $("#idValue").text();
            }
            newInstanceId = curSelectedInstance.name;
            // 向后台传数据
            if (slotType === "node") {
                let r = setNode(position, {"instance": newInstanceId});
                if (r != "success") {
                    alert(langDict[r]);
                    return;
                }
                // refresh nodeInfoWindow
                nodeInfoWindow_refresh();
                // refresh instanceInfoWindow
                instanceInfoWindow_refresh();
            } else if (slotType === "instance") {
                let r = setInstance();
                if (r != "success") {
                    alert(langDict[r]);
                    return;
                }
                // refresh nodeInfoWindow
                nodeInfoWindow_refresh();
                // refresh instanceInfoWindow
                instanceInfoWindow_refresh();
            }
            // 取消当前solt的待选特效
            curTriggerInstanceSlot.classList.remove("curSlot");
            document.body.style.cursor = "";
            //
            curTriggerInstanceSlot = undefined
            // 更新instance info
            if (curSelectedInstance != undefined) {
                getInstanceById(curSelectedInstance.name);
            }
        }
        // 展示实例
        else {
            let instanceIdStr = instanceElement.name;
            let instanceInfo = getInstanceById(instanceIdStr);
            instanceInfoWindow_showInstanceInfo(instanceInfo);
            instanceSelectWindow_updateOneInstance(instanceInfo);
        }
    }

    // instanceInfoWindow： 单击“x”按钮
    function delInstanceButtonClick() {
        //
        let curInstanceId = $("#idValue").text();
        let r = delInstance(curInstanceId);
        if (r[0] !== "success"){
            alert(r[1]);
            return
        }
        //
        instanceInfoWindow_showNoInstance();
        nodeInfoWindow_refresh();
        $(".instance[name=" + curInstanceId + "]").remove();

    }

    // wholeSystem: ctrl+s
    function ctrls() {
        save();
    }

}