// 全局变量。用于单击实例和双击实例的计时器
var clickFlag = null;
// 全局变量。array of html elements。选中的文本所对应的元素的数组。
var selectedElements = 0
// 全局变量。记录正在填充的实例槽。
var curTriggerInstanceSlot = undefined;
// 全局变量。记录被选中的实例。
var curSelectedInstance = undefined;


// <!-- ui interface -->
    /** In major text window, update char elements.
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
            $("#instanceValue")[0].textContent = nodeInfo["instance"]["desc"];
            $("#instanceValue")[0].name = nodeInfo["instance"]["id"];
            $("#instanceValue").addClass("instance");
        }else{
            $("#instanceValue").text("none");
            $("#instanceValue").name = undefined;
            $("#instanceValue").removeClass("instance");
        }
        $("#nodeInfo-noSelect").css("display", "none");
        $("#nodeInfo-noNode").css("display", "none");
        $("#nodeInfo-path").css("display", "block");
        $("#nodeInfo-token").css("display", "block");
        $("#nodeInfo-semanticType").css("display", "block");
        $("#nodeInfo-instance").css("display", "block");
    }

    function showCommonInstances(){}
    function showCannotAddNodeInfo(){
        alert("不行")
    }
    function showInstanceInfo(data){
        $("#idValue").text(data["id"]);
        $("#descValue").val(data["desc"]);
        if(data["kg"] !== undefined){
            $("#kgValue").val(data["kg"])
        }
        var mentionListsValue = $("#mentionListsValue");
        mentionListsValue.empty();
        for(var i=0;i<data["mention_list"].length;i++){
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

        // 单击“添加指称列表”按钮
        $("#instance_addMentionList_button").click(function(){
            instanceId = parseInt($("#idValue").text());
            addMentionListButtonClick(instanceId);
        });
        // 单击“扩展指称列表（基于当前节点）”按钮
        $(".instance_extentMentionList_button").click(function () {
            instanceId = parseInt($("#idValue").text());
            mentionListIndex = parseInt(this.name);
            extentMentionListButtonClick(instanceId, mentionListIndex);
        });
    }
    function updateInstanceButton(data){
        $("#allInstanceDiv [name=" + data['id'].toString() + "]").text(data['desc'])
    }
    function addToCommonInstanceTab(data){
        $("#commonInstanceDiv [name=" + data['id'].toString() + "]").remove();
        newInstanceButton = $("<button></button>");
        newInstanceButton.text(data['desc']);
        newInstanceButton.attr('name', data['id']);
        newInstanceButton.addClass('instance');
        $("#commonInstanceDiv").prepend(newInstanceButton);
    }

// <!-- flask interface -->
    /** flask interface. Given the position of a node, request the text of the node.
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
    /** flask interface. Given the position of a node, request the info of the node.
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
    /** flask interface. Given a range of nodes, check if those nodes correspond to a father node.
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
                    showCannotAddNodeInfo();
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
                showInstanceInfo(data);
                updateInstanceButton(data);
                addToCommonInstanceTab(data);
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
    function addInstance(){
        $.post(
            "/addInstance", {},
            function (data, status) {
                showInstanceInfo(data);
            }
        )
    }
    function addInstanceBasedOnCurNode(){
        selectedText = "";
        for (var i = 0; i < selectedElements.length; i++){
            selectedText += selectedElements[i].textContent;
        }
        curNodePosition = $("#pathValue").text();
        $.post(
            "/addInstance",
            {
                "desc": selectedText,
                "mention_list_new": curNodePosition,
            },
            function (data, status) {
                showInstanceInfo(data);
                alert("更新node信息")
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

    // 选中一段文本
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
    // 单击“添加标注对象”按钮
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
    // 双击实例
    function instanceDblclick(){
        startOfInstanceSlotFilling();
    }
    // 节点信息变动（token）
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
    // 节点信息变动（semanticType）
    function nodeSemanticTypeChange(){
        var position = $("#pathValue").text();
        var semanticTypeValue = $("#semanticTypeValue :checked").attr("value");
        setNode(position, {"semanticType": semanticTypeValue});
    }
    // 实例信息变动(desc)
    function instanceDescChange(){
        var id = $("#idValue").text()
        var descValue = $("#descValue")[0].value
        setInstance(
            id,
            {"desc": descValue},
            function(data){
                showInstanceInfo(data);
                updateInstanceButton(data);
                addToCommonInstanceTab(data);
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
    // 实例信息变动(kg)
    function instanceKgChange(){
        var id = $("#idValue").text()
        var kgValue = $("#kgValue")[0].value
        setInstance(id, {"kg": kgValue})
    }
    // 单击“添加实例”按钮
    function addInstanceClick(){
        addInstance();
    }
    // 单击“添加实例（基于当前节点）”按钮
    function addInstanceBasedOnCurNodeClick(){
        addInstanceBasedOnCurNode()
    }


    /** click "extent mention list( based on cur node）" button
     * @param instanceId {number} id of the instance to which the mention list belongs.
     * @param mentionListIndex {number} index of the mention list to which the button belongs.
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
                }
            )
        }
    }

    /** click "add mention list" button
     *
     */
    function addMentionListButtonClick(instanceId){
        setInstance(
            instanceId,
            {
                "mention_list":{
                    "action": "add"
                }
            }
        )
    }
