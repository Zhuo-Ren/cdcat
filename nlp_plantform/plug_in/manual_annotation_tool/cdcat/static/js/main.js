// 全局变量。用于单击实例和双击实例的计时器
var clickFlag = null;
// 全局变量。array of html elements。选中的文本所对应的元素的数组。
var selectedElements = 0
// 全局变量。记录正在填充的实例槽。
var curTriggerInstanceSlot = undefined;
// 全局变量。记录被选中的实例。
var curSelectedInstance = undefined;


// <!-- ui interface -->
    /**
     *  In contentWindow, scroll to the given element.
     *
     */
    function contentWindow_scroll(){}
    /**
     * In contentWindow, set content based on *contentArray*.
     */
    function contentWindow_updateContent(contentArray){
        //
        contentWindow = $("#contentWindow")
        contentWindow.empty();
        // 创建根目录
        var contentRoot = $("<ul></ul>");
        contentRoot.attr("id", "browser");
        contentRoot.addClass("filetree");
        contentWindow.append(contentRoot);
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
            curSpan = $("<span></span>")
            positionString = contentArray[0];
            if (positionString === ""){
                index = "root";
            }else{
                positionList = positionString.split("-");
                index = positionList[positionList.length - 1];
            }
            if (flag1 && flag2){
                // 当前是叶子节点（文件）
                curSpan.html(index + ": " + contentArray[1]);
                curSpan.addClass("file");
            } else{
                // 当前是枝干节点（文件夹）
                curSpan.html(index);
                curSpan.addClass("folder");
            }
            curSpan.attr("id", contentArray[0]);
            let curUl = $("<ul></ul>");
            curLi.append(curSpan);
            curLi.append(curUl);
            parentUl.append(curLi);
            // 遍历直接孩子
            if (! isLeaf){
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
        // 为目录添加单击事件
        $("#contentWindow span").click(function(){
            getText(
                this.id,
                function (data) {
                    majorTextWindow_updateText(data, 0);
                    majorTextWindow_show(data);
                }
            );
        });
    }

    /**
     * In major text window, update char elements.
     *
     * @param data
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
                elementText += "<div>\\n<div> <br style='clear:both;'>";
            }
            if (data[i]["char"] ==="\r"){
                elementText += "<div>\\n<div> <br style='clear:both;'>";
            }
            if (data[i]["char"] === " "){
                elementText += "<div>&nbsp; <div>";
            }
            else{
                elementText += "<div>" + data[i]["char"] + "<div>";
            }
            elementText += "</div>";
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
        $("#nodeInfo-path").css("display", "none");
        $("#nodeInfo-token").css("display", "none");
        $("#nodeInfo-semanticType").css("display", "none");
        $("#nodeInfo-instance").css("display", "none");
    }
    function nodeInfoWindow_showNoNode(){
        $("#nodeInfo-noSelect").css("display", "none");
        $("#nodeInfo-noNode").css("display", "block");
        $("#nodeInfo-path").css("display", "none");
        $("#nodeInfo-token").css("display", "none");
        $("#nodeInfo-semanticType").css("display", "none");
        $("#nodeInfo-instance").css("display", "none");
    }
    function nodeInfoWindow_showNodeInfo(nodeInfo) {
        if(nodeInfo["position"]){
            $("#pathValue")[0].textContent = nodeInfo["position"]
        }else{
            $("#pathValue")[0].textContent = ""
        }
        if(nodeInfo["token"]){
            $("#tokenValue").children()[0].checked = true
        }else{
            $("#tokenValue").children()[1].checked = true
        }
        if(nodeInfo["semanticType"]){
            $("#semanticTypeValue option[value="+ nodeInfo["semanticType"] +"]")[0].selected = true
        }else{
            $("#semanticTypeValue option[value='none']")[0].selected = true
        }
        if(nodeInfo["instance"]){
            nodeInstance = $("#instanceValue");
            nodeInstance.text(nodeInfo["instance"]["desc"]);
            nodeInstance.attr("name", nodeInfo["instance"]["id"]);
            nodeInstance.addClass("instance");
            nodeInstance.click(function(){
                if(clickFlag) {//取消上次延时未执行的方法
                    clickFlag = clearTimeout(clickFlag);
                }
                curSelectedInstance = this;
                clickFlag = setTimeout(function(){
                    instanceClick();
                }, 150);//延时300毫秒执行
            })
        }else{
            nodeInstance = $("#instanceValue");
            nodeInstance.text("none");
            nodeInstance.attr("name", "");
            nodeInstance.removeClass("instance");
            nodeInstance.click(function(){});
        }
        $("#nodeInfo-noSelect").css("display", "none");
        $("#nodeInfo-noNode").css("display", "none");
        $("#nodeInfo-path").css("display", "block");
        $("#nodeInfo-token").css("display", "block");
        $("#nodeInfo-semanticType").css("display", "block");
        $("#nodeInfo-instance").css("display", "block");
    }
    function nodeInfoWindow_showCannotAddNodeInfo(){
        alert("不行")
    }

    function instanceSelectWindow_updateOneInstance(data){
        // 删除旧节点
        oldInstanceButton = $("#allInstanceDiv [name=" + data['id'].toString() + "]")
        if (oldInstanceButton){oldInstanceButton.remove();}
        // 创建新节点
        newInstanceButton = $("<button></button>");
        newInstanceButton.attr('name', data['id']);
        newInstanceButton.addClass('instance');
        if (data['desc'] !== ""){
            newInstanceButton.text(data['desc']);
        } else {
            newInstanceButton.text('　');
        }
        newInstanceButton.click(function(){
            if(clickFlag) {//取消上次延时未执行的方法
                clickFlag = clearTimeout(clickFlag);
            }
            curSelectedInstance = this;
            clickFlag = setTimeout(function(){
                instanceClick();
            }, 150);//延时300毫秒执行
        });
        // 添加新节点
        $("#allInstanceDiv").prepend(newInstanceButton);
    }

    function instanceInfoWindow_showInstanceInfo(data){
        $("#idValue").text(data["id"]);
        $("#descValue").val(data["desc"]);
        if(data["kg"] !== undefined){
            $("#kgValue").val(data["kg"])
        }
        var mentionListsValue = $("#mentionListsValue");
        mentionListsValue.empty();
        for(var i=0; i<data["mention_list"].length; i++){
            var curMention = data["mention_list"][i];
            var curMentionLine = $("<div class='instanceMentionDiv'></div>");
            curMentionLine.append($("<span>[</span>"));
            for (var j=0; j<curMention.length; j++){
                var curPart = curMention[j];
                curMentionLine.append($(
                    "<button" +
                        " name=\"" + curPart["position"]+ "\"" +
                    ">" +
                        curPart["text"] +
                    "</button>"
                ))
            }
            curMentionLine.append($("<button class='instance_extentMentionList_button' name=" + (i).toString() +">→</button>"));
            curMentionLine.append($("<span>]</span>"));
            mentionListsValue.append(curMentionLine)
        }
        mentionListsValue.append($("<button id='instance_addMentionList_button'>+</button>"));
        //
        $("#instanceInfo-noInstance").css("display", "none");
        $("#instanceInfo-id").css("display", "block");
        $("#instanceInfo-desc").css("display", "block");
        $("#instanceInfo-kg").css("display", "block");
        $("#instanceInfo-mentionLists").css("display", "block");

        // instanceInfoWindow: 单击mentionLists中"+"按钮
        $("#instance_addMentionList_button").click(function(){
            instanceId = $("#idValue").text();
            addMentionListButtonClick(instanceId);
        });
        // instanceInfoWindow: 单击mentionList中"→"按钮
        $(".instance_extentMentionList_button").click(function () {
            instanceId = $("#idValue").text();
            mentionListIndex = this.name;
            extentMentionListButtonClick(instanceId, mentionListIndex);
        });
    }

// <!-- flask interface -->
    /**
     * flask interface. Given the position of a node, request the text of the node.
     *
     * @param nodePosition {string} Position string of the node.
     * @param callback {function} The call back function.
     *   The return value *data* of the POST request is given as the first param of the call back function.
     */
    function getText(nodePosition, callback){
        $.post(
            "/getText",
            {
                textNodeId: nodePosition
            },
            function (data, status) {
                callback(data)
            }
        );
    }
    /**
     * flask interface. request the content of corpora.
     *
     * @param callback {function} The call back function.
     *   The return value *data* of the POST request is given as the first param of the call back function.
     */
    function getContent(callback){
        $.post(
            "/getContent",
            { },
            function (data, status) {
                callback(data)
            }
        );
    }
    /**
     * flask interface. Given the position of a node, request the info of the node.
     *
     * @param nodePosition {string} Position string of the node.
     * @param callback {function} The call back function.
     *   The return value *data* of the POST request is given as the first param of the call back function.
     */
    function getNodeByPosition(nodePosition, callback){
        $.post(
            "/getNode",
            {
                position: nodePosition,
            },
            function (data, status) {
                // 区分是否为标注对象
                if (data === "") {
                    nodeInfoWindow_showNoNode();
                } else {
                    callback(data);
                    // nodeInfoWindow_showNodeInfo(data);
                }
            }
        );
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
    function setNode(position, infoDict){
        infoDict["position"] = position;
        $.post(
            "/setNode", infoDict,
            function (data, status) {
                nodeInfoWindow_showNodeInfo(data);
            }
        )
    }
    function addNodeByChildren(childrenNodePositionList){
        $.post(
            "/addNode",
            {
                childrenNodePositionList: childrenNodePositionList
            },
            function (data, status) {
                // 区分是否为标注对象
                if (data === ""){
                    nodeInfoWindow_showCannotAddNodeInfo();
                }else{
                    // 显示标注信息
                    nodeInfoWindow_showNodeInfo(data);
                    // 重新加载文本
                    getText("#textTab1", "")
                }
            }
        );
    }
    function getInstanceById(id){
        $.post(
            "/getInstance",
            {instance_id: id},
            function (data, status) {
                instanceInfoWindow_showInstanceInfo(data);
                instanceSelectWindow_updateOneInstance(data);
            }
        );
    }
    function setInstance(id, infoDict, callback){
        infoDict["id"] = id;
        $.post(
            "/setInstance", infoDict,
            function (data, status) {
                callback(data);

            }
        )
    }
    function addInstance_empty(callback){
        $.post(
            "/addInstance",
            {},
            function (data, status) {
                callback(data);
            }
        )
    }
    function addInstance_node(callback){
        $.post(
            "/addInstance",
            {
                "position": $("#pathValue").text()
            },
            function (data, status) {
                callback(data);
            }
        )
    }

// <!-- evnet logic -->
    function startOfInstanceSlotFilling(){
        // 标红当前槽元素
        curTriggerInstanceSlot.classList.add("curSlot");
        document.body.style.cursor = "help";
    }
    function endOfInstanceSlotFilling(){
        // 数据准备
        var slot = curTriggerInstanceSlot;
        if (slot.parentElement.parentElement.getAttribute("id") === "nodeInfoWindow"){
            var slotType = "node";
            var position = $("#pathValue").text();
        }
        newInstanceId = curSelectedInstance.name;
        // 向后台传数据
        if (slotType === "node"){
            setNode(position,{"instance":newInstanceId});
        } else if (slotType === "instance"){
            setInstance()
        }
        // 取消当前solt的待选特效
        curTriggerInstanceSlot.classList.remove("curSlot");
        document.body.style.cursor = "";
        //
        curTriggerInstanceSlot = undefined
    }

    // textWindow: 选中一段文本
    function textMouseup() {
        // 清除上次的选区效果
        if (selectedElements !== 0) {
            for (var i = 0; i < selectedElements.length; i++) {
                selectedElements[i].style = "color: black";
            }
        }
        // 如果没选中任何内容
        if (window.getSelection().toString() === "") {
            nodeInfoWindow_showNoSelect()
        }
        // 如果选中了某些内容
        else {
            // 获取当前选区(如果有多个选取，那只管第一个)
            {
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
                    alert("获取文本选区的anchor元素出错")
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
                    alert("获取文本选区的curve元素出错")
                }
                // 识别anchor和curve的顺序，得到start和end
                if (startDiv.id > endDiv.id) {
                    t = endDiv;
                    endDiv = startDiv;
                    startDiv = t;
                }
                // 遍历选区，得到element列表
                selectedElements = new Array(0);
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
            }

            // 选中效果
            for (var i = 0; i < selectedElements.length; i++) {
                selectedElements[i].style = "color: red";
            }
            selected.empty();

            // 请求注释信息，并显示
            getNodeByChildren(
                selectedElements[0].id.toString(),
                selectedElements[selectedElements.length - 1].id.toString(),
                function(data){
                    // 区分是否为标注对象
                    if (data === "") {
                        nodeInfoWindow_showNoNode();
                    } else {
                        nodeInfoWindow_showNodeInfo(data);
                    }
                }
            )
        }
    }

    // nodeInfoWindow: 单击“添加标注对象”按钮
    function addNodeButtonClick(){
        if(selectedElements !== 0){
            // 获取选中的node的position list。
            var selectedElementsIdList = Array();
            for (i=0; i<selectedElements.length; i++){
                selectedElementsIdList[i] = selectedElements[i].id.toString()
            }
            // 向后台发送操作请求
            addNodeByChildren(selectedElementsIdList)
        }
    }
    // nodeInfoWindow: 标注信息变动（token）
    function nodeTokenChange(){
        var position = $("#pathValue").text();
        var tokenValue = $("#tokenValue :checked").attr("value");
        if (tokenValue === "false"){
            tokenValue = false;
        }else if(tokenValue === "true"){
            tokenValue = true;
        }else{
            alert("搞笑")
        }
        setNode(position, {"token": tokenValue});
    }
    // nodeInfoWindow: 标注信息变动（semanticType）
    function nodeSemanticTypeChange(){
        var position = $("#pathValue").text();
        var semanticTypeValue = $("#semanticTypeValue :checked").attr("value");
        setNode(position, {"semanticType": semanticTypeValue});
    }

    // 单击实例
    function instanceClick(){
        if (curTriggerInstanceSlot === undefined){
            // 显示实例信息
            getInstanceById(curSelectedInstance.name);
        }
        else{
            // 选择此实例填充当前槽
            endOfInstanceSlotFilling();
        }
    }
    // 双击实例槽
    function instanceDblclick(){
        startOfInstanceSlotFilling();
    }

    // instanceSelectWindow: 单击“+”按钮
    function addInstancePlusButtonClick(){
        addInstance_empty(
            function (data) {
                instanceInfoWindow_showInstanceInfo(data);
                instanceSelectWindow_updateOneInstance(data)
            }
        );
    }
    // instanceSelectWindow: 单击“→”按钮
    function addInstanceArrowButtonClick(){
        // 如果curNode不存在
        if ($("#nodeInfo-path").css("display") == "none"){
            alert("There is no current node, you can't add instance based on current node.");
        }
        // 如果curNode存在，但curNode已有instance
        else if ($("#instanceValue").attr("name") !== ""){
            alert("Current node is already referenced to a instance, " +
                "You can't add a new instance based on current node, because this action will make one node " +
                "reference to two different instance.");
        }
        // 如果curNode存在，curNode也没有instance
        else{
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

    }

    // instanceInfoWindow: desc变动
    function instanceDescChange(){
        var id = $("#idValue").text()
        var descValue = $("#descValue")[0].value
        setInstance(
            id,
            {"desc": descValue},
            function(data){
                instanceInfoWindow_showInstanceInfo(data);
                instanceSelectWindow_updateOneInstance(data);
                if ($("#nodeInfo-path").css("display") == "block"){
                    getNodeByPosition(
                        $("#pathValue").text(),
                        function(data){
                            nodeInfoWindow_showNodeInfo(data);
                        }
                    )
                }
            }
        )
    }
    // instanceInfoWindow: kg变动
    function instanceKgChange(){
        var id = $("#idValue").text()
        var kgValue = $("#kgValue")[0].value
        setInstance(id, {"kg": kgValue})
    }
    // instanceInfoWindow: 单击mentionList中"→"按钮
    /**
     * click "extent mention list( based on cur node）" button
     *
     * @param instanceId {string} id string of the instance to which the mention list belongs.
     * @param mentionListIndex {string} index string of the mention list to which the button belongs.
     */
    function extentMentionListButtonClick(instanceId, mentionListIndex){
        if ($("#nodeInfo-path").css("display") == "block"){
            curNodePosition = $("#pathValue").text()
            setInstance(
                instanceId,
                {
                    "mention_list":{
                        "action": "extent",
                        "mention_list_index": mentionListIndex,
                        "new_node_position": curNodePosition
                    }
                },
                function (data) {
                    if (typeof data == "string"){
                        alert("set instance fail.");
                    }
                    else if (typeof data == "object"){
                        instanceInfoWindow_showInstanceInfo(data);
                    }
                }
            )
        }
    }
    // instanceInfoWindow: 单击mentionLists中"+"按钮
    /**
     * click "add mention list" button
     *
     *  @param instanceId {string} id string of the instance.
     */
    function addMentionListButtonClick(instanceId){
        setInstance(
            instanceId,
            {
                "mention_list":{
                    "action": "add"
                }
            },
            function(data){
                if (typeof data == "string"){
                    alert("set instance fail.");
                }
                else if (typeof data == "object"){
                    instanceInfoWindow_showInstanceInfo(data);
                }
            }
        )
    }
