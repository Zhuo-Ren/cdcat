// 全局变量。array of html elements。选中的文本所对应的元素的数组。
// var selectedElements = 0;
// var selectedIndex = undefined;

var SelectedElementIndexList  = undefined;
var k = 0;

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
                    //curSpan.html(index + ": " + contentArray[1]);
                    curSpan.html(contentArray[1]);
                    curSpan.addClass("file");
                    // 为目录添加单击事件
                    curSpan.click(function () {
                        getText(
                            this.id,
                            function (returnData, status, requireData) {
                                majorTextWindow_setCurArticleNodePosition(requireData["textNodeId"]);
                                majorTextWindow_updateText(returnData, 0);
                                majorTextWindow_show(returnData);
                            }
                        );
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
             * highlighted as long as they are existing.
         *
         * @param elementList
         */
        function majorTextWindow_hightlightElement(elementList) {
            for (var i = 0; i < elementList.length; i++) {
                elementList[i][0].style = "color: red";
            }
        }

        /**
         * If majorTextWindow shows the chars of a node, the name of majorTextWindow is the position of this node. If
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
         *
         * @param data The Array of every chair
         * @param scroll
         */
        function majorTextWindow_updateText(data, scroll) {
            let majorTextWindow = $("#textTab1");
            majorTextWindow.empty();
            // add html element for each char.
            for (i = 0; i < data.length; i++) {
                let elementText = "";
                elementText += "<div " +
                    "id=" + data[i]["id"] +
                    " " +
                    "desc=" + data[i]["char"]+
                    " " +
                    "class='char'" +
                    ">";
                if (data[i]["char"] === "\n") {
                    elementText += "<div>\\n</div> ";
                    elementText += "</div>";
                    elementText += "<br style='clear:both;'>";
                } else if (data[i]["char"] === "\r") {
                    elementText += "<div>\\r</div>";
                    elementText += "</div>";
                    elementText += "<br style='clear:both;'>";
                } else if (data[i]["char"] === " ") {
                    elementText += "<div>&nbsp; <div>";
                    elementText += "</div>";
                } else {
                    elementText += "<div>" + data[i]["char"] + "</div>";
                    elementText += "</div>";
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
            // add positionObj <div>
            let positionObj = nodeInfoWindow_generatePositionObj()
            $("#nodeInfo-selectedNode").append(positionObj);
            // add labels
            for (let curLabelIndex = 0; curLabelIndex < labelSysDict["node"].length; curLabelIndex++) {
                let curLabelDict = labelSysDict["node"][curLabelIndex];
                //generate label obj
                let curLabelObj = labelTemplate[curLabelDict["value_type"]]["generateLabelObj_func"](curLabelDict);
                $("#nodeInfo-selectedNode").append(curLabelObj);
                //add event to label obj
                // labelTemplate[curLabelDict["value_type"]]["addEvent_func"](curLabelDict);
                //add updateValueFunc to label (in labelSysDict)
                // curLabelUpdateValueFunc = labelTemplate[curLabelDict["value_type"]]["addUpdateValueFunc_func"](curLabelDict);
                // labelSysDict["node"][curLabelIndex]["updateValueFunc"] = curLabelUpdateValueFunc;
            }
        }

        function nodeInfoWindow_showCannotAddNode() {
            alert(langDict["can not add node based on current mention."])
        }

        function nodeInfoWindow_generatePositionObj(position) {
            let positionObj = $(" <div id='nodeInfo-position'></div>");
            positionObj.css("padding-left", "10px");
            // keyObj <span>
            let keyObj = $("<span id='positionKey'>position: </span>");
            positionObj.append(keyObj);
            // valueObj <span>
            let valueObj = $("<span id='positionValue'></span>");
            let innerText = undefined;
            // if given a value, display the value
            if (position != undefined) {
                innerText = position;
            } else {
                innerText = "XXXX";
            }
            valueObj.text(innerText);
            positionObj.append(valueObj);
            //
            return positionObj
        }

        /**
         * This function update the info in nodeInfoWindow.
         *
         * @param nodeInfo: A node info dict. Each item is a property or a label.
         *   The disappear of a label in the dict means annotators never label the label.
         *   Also,{"label_key": undefined} means annotators never label the label.
         */
        function nodeInfoWindow_updateNodeInfo(nodeInfo) {
            // update position
            // get the position data ready
            let position = nodeInfo["position"];
            // generate new positionObj
            let positionObj = nodeInfoWindow_generatePositionObj(position);
            // replace the old label obj
            $("#nodeInfo-position").replaceWith(positionObj);
            // update labels
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
                $("#nodeInfo-" + curLabelConfig["key"]).replaceWith(labelObj);
            }
        }

        function nodeInfoWindow_refresh() {
            if ($("#nodeInfo-selectedNode").css("display") == "block") {
                // prepare ajax data
                let nodePosition = $("#positionValue").text();
                // ajax to background
                let r = getNodeByPosition(nodePosition);
                // display the new node info in GUI
                if (r[0] != "success") {
                    nodeInfoWindow_showNoNode();
                } else {
                    let nodeInfo = r[1];
                    nodeInfoWindow_updateNodeInfo(nodeInfo);
                }
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
            let instance_list = r[1][2][0][2]
            let id_list = []
//            console.log(instance_list)
            for(let i =0; i<instance_list.length; i++){
                id_list.push(instance_list[i])
            }
            console.log(id_list)
            for(let i=0; i<id_list.length; i++){
                get_instance_desc(id_list[i])
            }
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
            let targetElement = $(".instance[name=" + data["id"] + "]");
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
         * del a instance。
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
            liObj.attr('name', curInstancelink);
            liObj.addClass('instance');

            liObj.text(get_instance_desc(curInstancelink))

            // if (curInstancelink['desc'] !== undefined) {
            //     if (curInstancelink['desc'] !== "") {
            //         liObj.text(curInstancelink['desc']);
            //     } else {
            //         liObj.text('　');
            //     }
            // } else {
            //     liObj.text('　');
            // }


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
            // add idObj <div>
            let idObj = instanceInfoWindow_generateIdObj();
            $("#instanceInfo-selectedInstance").append(idObj);
            // add descObj <div>
            let descObj = instanceInfoWindow_generateDescObj();
            $("#instanceInfo-selectedInstance").append(descObj);
            // add labels
            for (let curLabelIndex = 0; curLabelIndex < labelSysDict["instance"].length; curLabelIndex++) {
                let curLabelDict = labelSysDict["instance"][curLabelIndex];
                //generate label obj
                curLabelObj = labelTemplate[curLabelDict["value_type"]]["generateLabelObj_func"](curLabelDict);
                $("#instanceInfo-selectedInstance").append(curLabelObj);
                //add event to label obj
                // labelTemplate[curLabelDict["value_type"]]["addEvent_func"](curLabelDict);
                //add updateValueFunc to label (in labelSysDict)
                // curLabelUpdateValueFunc = labelTemplate[curLabelDict["value_type"]]["addUpdateValueFunc_func"](curLabelDict);
                // labelSysDict["instance"][curLabelIndex]["updateValueFunc"] = curLabelUpdateValueFunc;
            }
        }

        function instanceInfoWindow_updateInstanceInfo(instanceInfo) {
            // $("#idValue").text(data["id"]);
            // $("#descValue").val(data["desc"]);
            // if(data["kg"] !== undefined){
            //     $("#kgValue").val(data["kg"])
            // }
            // var mentionListsValue = $("#mentionListsValue");
            // mentionListsValue.empty();
            // for(var i=0; i<data["mention_list"].length; i++){
            //     var curMention = data["mention_list"][i];
            //     var curMentionLine = $("<div class='instanceMentionDiv'></div>");
            //     curMentionLine.append($("<span>[</span>"));
            //     for (var j=0; j<curMention.length; j++){
            //         var curPart = curMention[j];
            //         curMentionLine.append($(
            //             "<button" +
            //                 " name=\"" + curPart["position"]+ "\"" +
            //             ">" +
            //                 curPart["text"] +
            //             "</button>"
            //         ));
            //     }
            //     curMentionLine.append($("<button class='instance_extentMentionList_button' name=" + (i).toString() +">→</button>"));
            //     curMentionLine.append($("<span>]</span>"));
            //     mentionListsValue.append(curMentionLine)
            // }
            // mentionListsValue.append($("<button id='instance_addMentionList_button'>+</button>"));
            // update id
            let idObj = instanceInfoWindow_generateIdObj(instanceInfo["id"]);
            $("#instanceInfo-id").replaceWith(idObj);
            // update desc
            let descObj = instanceInfoWindow_generateDescObj(instanceInfo["desc"]);
            $("#instanceInfo-desc").replaceWith(descObj);
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
                $("#nodeInfo-" + curLabelDict["key"]).replaceWith(labelObj);
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
                let instanceId = $("#idValue").text();
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

    function get_instance_desc(id){
        let instance_desc = undefined
        $.post(
            "/getInstanceDesc",
            {
                "id": id
            },
            function (data, status) {
//                $("body").css("pointer-events", "auto");
//                callback(data, status, requireData);
                  instance_desc = data
            }
        );
        return instance_desc

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
         * @param nodePosition {string} Position string of the node.
         * @param callback {function} The call back function.
         *   The return value *data* of the POST request is given as the first param of the call back function.
         */
        function getNodeByPosition(nodePosition) {
            let nodeInfo = undefined;
            $("body").css("pointer-events", "none");
            $.post(
                "/getNode",
                {
                    position: nodePosition,
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
        function getNodeByChildren(startNodePosition, endNodePosition) {
            let r = undefined;
            $("body").css("pointer-events", "none");
            $.post(
                "/getNode",
                {
                    start: startNodePosition,
                    end: endNodePosition
                },
                function (data, status) {
                    $("body").css("pointer-events", "auto");
                    r = data;
                }
            );
            return r
        }

        function setNode(position, newValueDict) {
            let nodeInfo = undefined;
            newValueDict["position"] = position;
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

        function addNodeByChildren(childrenNodePositionList) {
            let r = undefined
            $("body").css("pointer-events", "none");
            $.post(
                "/addNode",
                {
                    childrenNodePositionList: childrenNodePositionList
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
                    "position": $("#positionValue").text()
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
            // 清除上次的选区效果
            if (SelectedElementIndexList !== undefined) {
                let selectedElementsBefore = majorTextWindow_getSelectedElementFromIndex(SelectedElementIndexList);
                for (let i = 0; i < selectedElementsBefore.length; i++) {
                    selectedElementsBefore[i][0].style = "color: black";
                }
                //清除上次的推荐内容
                //这个地方需要优化，清除后就不可再次加入了
//                $("#rcmWindowOutput").html("")
                $("#rcmWindowOutput").empty();
                $("#best_rcmWindowOutput").empty();
//                $("#rcmWindowOutput").stopPropagation();

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
                // 选中效果
                majorTextWindow_hightlightElement(selectedElementsNow);
                // 请求注释信息，并显示
                let r = getNodeByChildren(
                    selectedElementsNow[0].attr("id"),
                    selectedElementsNow[selectedElementsNow.length - 1].attr("id"),
                );
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
                    desc_complex_list[i] = find_element_list[i][1]["mention_list"]
                    desc_simple_list[i] = find_element_list[i][1]["desc"]
                }
                //console.log(desc_complex_list)
                for(i=0; i<desc_complex_list.length; i++)
                {
                    if(desc_complex_list[i].length != 1){
                        text_pool[i] = new Array();
                        for( k=0; k<desc_complex_list[i].length; k++)
                        {
                            text_pool[i][k] = desc_complex_list[i][k]["text"].toString();
                            text_pool[i] = text_pool[i].concat(desc_simple_list[i]);
                            str_text_pool[i] = text_pool[i].join("");
                        }
                    }
                    if(desc_complex_list[i].length == 1){
                        text_pool[i] = desc_complex_list[i][0]["text"].toString();
                        str_text_pool[i] = text_pool[i];
                    }
//                        console.log(str_text_pool[i])
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
                        if((str_text_pool[i].match(mark_merge_list))&&(desc_simple_list[i] != mark_merge_list)){
                            //$("#rcmWindowOutput").append(w[i]);
                            let q = $(w[i]).clone(true);
                            $("#rcmWindowOutput").append(q);
                         }
                         else if(desc_simple_list[i] == mark_merge_list){
                            //$("#best_rcmWindowOutput").append(w[i]);
                            let q = $(w[i]).clone(true);
                            $("#best_rcmWindowOutput").append(q);
                         }
                    }
                }
                else {
                    //节点存在的情况下，以下功能已实现
                    nodeInfoWindow_updateNodeInfo(r[1]);
                    nodeInfoWindow_showNodeInfo();
                    //console.log(r[1]["text"]);
                    for(i=0; i<str_text_pool.length; i++)
                    {
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
                // 取消鼠标特效

                // 尝试获取选区对应的node
                let selectedElements = majorTextWindow_getSelectedElementFromIndex(curSelectedIndex);
                let r = getNodeByChildren(
                    selectedElements[0].attr("id"),
                    selectedElements[selectedElements.length - 1].attr("id"),
                );
                // 如果获取到了node，就调用slot元素的处理函数
                if (r[0] == "success") {
                    $(".slot")[0].fillSlot(r[1]["position"]);
                } else {
                    alert(langDict[r[1]]);
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
            let r = addNodeByChildren(selectedElementPositionList);
            // 区分是否为标注对象
            if (r[0] != "success") {
                nodeInfoWindow_showCannotAddNode();
                alert(langDict[r[1]])
            } else {
                let newNodeInfo = r[1]
                // 更新标注信息
                nodeInfoWindow_updateNodeInfo(newNodeInfo);
                // 显示标注信息
                nodeInfoWindow_showNodeInfo(newNodeInfo);
                // 重新加载文本
                getText(
                    majorTextWindow_getCurArticleNodePosition(),
                    function (returnData, status, requireData) {
                        majorTextWindow_setCurArticleNodePosition(requireData["textNodeId"]);
                        majorTextWindow_updateText(returnData, 0);
                        majorTextWindow_show(returnData);
                    }
                );
                // 高亮选中文本
                if (SelectedElementIndexList != undefined) {
                    let selectedElement = majorTextWindow_getSelectedElementFromIndex(SelectedElementIndexList);
                    majorTextWindow_hightlightElement(selectedElement);
                }

            }
        }
        // 当前没有选中任何指称
        else {
            alert(langDict["Can not create node, because no mention is selected."]);
        }
    }

    // nodeInfoWindow: 标注信息变动（token）
    function nodeTokenChange() {
        var position = $("#positionValue").text();
        var tokenValue = $("#tokenValue :checked").attr("value");
        if (tokenValue === "false") {
            tokenValue = false;
        } else if (tokenValue === "true") {
            tokenValue = true;
        } else {
            alert("搞笑")
        }
        let r = setNode(position, {"token": tokenValue});
        if (r != "success") {
            alert(langDict[r]);
            return;
        }
        // refresh nodeInfoWindow
        nodeInfoWindow_refresh();
        // refresh instanceInfoWindow
        instanceInfoWindow_refresh();
    }

    // nodeInfoWindow: 标注信息变动（semanticType）
    function nodeSemanticTypeChange() {
        var position = $("#positionValue").text();
        var semanticTypeValue = $("#semanticTypeValue :checked").attr("value");
        let r = setNode(position, {"semanticType": semanticTypeValue});
        if (r != "success") {
            alert(langDict[r]);
            return;
        }
        // refresh nodeInfoWindow
        nodeInfoWindow_refresh();
        // refresh instanceInfoWindow
        instanceInfoWindow_refresh();
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
                $("#nodeInfo-noNode").click();
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
            let r = getNodeByPosition($("#positionValue").text());
            let nodeText = r[1]["text"];
            $("#descValue").attr("value", nodeText);
            $("#descValue").change();
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
                var position = $("#positionValue").text();
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