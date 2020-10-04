// 全局变量。array of html elements。选中的文本所对应的元素的数组。
// var selectedElements = 0;
// var selectedIndex = undefined;
var SelectedElementIndexList  = undefined;

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

// <!-- ui interface -->
    /**
     *  In catalogueWindow, scroll to the given element.
     *
     */
    function catalogueWindow_scroll(){}
    /**
     * In catalogueWindow, set content based on *contentArray*.
     */
    function catalogueWindow_updateContent(contentArray){
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
        function addContentElement(parentUl, contentArray){
            flag1 = (typeof contentArray[0] == "string");
            flag2 = (typeof contentArray[1] == "string");
            isLeaf = (flag1 && flag2);
            // 添加当前节点
            curLi = $("<li></li>");
            parentUl.append(curLi);
            curSpan = $("<span></span>")
            curLi.append(curSpan);
            curSpan.attr("id", contentArray[0]);
            curSpan.css("white-space","nowrap")
            positionString = contentArray[0];
            if (positionString === ""){
                index = "root";
            }else{
                positionList = positionString.split("-");
                index = positionList[positionList.length - 1];
            }
            if (isLeaf){
                // 当前是叶子节点（文件）
                curSpan.html(index + ": " + contentArray[1]);
                curSpan.addClass("file");
                // 为目录添加单击事件
                curSpan.click(function(){
                    getText(
                        this.id,
                        function (returnData, status, requireData){
                            majorTextWindow_setCurArticleNodePosition(requireData["textNodeId"]);
                            majorTextWindow_updateText(returnData, 0);
                            majorTextWindow_show(returnData);
                        }
                    );
                });
            } else{
                // 当前是枝干节点（文件夹）
                curSpan.html(index);
                curSpan.addClass("folder");
                let curUl = $("<ul></ul>");
                curLi.append(curUl);

                // 遍历直接孩子
                for (let i=1; i<contentArray.length; i++){
                    addContentElement(curUl, contentArray[i]);
                }
            }
        }
        addContentElement(contentRoot, contentArray);
        // 为目录添加样式
        $("#browser").treeview({
            toggle: function() {
                console.log("%s was toggled.", $(this).find(">span").text());
            }
        });
        $("#add").click(function() {
            var branches = $("<li><span class='folder'>New Sublist</span><ul>" +
                "<li><span class='file'>Item1</span></li>" +
                "<li><span class='file'>Item2</span></li></ul></li>").appendTo("#browser");
            $("#browser").treeview({
                add: branches
            });
        });
    }

    /**
     * In majorTextWindow, user can select a range of chars. This function return a list of index of those chars.
     * @return {Array} ["index string of the 1th selected char", "index string of the 2th selected char", ...]
     */
    function majorTextWindow_getSelectedIndexFromGui(){
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
            function idCompare(a, b){
                a = a.split('-').map(Number)
                b = b.split('-').map(Number)
                var r = 0;
                for (var i = 0; i < Math.min(a.length,b.length); i++)
                {
                    if (a[i] != b[i]){
                        r = (a[i] > b[i]);
                        break;
                    }
                }
                if ((r == 0) && (a.length == b.length)){
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
            for (i=0; i<selectedElements.length; i++){
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
    function majorTextWindow_getSelectedElementFromIndex(selectedElementIndexList){
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
    function majorTextWindow_hightlightElement(elementList){
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
    function majorTextWindow_setCurArticleNodePosition(curNodePosition){
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
    function majorTextWindow_getCurArticleNodePosition(){
         let majorTextWindow = $("#textTab1");
         return majorTextWindow.attr("name");
     }
    /**
     *
     * @param data The Array of every chair
     * @param scroll
     */
    function majorTextWindow_updateText(data, scroll){
        let majorTextWindow = $("#textTab1");
        majorTextWindow.empty();
        // add html element for each char.
        for (i=0; i<data.length; i++){
            let elementText = "";
            elementText += "<div " +
                                "id=" + data[i]["position"] +
                                " " +
                                "class='char'" +
                            ">";
            if (data[i]["char"] === "\n"){
                elementText += "<div>\\n</div> ";
                elementText += "</div>";
                elementText += "<br style='clear:both;'>";
            }
            else if (data[i]["char"] ==="\r"){
                elementText += "<div>\\r</div>";
                elementText += "</div>";
                elementText += "<br style='clear:both;'>";
            }
            else if (data[i]["char"] === " "){
                elementText += "<div>&nbsp; <div>";
                elementText += "</div>";
            }
            else{
                elementText += "<div>" + data[i]["char"] + "</div>";
                elementText += "</div>";
            }
            let charElement = $(elementText);
            //
            majorTextWindow.append(charElement);
        }
    }
    function majorTextWindow_show(){
        $("#ui-id-1").click();
    }

    function minorTextWindow_updateText(data, scroll){

    }
    function minorTextWindow_show(){
        $("#ui-id-2").click();
    }

    function nodeInfoWindow_showNoSelect(){
        $("#nodeInfo-noSelect").css("display", "block");
        $("#nodeInfo-noNode").css("display", "none");
        $("#nodeInfo-selectedNode").css("display", "none");
    }
    function nodeInfoWindow_showNoNode(){
        $("#nodeInfo-noSelect").css("display", "none");
        $("#nodeInfo-noNode").css("display", "block");
        $("#nodeInfo-selectedNode").css("display", "none");
    }
    function nodeInfoWindow_showNodeInfo() {
        $("#nodeInfo-noSelect").css("display", "none");
        $("#nodeInfo-noNode").css("display", "none");
        $("#nodeInfo-selectedNode").css("display", "block");
    }
    function nodeInfoWindow_addLabels(){
        // add positionObj <div>
        let positionObj = nodeInfoWindow_generatePositionObj()
        $("#nodeInfo-selectedNode").append(positionObj);
        // add labels
        for(let curLabelIndex=0; curLabelIndex<labelSysDict["node"].length; curLabelIndex++){
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
    function nodeInfoWindow_showCannotAddNode(){
        alert(langDict["can not add node based on current mention."])
    }
    function nodeInfoWindow_generatePositionObj(position){
        let positionObj = $(" <div id='nodeInfo-position'></div>");
        positionObj.css("padding-left","10px");
        // keyObj <span>
        let keyObj = $("<span id='positionKey'>position: </span>");
        positionObj.append(keyObj);
        // valueObj <span>
        let valueObj = $("<span id='positionValue'></span>");
        let innerText = undefined;
        // if given a value, display the value
        if (position != undefined) {
            innerText = position;
        }else{
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
    function nodeInfoWindow_updateNodeInfo(nodeInfo){
        // update position
            // get the position data ready
            let position = nodeInfo["position"];
            // generate new positionObj
            let positionObj = nodeInfoWindow_generatePositionObj(position);
            // replace the old label obj
            $("#nodeInfo-position").replaceWith(positionObj);
        // update labels
        for(let curLabelIndex=0; curLabelIndex<labelSysDict["node"].length; curLabelIndex++){
            // get the label data ready
            let curLabelConfig = labelSysDict["node"][curLabelIndex];
            let newValue = undefined;
            if(curLabelConfig["key"] in nodeInfo) {
                newValue = nodeInfo[curLabelConfig["key"]];
            }
            // generate a new label obj based on new value
            let curLabelTypeDict = labelTemplate[curLabelConfig["value_type"]];
            let labelObj = curLabelTypeDict["generateLabelObj_func"](curLabelConfig, newValue);
            // replace the old label obj
            $("#nodeInfo-" + curLabelConfig["key"]).replaceWith(labelObj);
        }
    }
    function nodeInfoWindow_refresh(){
        if ($("#nodeInfo-selectedNode").css("display") == "block"){
            // prepare ajax data
            let nodePosition = $("#positionValue").text();
            // ajax to background
            let nodeInfo = getNodeByPosition(nodePosition);
            // display the new node info in GUI
            if (nodeInfo === "") {
                nodeInfoWindow_showNoNode();
            } else {
                nodeInfoWindow_updateNodeInfo(nodeInfo);
            }
        }
    }
        // if(nodeInfo["position"]){
        //     $("#pathValue")[0].textContent = nodeInfo["position"]
        // }else{
        //     $("#pathValue")[0].textContent = ""
        // }
        // if(nodeInfo["token"]){
        //     $("#tokenValue").children()[0].checked = true
        // }else{
        //     $("#tokenValue").children()[1].checked = true
        // }
        // if(nodeInfo["semanticType"]){
        //     $("#semanticTypeValue option[value="+ nodeInfo["semanticType"] +"]")[0].selected = true
        // }else{
        //     $("#semanticTypeValue option[value='none']")[0].selected = true
        // }
        // if(nodeInfo["instance"]){
        //     nodeInstance = $("#instanceValue");
        //     nodeInstance.text(nodeInfo["instance"]["desc"]);
        //     nodeInstance.attr("name", nodeInfo["instance"]["id"]);
        //     nodeInstance.addClass("instance");
        //     nodeInstance.click(function(){
        //         if(clickFlag) {//取消上次延时未执行的方法
        //             clickFlag = clearTimeout(clickFlag);
        //         }
        //         curSelectedInstance = this;
        //         clickFlag = setTimeout(function(){
        //             instanceClick();
        //         }, 150);//延时300毫秒执行
        //     })
        // }else{
        //     nodeInstance = $("#instanceValue");
        //     nodeInstance.text("none");
        //     nodeInstance.attr("name", "");
        //     nodeInstance.removeClass("instance");
        //     nodeInstance.click(function(){});
        // }

    function instanceSelectWindow_updateOneInstance(data){
        // 删除旧节点
        instanceSelectWindow_delOneInstanceObj(data);
        // 创建新节点
        let newInstanceObj = instanceSelectWindow_createOneInstanceObj(data);
        // 添加新节点
        $("#allInstanceDiv").prepend(newInstanceObj);
    }
    /**
     * 创建新的instance元素(包括属性和事件)
     * @param {Object} data : {"id": , "desc":"xxxx"}
     * @returns {jQuery.HTMLElement}
     */
    function instanceSelectWindow_createOneInstanceObj(data){
        // 建元素
        let newInstanceObj = $("<button></button>");
        // 加属性
        newInstanceObj.attr('name', data['id']);
        newInstanceObj.addClass('instance');
        if (data['desc'] !== undefined){
            if (data['desc'] !== "") {
                newInstanceObj.text(data['desc']);
            }else{
                newInstanceObj.text('　');
            }
        } else {
            newInstanceObj.text(labelSysDict["instance"][1]["value_default"]);  //[1]是desc标签的描述数组
        }
        // 挂事件
        newInstanceObj.click(function() {
            let instanceIdStr = this.name;
            let instanceInfo = getInstanceById(instanceIdStr);
            instanceInfoWindow_updateInstanceInfo(instanceInfo);
            instanceInfoWindow_showInstanceInfo();
            instanceSelectWindow_updateOneInstance(instanceInfo);
        })
        //
        return newInstanceObj
    }
    /**
     *
     * @param {Object} data: {"id"}
     */
    function instanceSelectWindow_delOneInstanceObj(data){
        let oldInstanceObj = $("#allInstanceDiv [name=" + data['id'].toString() + "]")
        if (oldInstanceObj.length > 0 ){oldInstanceObj.remove();}
    }

    function instanceInfoWindow_showInstanceInfo(){
        $("#instanceInfo-noInstance").css("display", "none");
        $("#instanceInfo-selectedInstance").css("display", "block");
    }
    function instanceInfoWindow_showNoInstance(){
         $("#instanceInfo-noInstance").css("display", "block");
        $("#instanceInfo-selectedInstance").css("display", "none");
    }
    function instanceInfoWindow_addLabels(){
        for(let curLabelIndex=0; curLabelIndex<labelSysDict["instance"].length; curLabelIndex++){
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
    function instanceInfoWindow_updateInstanceInfo(instanceInfo){
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
        for(curLabelIndex=0; curLabelIndex<labelSysDict["instance"].length; curLabelIndex++){
            // get the label data ready
            let curLabelDict = labelSysDict["instance"][curLabelIndex];
            let newValue = undefined;
            if(curLabelDict["key"] in instanceInfo) {
                newValue = instanceInfo[curLabelDict["key"]];
            }else{
                newValue = undefined;
            }
            let curLabelTypeDict = labelTemplate[curLabelDict["value_type"]];
            // generate a new label obj based on new value
            let labelObj = curLabelTypeDict["generateLabelObj_func"](curLabelDict, newValue);
            // replace the old label obj
            $("#nodeInfo-" + curLabelDict["key"]).replaceWith(labelObj);
        }
    }
    function instanceInfoWindow_refresh(){
        if ($("#instanceInfo-selectedInstance").css("display") == "block"){
            // prepare ajax data
            let instanceId = $("#idValue").text();
            // ajax to background
            let instanceInfo = getInstanceById(instanceId);
            // display the new instance info in GUI
            if (instanceInfo === "") {
                instanceInfoWindow_showNoInstance();
            } else {
                instanceInfoWindow_updateInstanceInfo(instanceInfo);
            }
        }
    }

// <!-- flask interface -->
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
        }
        $.post(
            "/getText",
            {
                textNodeId: nodePosition,
            },
            function (data, status) {
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
        $.post(
            "/getCatalogue",
            { },
            function (data, status) {
                contentInfo = data;
            }
        );
        return contentInfo;
    }
    /**
     * flask interface. Given the position of a node, request the info of the node.
     *
     * @param nodePosition {string} Position string of the node.
     * @param callback {function} The call back function.
     *   The return value *data* of the POST request is given as the first param of the call back function.
     */
    function getNodeByPosition(nodePosition, callback){
        let nodeInfo = undefined;
        $.post(
            "/getNode",
            {
                position: nodePosition,
            },
            function (data, status) {
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
     * @param callback {function} The call back function.
     *   The return value *data* of the POST request is given as the first param of the call back function.
     */
    function getNodeByChildren(startNodePosition, endNodePosition, callback){
        $.post(
            "/getNode",
            {
                start: startNodePosition,
                end: endNodePosition
            },
            function (data, status) {
                callback(data);
            }
        );
    }
    function setNode(position, newValueDict){
        let nodeInfo = undefined;
        newValueDict["position"] = position;
        $.post(
            "/setNode",
            newValueDict,
            function (data, status) {
                nodeInfo = data;
            }
        )
        return nodeInfo;
    }
    function addNodeByChildren(childrenNodePositionList){
        let r = undefined
        $.post(
            "/addNode",
            {
                childrenNodePositionList: childrenNodePositionList
            },
            function (data, status) {
                r = data
            }
        );
        if (r[0] == "success"){
            r[1] = PythonStyleToJsStyle(r[1])
        }
        return r
    }
    function getInstanceById(id){
        let r = undefined;
        $.post(
            "/getInstance",
            {instance_id: id},
            function (data, status) {
                // instanceInfoWindow_showInstanceInfo(data);
                // instanceSelectWindow_updateOneInstance(data);
                r = data;
            }
        );
        return r
    }
    function setInstance(instanceId, newValueDict){
        let instanceInfo = undefined;
        newValueDict["id"] = instanceId;
        $.post(
            "/setInstance",
            newValueDict,
            function (data, status) {
                instanceInfo = data;
            }
        )
        return instanceInfo;
    }
    function addInstance_empty(){
        let instanceInfo = undefined;
        $.post(
            "/addInstance",
            {},
            function (data, status) {
                instanceInfo = data;
            }
        )
        return instanceInfo;
    }
    function addInstance_node(callback){
        $.post(
            "/addInstance",
            {
                "position": $("#positionValue").text()
            },
            function (data, status) {
                callback(data);
            }
        )
    }
    function save(){
       $.post(
           "/save",
           {},
           function(data, status){
               if (data["success"] == true){
                   alert(langDict["saved success!"])
               }
           }
       )
    }

// <!-- evnet logic -->
//     function startOfInstanceSlotFilling(){
//     }
//     function endOfInstanceSlotFilling(){
//         // 数据准备
//         var slot = curTriggerInstanceSlot;
//         if (slot.parentElement.parentElement.getAttribute("id") === "nodeInfoWindow"){
//             var slotType = "node";
//             var position = $("#positionValue").text();
//         }
//         newInstanceId = curSelectedInstance.name;
//         // 向后台传数据
//         if (slotType === "node"){
//             setNode(position,{"instance":newInstanceId});
//         } else if (slotType === "instance"){
//             setInstance()
//         }
//         // 取消当前solt的待选特效
//         curTriggerInstanceSlot.classList.remove("curSlot");
//         document.body.style.cursor = "";
//         //
//         curTriggerInstanceSlot = undefined
//         // 更新instance info
//         if (curSelectedInstance != undefined){
//             getInstanceById(curSelectedInstance.name);
//         }
//     }

    // textWindow: 选中一段文本
    function textMouseup(){
        let slotNum = $(".slot").length
        // just select a mention
        if (slotNum == 0){
            // 清除上次的选区效果
            if (SelectedElementIndexList !== undefined) {
                let selectedElementsBefore = majorTextWindow_getSelectedElementFromIndex(SelectedElementIndexList);
                for (let i = 0; i < selectedElementsBefore.length; i++) {
                    selectedElementsBefore[i][0].style = "color: black";
                }
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
                getNodeByChildren(
                    selectedElementsNow[0].attr("id"),
                    selectedElementsNow[selectedElementsNow.length-1].attr("id"),
                    function(data){
                        // 区分是否为标注对象
                        if (data === "") {
                            nodeInfoWindow_showNoNode();
                        } else {
                            nodeInfoWindow_updateNodeInfo(data);
                            nodeInfoWindow_showNodeInfo();
                        }
                    }
                )
            }
        }
        // select a mention, get the corresponding node, and fill current slot with the node.
        else if(slotNum == 1){
            // 获取这次的选区，并更新全局变量
            let curSelectedIndex = majorTextWindow_getSelectedIndexFromGui();
            // 如果没选中任何内容
            if (curSelectedIndex === undefined) {
                return
            }
            // 如果选中了某些内容
            else {
                // 把选区的index转换成element，因为用起来方便
                let selectedElements = majorTextWindow_getSelectedElementFromIndex(curSelectedIndex);
                // 选中效果
                    // r = $(".slot").update(selectedElements)
                    let r =1
                // 请求注释信息，并显示
                if (r == "success"){
                    // 取消鼠标特效
                    // 刷新
                    nodeInfoWindow_refresh()
                    instanceInfoWindow_refresh()
                }
            }

        }else{
            alert(langDict["Error: More than one slots are to be filled."])
        }

    }

    // nodeInfoWindow: 单击“添加标注对象”按钮
    function addNodeButtonClick(){
        // 当前有选中某个指称
        if(SelectedElementIndexList !== undefined){
            // 把选区的index转换成position（因为flask接口要求position）
            let selectedElementPositionList = [];
            let selectedElement = majorTextWindow_getSelectedElementFromIndex(SelectedElementIndexList);
            for (let i=0; i<selectedElement.length; i++){
                selectedElementPositionList[i] = selectedElement[i].attr("id");
            }
            // 向后台发送操作请求
            let r = addNodeByChildren(selectedElementPositionList);
            // 区分是否为标注对象
            if (r[0] != "success"){
                nodeInfoWindow_showCannotAddNode();
                alert(langDict[r[1]])
            }else {
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
                if (SelectedElementIndexList != undefined){
                    let selectedElement = majorTextWindow_getSelectedElementFromIndex(SelectedElementIndexList);
                    majorTextWindow_hightlightElement(selectedElement);
                }

            }
        }
        // 当前没有选中任何指称
        else{
            alert(langDict["Can not create node, because no mention is selected."]);
        }
    }
    // nodeInfoWindow: 标注信息变动（token）
    function nodeTokenChange(){
        var position = $("#positionValue").text();
        var tokenValue = $("#tokenValue :checked").attr("value");
        if (tokenValue === "false"){
            tokenValue = false;
        }else if(tokenValue === "true"){
            tokenValue = true;
        }else{
            alert("搞笑")
        }
        let r = setNode(position, {"token": tokenValue});
        if (r != "success"){
            alert(langDict[r]);
            return;
        }
        // refresh nodeInfoWindow
        nodeInfoWindow_refresh();
        // refresh instanceInfoWindow
        instanceInfoWindow_refresh();
    }
    // nodeInfoWindow: 标注信息变动（semanticType）
    function nodeSemanticTypeChange(){
        var position = $("#positionValue").text();
        var semanticTypeValue = $("#semanticTypeValue :checked").attr("value");
        let r = setNode(position, {"semanticType": semanticTypeValue});
        if (r != "success"){
            alert(langDict[r]);
            return;
        }
        // refresh nodeInfoWindow
        nodeInfoWindow_refresh();
        // refresh instanceInfoWindow
        instanceInfoWindow_refresh();
    }

    // // 单击实例
    // function instanceSlotClick(){
    //     if (curTriggerInstanceSlot === undefined){
    //         // 显示实例信息
    //         if (curSelectedInstance.name == ""){
    //             // alert("no instance.")
    //         }else{
    //             getInstanceById(curSelectedInstance.name);
    //         }
    //     }
    //     /y
    // }
    // // 双击实例槽
    // function instanceSlotShiftClick(){
    //     startOfInstanceSlotFilling();
    // }

    // instanceSelectWindow: 单击“+”按钮
    function addInstancePlusButtonClick(){
        // ajax to background
        let instanceInfo = addInstance_empty();
        // add instance obj in instanceSelectWindow
        instanceSelectWindow_updateOneInstance(instanceInfo);
        // show instance info in nstanceInfoWindow
        instanceInfoWindow_showInstanceInfo();
        instanceInfoWindow_updateInstanceInfo(instanceInfo);
    }
    // instanceSelectWindow: 单击“→”按钮
    function addInstanceArrowButtonClick(){
        // 如果curNode不存在
        if ($("#nodeInfo-path").css("display") == "none"){
            // 如果有选中一个mention，只差创建node
            if ($("#nodeInfo-noNode").css("display") == "block"){
                $("#nodeInfo-noNode").click();
            }
            // 如果连mention都没选
            else{
                alert(langDict["you should select a mention at first."]);
                return;
            }
        }
        // 如果curNode存在
            // 如果curNode已指向一个instance
            if($("#instanceValue").attr("name") !== ""){

                // if (allowOneNodeReferToMultiInstances == False){
                //     alert(langDict["Current node is already referenced to a instance, " +
                //         "You can't add a new instance based on current node, because this action will make one node " +
                //         "reference to two different instance."]);
                //     return;
                // }
            }
            // curNode也没有指向instance
            addInstance_node(
                function (data) {
                    instanceInfoWindow_showInstanceInfo(data);
                    instanceSelectWindow_updateOneInstance(data);
                    //
                    nodeInstance = $("#instanceValue");
                    nodeInstance.attr("name", data["id"]);
                    if (data["desc"]){
                        nodeInstance.text(data["desc"]);
                    }else{
                        nodeInstance.text("none");
                    }
                }
            )
    }
    // // instanceSelectWindow: 单击实例
    function instanceClick(instanceElement){
        let isHaveInstanceSlotActive = undefined;
        if ($(".curInstanceSlot").length == 0){
            isHaveInstanceSlotActive = false;
        }else{
            isHaveInstanceSlotActive = true;
        }

        // 用此实例填充槽
        if (isHaveInstanceSlotActive){
            // 数据准备
            var slot = curTriggerInstanceSlot;
            let instanceSlot = $(".curInstanceSlot");
            if (slot.parentElement.parentElement.getAttribute("id") === "nodeInfoWindow"){
                var slotType = "node";
                var position = $("#positionValue").text();
            }
            newInstanceId = curSelectedInstance.name;
            // 向后台传数据
            if (slotType === "node"){
                let r = setNode(position,{"instance":newInstanceId});
                if (r != "success"){
                    alert(langDict[r]);
                    return;
                }
                // refresh nodeInfoWindow
                nodeInfoWindow_refresh();
                // refresh instanceInfoWindow
                instanceInfoWindow_refresh();
            } else if (slotType === "instance"){
                let r = setInstance();
                if (r != "success"){
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
            if (curSelectedInstance != undefined){
                getInstanceById(curSelectedInstance.name);
            }
        }
        // 展示实例
        else{
            let instanceIdStr = instanceElement.name;
            let instanceInfo = getInstanceById(instanceIdStr);
            instanceInfoWindow_showInstanceInfo(instanceInfo);
            instanceSelectWindow_updateOneInstance(instanceInfo);
        }
    }

    // // instanceInfoWindow: desc变动
    // function instanceDescChange(){
    //     var id = $("#idValue").text()
    //     var descValue = $("#descValue")[0].value
    //     setInstance(
    //         id,
    //         {"desc": descValue},
    //         function(data){
    //             instanceInfoWindow_showInstanceInfo(data);
    //             instanceSelectWindow_updateOneInstance(data);
    //             if ($("#nodeInfo-path").css("display") == "block"){
    //                 getNodeByPosition(
    //                     $("#pathValue").text(),
    //                     function(data){
    //                         nodeInfoWindow_showNodeInfo(data);
    //                     }
    //                 )
    //             }
    //         }
    //     )
    // }
    // // instanceInfoWindow: kg变动
    // function instanceKgChange(){
    //     var id = $("#idValue").text()
    //     var kgValue = $("#kgValue")[0].value
    //     setInstance(id, {"kg": kgValue})
    // }
    // // instanceInfoWindow: 单击mentionList中"→"按钮
    // /**
    //  * click "extent mention list( based on cur node）" button
    //  *
    //  * @param instanceId {string} id string of the instance to which the mention list belongs.
    //  * @param mentionListIndex {string} index string of the mention list to which the button belongs.
    //  */
    // function extentMentionListButtonClick(instanceId, mentionListIndex){
    //     if ($("#nodeInfo-path").css("display") == "block"){
    //         curNodePosition = $("#pathValue").text()
    //         setInstance(
    //             instanceId,
    //             {
    //                 "mention_list":{
    //                     "action": "extent",
    //                     "mention_list_index": mentionListIndex,
    //                     "new_node_position": curNodePosition
    //                 }
    //             },
    //             function (data) {
    //                 if (typeof data == "string"){
    //                     alert(langDict["set instance fail."]);
    //                 }
    //                 else if (typeof data == "object"){
    //                     instanceInfoWindow_showInstanceInfo(data);
    //                 }
    //             }
    //         )
    //     }
    // }
    // // instanceInfoWindow: 单击mentionLists中"+"按钮
    // /**
    //  * click "add mention list" button
    //  *
    //  *  @param instanceId {string} id string of the instance.
    //  */
    // function addMentionListButtonClick(instanceId){
    //     setInstance(
    //         instanceId,
    //         {
    //             "mention_list":{
    //                 "action": "add"
    //             }
    //         },
    //         function(data){
    //             if (typeof data == "string"){
    //                 alert(langDict["set instance fail."]);
    //             }
    //             else if (typeof data == "object"){
    //                 instanceInfoWindow_showInstanceInfo(data);
    //             }
    //         }
    //     )
    // }

    // wholeSystem: ctrl+s
    function ctrls(){
        save();
    }

