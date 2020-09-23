//label template
labelTemplate = {
    "radio": {
        "generateLabelObj_func":generateRadioLabelObj,
        "addUpdateValueFunc_func": function (labelDict) {
            return function (newValue) {
                // if (newValue != undefined){
                //     $("#" + labelDict["key"] + "Value input[value=" + newValue + "]")[0].checked = true;
                // }else{
                //     $("#" + labelDict["key"] + "Value input[value=" + labelDict["value_default"][1] + "]")[0].checked = true;
                // }
            }
        },
        "addEvent_func": function(labelDict){
            // $("#" + labelDict["key"] + "Value input").change(function() {
            //     if ($("#nodeInfoWindow")[0].contains(this)){
            //         let position = $("#positionValue").text();
            //         let value = $("#" + labelDict["key"] + "Value :checked").attr("value");
            //         setNode(position, {[labelDict["key"]]: value});
            //     }else if($("#instancInfoWindow")[0].contains(this)){
            //         let id = $("#idValue").text();
            //         let value = $("#" + labelDict["key"] + "Value :checked").attr("value");
            //         setInstance(id, {[labelDict["key"]]: value});
            //     }
            // });
        }
    },
    "checkbox":{
        "generateLabelObj_func": function(labelDict){
            return  $("<span>没实现</span>");
        },
        "addUpdateValueFunc_func": function (labelDict) {
            return function(newValue){
                alert("没实现")
            };
        }
    },
    "list-one":{
        "generateLabelObj_func": generateListOneLabelObj,
        "addUpdateValueFunc_func": function(labelDict) {
            return function(newValue){
                // if (newValue != undefined) {
                //     $("#" + labelDict["key"] + "Value option[value=" + newValue + "]")[0].selected = true;
                // }else{
                //     $("#" + labelDict["key"] + "Value option[value=" + labelDict["value_default"][1] + "]")[0].selected = true;
                // }
            };
        },
        "addEvent_func": function(labelDict){
            // $("#" + labelDict["key"] + "Value select").change(function() {
            //     if ($("#nodeInfoWindow")[0].contains(this)){
            //         var position = $("#positionValue").text();
            //         let value = $("#" + labelDict["key"] + "Value :checked").attr("value");
            //         setNode(position, {[labelDict["key"]]: value});
            //     }else if($("#instancInfoWindow")[0].contains(this)){
            //         var id = $("#pidValue").text();
            //         var value = $("#" + labelDict["key"] + "Value :checked").attr("value");
            //         setInstance(id, {[labelDict["key"]]: value});
            //     }
            // });
        }
    },
    "list-multi":{
        "generateLabelObj_func": function(labelDict){
            return  $("<span>没实现</span>");
        },
        "addUpdateValueFunc_func": function (labelDict) {
            return function(newValue){
                alert("没实现")
            };
        }
    },
    "text-readonly":{
        "generateLabelObj_func": generateTextReadonlyLabelObj,
        "addUpdateValueFunc_func": function (labelDict) {
            return function(newValue){
                // if (newValue != undefined){
                //     $("#" + labelDict["key"] + "Value")[0].textContent = newValue;
                // }else{
                //     $("#" + labelDict["key"] + "Value")[0].textContent = labelDict["value_default"];
                // }
            };
        },
        "addEvent_func": function(labelDict){
            $("#" + labelDict["key"] + "Value").change(function() {
            });
        }
    },
    "text-input":{
        "generateLabelObj_func": generateTextInputLabelObj,
        "addUpdateValueFunc_func": function (labelDict) {
            return function(newValue){
                // alert("没实现")
            };
        },
        "addEvent_func": function(labelDict){
            // $("#" + labelDict["key"] + "Value").change(function() {
            //     // if the changed label belongs to a node
            //     if ($("#nodeInfoWindow")[0].contains(this)){
            //         let position = $("#positionValue").text();
            //         let value = $("#" + labelDict["key"] + "Value")[0].value;
            //         setNode(position, {[labelDict["key"]]: value});
            //     }
            //     // if the changed label belongs to a instance
            //     else if($("#instancInfoWindow")[0].contains(this)){
            //         // prepare ajax data
            //         let id = $("#idValue").text();
            //         let value = $("#" + labelDict["key"] + "Value")[0].value;
            //         // ajax to background
            //         instanceInfo = setInstance(id, {[labelDict["key"]]: value});
            //         // display the new instance info in GUI
            //         instanceInfoWindow_updateInstanceInfo(instanceInfo);
            //         instanceInfoWindow_showInstanceInfo();
            //         instanceSelectWindow_updateOneInstance(instanceInfo);
            //
            //         // The change of instance may lead to a change of nodes, so we also update the current node.
            //         if ($("#nodeInfo-selectedNode").css("display") == "block"){
            //             // prepare ajax data
            //             let position = $("#pathValue").text();
            //             // ajax to background
            //             let nodeInfo = getNodeByPosition(position);
            //             // display the new node info in GUI
            //             if (nodeInfo === "") {
            //                 nodeInfoWindow_showNoNode();
            //             } else {
            //                 nodeInfoWindow_updateNodeInfo(nodeInfo);
            //                 nodeInfoWindow_showNodeInfo();
            //             }
            //         }
            //     }
            // });
        }
    },
    "instance":{
        "generateLabelObj_func": generateInstanceLabelObj,
        // function(labelDict){
        //     reStr =     " <div id='nodeInfo-" + labelDict["key"] + "'>" +
        //                 "   <span id='" + labelDict["key"] + "Key'>" + labelDict["GUI_name"] + "</span>" +
        //                 "   <span id='" + labelDict["key"] + "Value'> " +
        //                 "       <button class='instance' name=''>none</button>" +
        //                 "       <button class='circleButton'>x</button>" +
        //                 "   </span>" +
        //                 "   <button id='" + labelDict["key"] + "Arrow\' class='circleButton'>←</button>" +
        //                 "</div>";
        //     reObj = $(reStr);
        //     reObj.css("padding-left","10px");
        //     return reObj
        // },
        "addUpdateValueFunc_func": function (labelDict) {
            return function(newValue){
                // if(newValue != undefined){
                //     let label = $("#" + labelDict["key"] + "Value button.instance");
                //     label.text(newValue["desc"]);
                //     label.attr("name", newValue["id"]);
                //     // label.addClass("instance");
                //     // label.click(function(){
                //     //     if(clickFlag) {//取消上次延时未执行的方法
                //     //         clickFlag = clearTimeout(clickFlag);
                //     //     }
                //     //     curSelectedInstance = this;
                //     //     clickFlag = setTimeout(function(){
                //     //         instanceClick();
                //     //     }, 149);//延时300毫秒执行
                //     // })
                // }else{
                //     let label = $("#" + labelDict["key"] + "Value button.instance");
                //     label.text("none");
                //     label.attr("name", "");
                //     // nodeInstance.text("none");
                //     // nodeInstance.attr("name", "");
                //     // nodeInstance.removeClass("instance");
                //     // nodeInstance.click(function(){});
                // }
            };
        },
        "addEvent_func": function(labelDict){
            // $("#" + labelDict["key"] + "Value").click(function(e){
                // shift+click instance slot: select a new instance as value of the label
                // if (e.shiftKey == true){
                //     // curTriggerInstanceSlot = this;
                //     // 标红当前槽元素
                //     $(this).css("background", "red");
                //     // 添加class
                //     this.classList.add("curInstanceSlot");
                //     // 修改鼠标样式
                //     document.body.style.cursor = "help";
                // }
                // click instance slot: show instance info in the instanceInfoWindow
                // else{
                    // curSelectedInstance = this;
                    // if (this.name == ""){
                    //     // alert("no instance.")
                    // }else{
                    //     let instanceIdStr = this.name;
                    //     let instanceInfo = getInstanceById(instanceIdStr);
                    //     instanceInfoWindow_showInstanceInfo(instanceInfo);
                    //     instanceSelectWindow_updateOneInstance(instanceInfo);
                    // }
                // }
            // });
            // $("#" + labelDict["key"] + "Value Button.instance").click(function(e){
            //     let instanceIdStr = this.name;
            //     if (instanceIdStr == ""){
            //         alert(langDict["Can not view the info of this instance, because it is a empty instance."]);
            //     }else{
            //         let instanceInfo = getInstanceById(instanceIdStr);
            //         instanceInfoWindow_showInstanceInfo(instanceInfo);
            //         instanceSelectWindow_updateOneInstance(instanceInfo);
            //     }
            // });
            // $("#" + labelDict["key"] + "Value Button.circleButton").click(function(e){
            //    if (this.prev().name == ""){
            //        alert(langDict["Can not delete this value, because this value is already empty."]);
            //    }else{
            //        // 准备数据
            //        let curNodePosition = $("#pathValue").text();
            //        let newValueDict = {
            //            [labelDict["key"]]: ""
            //        }
            //        // 回传给后台
            //        let nodeInfo = setNode(curNodePosition, newValueDict);
            //        // 显示节点的最新信息
            //        nodeInfoWindow_updateNodeInfo(nodeInfo);
            //        nodeInfoWindow_showNodeInfo(nodeInfo);
            //
            //    }
            // });
            // $("#" + labelDict["key"] + "Arrow").click(function(e){
            //     // 准备数据
            //     let curNodePosition = $("#pathValue").text();
            //     let newValueDict = {
            //         [labelDict["key"]]: $("#idValue").text()
            //     }
            //     // 回传给后台
            //     let nodeInfo = setNode(curNodePosition, newValueDict);
            //     // 显示节点的最新信息
            //     nodeInfoWindow_updateNodeInfo(nodeInfo);
            //     nodeInfoWindow_showNodeInfo(nodeInfo);
            //     //
            //     // var slot = curTriggerInstanceSlot;
            //     // if (slot.parentElement.parentElement.getAttribute("id") === "nodeInfoWindow"){
            //     //     var slotType = "node";
            //     //     var position = $("#pathValue").text();
            //     // }
            //     // newInstanceId = curSelectedInstance.name;
            //     // // 向后台传数据
            //     // if (slotType === "node"){
            //     //     setNode(position,{"instance":newInstanceId});
            //     // } else if (slotType === "instance"){
            //     //     setInstance()
            //     // }
            //     // // 取消当前solt的待选特效
            //     // curTriggerInstanceSlot.classList.remove("curSlot");
            //     // document.body.style.cursor = "";
            //     // //
            //     // curTriggerInstanceSlot = undefined
            //     // // 更新instance info
            //     // if (curSelectedInstance != undefined){
            //     //     getInstanceById(curSelectedInstance.name);
            //     // }
            // });
        }
    },
    "instances":{
        "generateLabelObj_func": function(labelDict){
            return  $("<span>没实现</span>");
        },
        "addUpdateValueFunc_func": function (labelDict) {
            return function(newValue){
                alert("没实现")
            };
        }
    },
    "nodes": {
        "generateLabelObj_func": generateNodesLabelObj,
        // function(labelDict){
        //     reStr =     "<div id='nodeInfo-" + labelDict["key"] + "'>" +
        //                 "   <span id='" + labelDict["key"] + "Key'>" + labelDict["GUI_name"] + "</span>" +
        //                 "   <span id='" + labelDict["key"] + "Value'> " +
        //                 "       <button class='circleButton' name='addList'>x</button>" +
        //                 "   </span>" +
        //                 "   <button id='" + labelDict["key"] + "Arrow\' class='circleButton'>←</button>" +
        //                 "</div>";
        //     reObj = $(reStr);
        //     reObj.css("padding-left","10px");
        //     return reObj
        // },
        "addUpdateValueFunc_func": function (labelDict) {
            return function(newValue){
                // if(newValue != undefined){
                //     let label = $("#" + labelDict["key"] + "Value button.instance");
                //     label.text(newValue["desc"]);
                //     label.attr("name", newValue["id"]);
                //     // label.addClass("instance");
                //     // label.click(function(){
                //     //     if(clickFlag) {//取消上次延时未执行的方法
                //     //         clickFlag = clearTimeout(clickFlag);
                //     //     }
                //     //     curSelectedInstance = this;
                //     //     clickFlag = setTimeout(function(){
                //     //         instanceClick();
                //     //     }, 149);//延时300毫秒执行
                //     // })
                // }else{
                //     let label = $("#" + labelDict["key"] + "Value button.instance");
                //     label.text("none");
                //     label.attr("name", "");
                //     // nodeInstance.text("none");
                //     // nodeInstance.attr("name", "");
                //     // nodeInstance.removeClass("instance");
                //     // nodeInstance.click(function(){});
                // }
            };
        },
        "addEvent_func": function(labelDict){
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
            //                 // prepare ajax data
            //                 let position = $("#pathValue").text();
            //                 // ajax to background
            //                 let nodeInfo = getNodeByPosition(position);
            //                 // 区分是否为标注对象
            //                 if (data === "") {
            //                     nodeInfoWindow_showNoNode();
            //                 } else {
            //                     callback(data);
            //                     // nodeInfoWindow_showNodeInfo(data);
            //                 }
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

            // instanceInfoWindow: desc变动
            // $("#descValue").change(function () {
            //     instanceDescChange();
            // });

            // instanceInfoWindow: kg变动
            // $("#kgValue").change(function () {
            //     instanceKgChange();
            // });
            // instanceInfoWindow: 单击mentionList中"→"按钮

            // /**
            //  * click "extent mention list( based on cur node）" button
            //  *
            //  * @param instanceId {string} id string of the instance to which the mention list belongs.
            //  * @param mentionListIndex {string} index string of the mention list to which the button belongs.
            //  */
            // function extentMentionListButtonClick(instanceId, mentionListIndex){
            //     if ($("#nodeInfo-path").css("display") == "block"){
            //         curNodePosition = $("#positionValue").text()
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
            //                     instanceInfoWindow_showInstanceInfo();
            //                     instanceInfoWindow_updateInstanceInfo(data);
            //                 }
            //             }
            //         )
            //     }
            // }
            //
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
            //
            // // instanceInfoWindow: 单击mentionLists中"+"按钮
            // $("#instance_addMentionList_button").click(function(){
            //     instanceId = $("#idValue").text();
            //     addMentionListButtonClick(instanceId);
            // });
            // // instanceInfoWindow: 单击mentionList中"→"按钮
            // $(".instance_extentMentionList_button").click(function () {
            //     instanceId = $("#idValue").text();
            //     mentionListIndex = this.name;
            //     extentMentionListButtonClick(instanceId, mentionListIndex);
            // });
        }
    }
}

/**
 * This function generate a radio type label obj.
 *
 * @example
    let labelDict = {
        "key": "token",
        "GUI_name": "is the mention a token: ",
        "value_type": "radio",
        "value_option": [["中杯", "m"], ["大杯", "l"],["超大杯", "xl"]],
        "value_default": "m"
    };
    let labelValue = "xl";
    let labelObj = generateRadioLabelObj(labelDict, labelValue);
 *
 * @param {Array} labelDict **[Required]** Info of the label. Required items included "key", "GUI_name", "value_option".
 *   Optional items include "value_default".
 * @param {Array} labelValue **[Optional]** The value of this label. The generated obj will display the value if given, or
 *   display the default value in *labelDict* if not given.
 * @return {Jquery.HtmlElement}
 */
function generateRadioLabelObj(labelDict, labelValue) {
    // labelObj <div>
    let labelObj = $(" <div id='nodeInfo-" + labelDict["key"] + "'><div>");
    labelObj.css("padding-left","10px");
        // keyObj <span>
        let keyObj = $("<span id='" + labelDict["key"] + "Key'>" + labelDict["GUI_name"] + "</span>");
        labelObj.append(keyObj);
        // valueObj <span>
        let valueObj = $("<span id='" + labelDict["key"] + "Value'></span>");
            // optionObj <span><input type="radio" name="XXX" value="XXX">XXX</span>
            for (optionIndex = 0; optionIndex < labelDict["value_option"].length; optionIndex++) { curOption = labelDict["value_option"][optionIndex];
                curOptionObj = $("<input type = 'radio' name = '" + labelDict["key"] + "' value = '" + curOption[1] + "' /><span>"+curOption[0]+" </span>");
                // if given a value, display the value
                if (labelValue != undefined){
                    if (labelValue == curOption[1]){
                        curOptionObj[0].checked = true;
                    }
                // if no value given, display the default value
                }else if (labelDict["value_default"] != undefined){
                    if (labelDict["value_default"] == curOption[1]){
                        curOptionObj[0].checked = true;
                    }
                }
                valueObj.append(curOptionObj);
            }
        valueObj.change(function() {
            if ($("#nodeInfoWindow")[0].contains(this)){
                let position = $("#positionValue").text();
                let value = $("#" + labelDict["key"] + "Value :checked").attr("value");
                let r = setNode(position, {[labelDict["key"]]: value});
                if (r != "success"){
                    alert(langDict[r]);
                    return;
                }
                // refresh nodeInfoWindow
                nodeInfoWindow_refresh();
                // refresh instanceInfoWindow
                instanceInfoWindow_refresh();
            }else if($("#instancInfoWindow")[0].contains(this)){
                let id = $("#idValue").text();
                let value = $("#" + labelDict["key"] + "Value :checked").attr("value");
                // ajax to background
                let r = setInstance(id, {[labelDict["key"]]: value});
                if (r != "success"){
                    alert(langDict[r]);
                    return;
                }
                // refresh nodeInfoWindow
                nodeInfoWindow_refresh();
                // refresh instanceInfoWindow
                instanceInfoWindow_refresh();
            }
        });
        labelObj.append(valueObj);
    // return
    return labelObj
}

/**
 * This function generate a list-one type label obj.
 *
 * @example
 let labelDict = {
      "key": "type",
      "GUI_name": "type of the mention: ",
      "value_type": "list-one",
      "value_option": [["无", "none"],["人", "PEO"],["地", "LOC"],["行为", "ACT"],["组织", "ORG"],["物", "SUB"]],
      "value_default": "none"
    };
 let labelValue = "ORG";
 let labelObj = generateListOneLabelObj(labelDict, labelValue);
 *
 * @param {Array} labelDict **[Required]** Info of the label. Required items included "key", "GUI_name", "value_option".
 *   Optional items include "value_default".
 * @param {Array} labelValue **[Optional]** The value of this label. The generated obj will display the value if given, or
 *   display the default value in *labelDict* if not given.
 * @return {Jquery.HtmlElement}
 */
function generateListOneLabelObj(labelDict, labelValue){
    // labelObj <div>
    let labelObj = $(" <div id='nodeInfo-" + labelDict["key"] + "'></div>");
    labelObj.css("padding-left","10px");
        // keyObj <span>
        let keyObj = $("<span id='" + labelDict["key"] + "Key'>" + labelDict["GUI_name"] + "</span>");
        labelObj.append(keyObj);
        // valueObj <span>
        let valueObj = $("<span id='" + labelDict["key"] + "Value'></span>");
            //valueSelectObj <select>
            let selectObj = $("<select></select>");
                //optionObj <option>
                for (optionIndex = 0; optionIndex < labelDict["value_option"].length; optionIndex++){
                    let curOption = labelDict["value_option"][optionIndex];
                    let optionObj = $("<option value = '" + curOption[1] + "'>" + curOption[0] + "</option>");
                    // if given a value, display the value
                    if (labelValue != undefined) {
                        if (curOption[1] == labelValue){
                            optionObj[0].selected = true;
                        }
                    }
                    // if no value given, display the default value
                    else if (labelDict["value_default"] != undefined){
                        if (curOption[1] == labelDict["value_default"]){
                            optionObj[0].selected = true;
                        }
                    }
                    selectObj.append(optionObj);
                }
            valueObj.append(selectObj);
        valueObj.change(function() {
            if ($("#nodeInfoWindow")[0].contains(this)){
                var position = $("#positionValue").text();
                let value = $("#" + labelDict["key"] + "Value :checked").attr("value");
                let r = setNode(position, {[labelDict["key"]]: value});
                if (r != "success"){
                    alert(langDict[r]);
                    return;
                }
                // refresh nodeInfoWindow
                nodeInfoWindow_refresh();
                // refresh instanceInfoWindow
                instanceInfoWindow_refresh();
            }else if($("#instancInfoWindow")[0].contains(this)){
                // prepare ajax data
                var id = $("#pidValue").text();
                var value = $("#" + labelDict["key"] + "Value :checked").attr("value");
                // ajax to background
                let r = setInstance(id, {[labelDict["key"]]: value});
                if (r != "success"){
                    alert(langDict[r]);
                    return;
                }
                // refresh nodeInfoWindow
                nodeInfoWindow_refresh();
                // refresh instanceInfoWindow
                instanceInfoWindow_refresh();
            }
        });
        labelObj.append(valueObj);
    // return
    return labelObj
}

/**
 * This function generate a text-readonly type label obj.
 *
 * @example
 let labelDict = {
        "key": "position",
        "GUI_name": "position: ",
        "value_type": "text-readonly",
        "value_default": "XXXXX"
    };
 let labelValue = "0-0-1-2";
 let labelObj = generateTextReadonlyLabelObj(labelDict, labelValue);
 *
 * @param {Array} labelDict **[Required]** Info of the label. Required items included "key", "GUI_name". Optional items
 *   include "value_default".
 * @param {Array} labelValue **[Optional]** The value of this label. The generated obj will display the value if given, or
 *   display the default value in *labelDict* if not given.
 * @return {Jquery.HtmlElement}
 */
function generateTextReadonlyLabelObj(labelDict, labelValue){
    // labelObj <div>
    let labelObj = $(" <div id='nodeInfo-" + labelDict["key"] + "'></div>");
    labelObj.css("padding-left","10px");
        // keyObj <span>
        let keyObj = $("<span id='" + labelDict["key"] + "Key'>" + labelDict["GUI_name"] + "</span>");
        labelObj.append(keyObj);
        // valueObj <span>
        let valueObj = $("<span id='" + labelDict["key"] + "Value'></span>");
            let innerText = undefined;
            // if given a value, display the value
            if (labelValue != undefined) {
                innerText =  labelValue;
            }
            // if no value given, display the default value
            else if (labelDict["value_default"] != undefined){
                innerText = labelDict["value_default"];
            }
            // if no given value and no default value
            else{
                innerText = "";
            }
            valueObj.text(innerText);
        labelObj.append(valueObj);
    // return
    return labelObj
}

/**
 * This function generate a text-input type label obj.
 *
 * @example
 let labelDict = {
    "key": "desc",
    "GUI_name": "desc: ",
    "value_type": "text-input",
    "value_default": "XXXXX"
 };
 let labelValue = "埃航失事客机";
 let labelObj = generateTextInputLabelObj(labelDict, labelValue);
 *
 * @param {Array} labelDict **[Required]** Info of the label. Required items included "key", "GUI_name". Optional items
 *   include "value_default".
 * @param {Array} labelValue **[Optional]** The value of this label. The generated obj will display the value if given, or
 *   display the default value in *labelDict* if not given.
 * @return {Jquery.HtmlElement}
 */
function generateTextInputLabelObj(labelDict, labelValue){
    // labelObj <div>
        let labelObj = $(" <div id='nodeInfo-" + labelDict["key"] + "'></div>");
        labelObj.css("padding-left","10px");
        // keyObj <span>
            let keyObj = $("<span id='" + labelDict["key"] + "Key'>" + labelDict["GUI_name"] + "</span>");
            labelObj.append(keyObj);
        // valueObj <span>
            let valueObj = $("<input id='" + labelDict["key"] + "Value' type='text'></input>");
            labelObj.append(valueObj);
            // display the label value
                let inputText = undefined;
                // if given a value, display the value
                if (labelValue != undefined) {
                    inputText =  labelValue;
                }
                // if no value given, display the default value
                else if (labelDict["value_default"] != undefined){
                    inputText = labelDict["value_default"];
                }
                // if no given value and no default value
                else{
                    inputText = "";
                }
                valueObj.attr("value", inputText)
            // add change event
                valueObj.change(function() {
                    // if the changed label belongs to a node
                    if ($("#nodeInfoWindow")[0].contains(this)){
                        let position = $("#positionValue").text();
                        let value = $("#" + labelDict["key"] + "Value")[0].value;
                        let r = setNode(position, {[labelDict["key"]]: value});
                        if (r != "success"){
                            alert(langDict[r]);
                            return;
                        }
                        // refresh nodeInfoWindow
                        nodeInfoWindow_refresh();
                        // refresh instanceInfoWindow
                        instanceInfoWindow_refresh();
                    }
                    // if the changed label belongs to a instance
                    else if($("#instancInfoWindow")[0].contains(this)){
                        // prepare ajax data
                        let id = $("#idValue").text();
                        let value = $("#" + labelDict["key"] + "Value")[0].value;
                        // ajax to background
                        let r = setInstance(id, {[labelDict["key"]]: value});
                        if (r != "success"){
                            alert(langDict[r]);
                            return;
                        }
                        // refresh nodeInfoWindow
                        nodeInfoWindow_refresh();
                        // refresh instanceInfoWindow
                        instanceInfoWindow_refresh();
                        // The change of instance may lead to a change of nodes, so we also update the current node.
                        if ($("#nodeInfo-selectedNode").css("display") == "block"){
                            // prepare ajax data
                            let position = $("#positionValue").text();
                            // ajax to background
                            let nodeInfo = getNodeByPosition(position);
                            // display the new node info in GUI
                            if (nodeInfo === "") {
                                nodeInfoWindow_showNoNode();
                            } else {
                                nodeInfoWindow_updateNodeInfo(nodeInfo);
                                nodeInfoWindow_showNodeInfo();
                            }
                        }
                    }
                });


    // return
    return labelObj
}

/**
 * This function generate a instance type label obj.
 *
 * @example
 let labelDict = {
    "key": "refer",
    "GUI_name": "instance which the mention refer to: ",
    "value_type": "instance",
    "instance_label": "mention_list",
 };
 let labelValue = {"id": "1", "desc":"AAA"}; //"id" can be "1" or 1 or "".  "desc" can be "AAA" or "".
 let labelObj = generateTextInputLabelObj(labelDict, labelValue);
 *
 * @param {Array} labelDict **[Required]** Info of the label. Required items included "key", "GUI_name". Optional items
 *   include "value_default".
 * @param {Array} labelValue **[Optional]** The value of this label. The generated obj will display the value if given, or
 *   display the default value in *labelDict* if not given.
 * @return {Jquery.HtmlElement}
 */
function generateInstanceLabelObj(labelDict, labelValue){
    // labelObj <div>
        let labelObj = $(" <div id='nodeInfo-" + labelDict["key"] + "'></div>");
        labelObj.css("padding-left","10px");
        // keyObj <span>
            let keyObj = $("<span id='" + labelDict["key"] + "Key'>" + labelDict["GUI_name"] + "</span>");
            labelObj.append(keyObj);
        // valueObj <span>
            let valueObj = $("<span id='" + labelDict["key"] + "Value'></span>");
            labelObj.append(valueObj);
            // instanceButtonObj <button>
                let instanceButtonObj = $("<button class='instance' name=''></button>");
                valueObj.append(instanceButtonObj);
                // display the label value
                    let inputText = undefined;
                    let instanceId = undefined;
                    // if given a value, display the value
                    if (labelValue != undefined) {
                        if (labelValue["desc"]==""){
                            inputText = '　';
                        }else{
                            inputText =  labelValue["desc"];
                        }
                        instanceId = labelValue["id"];
                    }
                    // if no value given, display the default value
                    else if (labelDict["value_default"] != undefined){
                        if (labelDict["value_default"]["desc"]==""){
                            inputText = '　';
                        }else{
                            inputText = labelDict["value_default"]["desc"];
                        }
                        instanceId = labelDict["value_default"]["id"];
                    }
                    // if no given value and no default value
                    else{
                        inputText = '　';
                        instanceId = "";
                    }
                    instanceButtonObj.text(inputText);
                    instanceButtonObj.attr("name", instanceId);
                // add click event
                    instanceButtonObj.click(function(e){
                        let instanceIdStr = this.name;
                        if (instanceIdStr == ""){
                            alert(langDict["Can not view the info of this instance, because it is a empty instance."]);
                        }else{
                            let instanceInfo = getInstanceById(instanceIdStr);
                            instanceInfoWindow_showInstanceInfo();
                            instanceInfoWindow_updateInstanceInfo(instanceInfo);
                            instanceSelectWindow_updateOneInstance(instanceInfo);
                        }
                    });
            // delInstanceButtonObj <button>
                let delInstanceButtonObj = $("<button class='circleButton'>x</button>");
                valueObj.append(delInstanceButtonObj);
                // add click event
                    delInstanceButtonObj.click(function(){
                        // prepare ajax data
                        let curNodePosition = undefined;
                        let newValueDict = undefined;
                        if (delInstanceButtonObj.prev().attr("name") == ""){
                            alert(langDict["Can not delete this value, because this value is already empty."]);
                        }else {
                            // 准备数据
                            curNodePosition = $("#positionValue").text();
                            newValueDict = {
                                [labelDict["key"]]: ""
                            }
                        }
                        // ajax
                        let r = setNode(curNodePosition,newValueDict);
                        if (r != "success"){
                            alert(langDict[r]);
                            return;
                        }
                        // refresh nodeInfoWindow
                        nodeInfoWindow_refresh();
                        // refresh instanceInfoWindow
                        instanceInfoWindow_refresh();
                    });
        // ArrowObj <button>
            let arrowObj = $("<button id='" + labelDict["key"] + "Arrow\' class='circleButton'>←</button>");
            labelObj.append(arrowObj);
            // add click event
                arrowObj.click(function(){
                    // prepare ajax data
                    let curNodePosition = $("#positionValue").text();
                    let curInstanceId = undefined;
                    if ($("#instanceInfo-selectedInstance").css("display") == "block") {
                        curInstanceId = $("#idValue").text();
                    }else{
                        alert(langDict["can not build a reference relation between cur node and cur instance, because no instance are selected."]);
                        return;
                    }
                    let newValue = {[labelDict["key"]]: curInstanceId};
                    // ajax
                    let r = setNode(curNodePosition,newValue);
                    if (r != "success"){
                        alert(langDict[r]);
                        return;
                    }
                    // refresh nodeInfoWindow
                    nodeInfoWindow_refresh();
                    // refresh instanceInfoWindow
                    instanceInfoWindow_refresh();
                    });
    // return
        return labelObj
}

/**
 * This function generate a nodes type label obj.
 *
 * @example
 let labelDict = {
    "key": "mention_list",
    "GUI_name": "mentionList: ",
    "value_type": "node",
    "node_label": "refer",
    "value_default": [[]]
 };
 let labelValue = [
    [
        {"position": "0-0-0", "text":"埃航"},
        {"position":"0-0-1", "text":"狮航"}
    ],
    [
        {"position": "5-2-0", "text":"两家航空公司"}
    ]
 ]
 let labelObj = generateNodesLabelObj(labelDict, labelValue);
 *
 * @param {Array} labelDict **[Required]** Info of the label. Required items included "key", "GUI_name". Optional items
 *   include "value_default".
 * @param {Array} labelValue **[Optional]** The value of this label. The generated obj will display the value if given, or
 *   display the default value in *labelDict* if not given.
 * @return {Jquery.HtmlElement}
 */
function generateNodesLabelObj(labelDict, labelValue){
    // function(labelDict){
        //     reStr =     "<div id='nodeInfo-" + labelDict["key"] + "'>" +
        //                 "   <span id='" + labelDict["key"] + "Key'>" + labelDict["GUI_name"] + "</span>" +
        //                 "   <span id='" + labelDict["key"] + "Value'> " +
        //                 "       <button class='circleButton' name='addList'>x</button>" +
        //                 "   </span>" +
        //                 "   <button id='" + labelDict["key"] + "Arrow\' class='circleButton'>←</button>" +
        //                 "</div>";
        //     reObj = $(reStr);
        //     reObj.css("padding-left","10px");
        //     return reObj
        // },
    // <labelObj>
        let labelObj = $(" <div id='nodeInfo-" + labelDict["key"] + "'></div>");
        labelObj.css("padding-left","10px");
        // <keyObj>
            let keyObj = $("<span id='" + labelDict["key"] + "Key'>" + labelDict["GUI_name"] + "</span>");
            labelObj.append(keyObj);
        // <valueObj>
            let valueObj = $("<span id='" + labelDict["key"] + "Value'></span>");
            labelObj.append(valueObj);
            // <b[>
            valueObj.append($("<span>[</span>"));
            valueObj.append($("<br>/"));
            // <bigBracketObj>
            {
                let bigBracketObj = $("<div name='bigBracket'></div>");
                valueObj.append(bigBracketObj);
                bigBracketObj.css("padding-left", "10px");
                // calc the value
                {
                    // if given a value, display the value
                    if (labelValue != undefined) {
                        //labelValue = labelValue
                    }
                    // if no value given, display the default value
                    else if (labelDict["value_default"] != undefined) {
                        labelValue = labelDict["value_default"];
                    }
                    // if no given value and no default value
                    else {
                        labelValue = [[]];
                    }
                }
                // for each mentionList
                for (let curMentionListIndex = 0; curMentionListIndex < labelValue.length; curMentionListIndex++) {
                    let curMentionList = labelValue[curMentionListIndex];
                    // <mentionListLineObj>
                    let mentionListLineObj = $("<span class='mentionListLine' mentionListIndex='" + curMentionListIndex + "'></span>");
                    bigBracketObj.append(mentionListLineObj);
                        // <s[>
                        mentionListLineObj.append($("<span>[</span>"));
                        // for each mention
                        for (let curMentionIndex = 0; curMentionIndex < curMentionList.length; curMentionIndex++) {
                            // <mention button>
                            {
                                let curMention = curMentionList[curMentionIndex];
                                let curMentionObj = $("<button mentionIndex='" + curMentionIndex + "'></button>");
                                mentionListLineObj.append(curMentionObj);
                                // display value
                                curMentionObj.text(curMention["text"]);
                                curMentionObj.attr("name", curMention["position"]);
                                // add click event
                                curMentionObj.click(function (e) {
                                    alert("展示node信息");
                                });
                            }
                            // <del mention button>
                            {
                                let delMentionButton = $("<button class='circleButton' name='delMentionButton'>x</button>");
                                mentionListLineObj.append(delMentionButton);
                                // add click event
                                delMentionButton.click(function () {
                                    // prepare ajax data
                                    let curInstanceId = $("#idValue").text();
                                    let newValueDict = {"mention_list": {
                                            "action": "del mention",
                                            "mention_list_index":$(this).parent().attr("mentionListIndex"),
                                            "mention_index": $(this).prev().attr("mentionIndex")
                                        }};
                                    // ajax to background
                                    r = setInstance(curInstanceId, newValueDict);
                                    if (r != "success"){
                                        alert(langDict[r]);
                                        return;
                                    }
                                    // refresh nodeInfoWindow
                                    nodeInfoWindow_refresh();
                                    // refresh instanceInfoWindow
                                    instanceInfoWindow_refresh();
                                });
                            }
                            // <semicolon between mention>
                            mentionListLineObj.append($("<span>;</span>"));
                        }
                        // <append new mention button>
                        {
                            let appendNewMentionButtonObj = $("<button class='circleButton'>→</button>");
                            mentionListLineObj.append(appendNewMentionButtonObj);
                            // add click event
                            appendNewMentionButtonObj.click(function () {
                                if ($("#nodeInfo-selectedNode").css("display") != "block"){
                                    alert(langDict["can not build a reference relation between cur node and cur instance, because no node are selected."]);
                                    return
                                }
                                // prepare ajax data
                                let curInstanceId = $("#idValue").text();
                                let newValueDict = {
                                    "mention_list":{
                                        "action": "append mention",
                                        "mention_list_index":$(this).parent().attr("mentionListIndex"),
                                        "new_node_position": $("#positionValue").text()
                                    }
                                };
                                // ajax to background
                                r = setInstance(curInstanceId, newValueDict);
                                if (r != "success"){
                                    alert(langDict[r]);
                                    return;
                                }
                                // refresh nodeInfoWindow
                                nodeInfoWindow_refresh();
                                // refresh instanceInfoWindow
                                instanceInfoWindow_refresh();
                            });
                        }
                        // <s]>
                        mentionListLineObj.append($("<span>]</span>"));
                        // <del mentionList button>
                        {
                            let delMentionListButtonObj = $("<button class='circleButton' name='delMentionListButton'>x</button>");
                            mentionListLineObj.append(delMentionListButtonObj);
                            // add click event
                            delMentionListButtonObj.click(function () {
                                let delButtonList = mentionListLineObj.children("[name=delMentionButton]");
                                for (let curDelButtonIndex = 0; curDelButtonIndex < delButtonList.length; curDelButtonIndex++){
                                    let curDelButtonObj = delButtonList[curDelButtonIndex];
                                    curDelButtonObj.click();
                                }
                                //prepare ajax data
                                let curInstanceId = $("#idValue").text();
                                let newValueDict = {
                                    "mention_list":{
                                        "action": "del mentionList",
                                        "mention_list_index":$(this).parent().attr("mentionListIndex"),
                                    }
                                };
                                // ajax to background
                                r = setInstance(curInstanceId, newValueDict);
                                if (r != "success"){
                                    alert(langDict[r]);
                                    return;
                                }
                                // refresh nodeInfoWindow
                                nodeInfoWindow_refresh();
                                // refresh instanceInfoWindow
                                instanceInfoWindow_refresh();
                            });

                        }
                        // <br/>
                        mentionListLineObj.append($("<br/>"));
                }
                // <add new mentionList button>
                // {
                //     let addNewMentionListButtonObj = $("<button class='circleButton'>+</button>");
                //     bigBracketObj.append(addNewMentionListButtonObj);
                //     addNewMentionListButtonObj.click(function () {
                //         alert("走着瞧");
                //     });
                // }
            }
            // <b]>
            valueObj.append($("<span>]</span>"));
    // return
        return labelObj
}
