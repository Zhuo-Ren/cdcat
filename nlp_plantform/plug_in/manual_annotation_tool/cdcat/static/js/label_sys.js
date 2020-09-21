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
        "generateLabelObj_func": function(labelDict){
            reStr = "<div id='nodeInfo-" + labelDict["key"] + "'>" +
                    "   <span id='" + labelDict["key"] + "Key'>" + labelDict["GUI_name"] + "</span>" +
                    "   <input id='" + labelDict["key"] + "Value' type='text' value='" + labelDict["value_default"] + "'/>" +
                    "</div>";
            reObj = $(reStr);
            reObj.css("padding-left","10px");
            return reObj
        },
        "addUpdateValueFunc_func": function (labelDict) {
            return function(newValue){
                alert("没实现")
            };
        },
        "addEvent_func": function(labelDict){
            $("#" + labelDict["key"] + "Value").change(function() {
                // if the changed label belongs to a node
                if ($("#nodeInfoWindow")[0].contains(this)){
                    let position = $("#positionValue").text();
                    let value = $("#" + labelDict["key"] + "Value")[0].value;
                    setNode(position, {[labelDict["key"]]: value});
                }
                // if the changed label belongs to a instance
                else if($("#instancInfoWindow")[0].contains(this)){
                    // prepare ajax data
                    let id = $("#idValue").text();
                    let value = $("#" + labelDict["key"] + "Value")[0].value;
                    // ajax to background
                    instanceInfo = setInstance(id, {[labelDict["key"]]: value});
                    // display the new instance info in GUI
                    instanceInfoWindow_updateInstanceInfo(instanceInfo);
                    instanceInfoWindow_showInstanceInfo();
                    instanceSelectWindow_updateOneInstance(instanceInfo);

                    // The change of instance may lead to a change of nodes, so we also update the current node.
                    if ($("#nodeInfo-selectedNode").css("display") == "block"){
                        // prepare ajax data
                        let position = $("#pathValue").text();
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
        }
    },
    "instance":{
        "generateLabelObj_func": function(labelDict){
            reStr =     " <div id='nodeInfo-" + labelDict["key"] + "'>" +
                        "   <span id='" + labelDict["key"] + "Key'>" + labelDict["GUI_name"] + "</span>" +
                        "   <span id='" + labelDict["key"] + "Value'> " +
                        "       <button class='instance' name=''>none</button>" +
                        "       <button class='circleButton'>x</button>" +
                        "   </span>" +
                        "   <button id='" + labelDict["key"] + "Arrow\' class='circleButton'>←</button>" +
                        "</div>";
            reObj = $(reStr);
            reObj.css("padding-left","10px");
            return reObj
        },
        "addUpdateValueFunc_func": function (labelDict) {
            return function(newValue){
                if(newValue != undefined){
                    let label = $("#" + labelDict["key"] + "Value button.instance");
                    label.text(newValue["desc"]);
                    label.attr("name", newValue["id"]);
                    // label.addClass("instance");
                    // label.click(function(){
                    //     if(clickFlag) {//取消上次延时未执行的方法
                    //         clickFlag = clearTimeout(clickFlag);
                    //     }
                    //     curSelectedInstance = this;
                    //     clickFlag = setTimeout(function(){
                    //         instanceClick();
                    //     }, 149);//延时300毫秒执行
                    // })
                }else{
                    let label = $("#" + labelDict["key"] + "Value button.instance");
                    label.text("none");
                    label.attr("name", "");
                    // nodeInstance.text("none");
                    // nodeInstance.attr("name", "");
                    // nodeInstance.removeClass("instance");
                    // nodeInstance.click(function(){});
                }
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
            $("#" + labelDict["key"] + "Value Button.instance").click(function(e){
                let instanceIdStr = this.name;
                if (instanceIdStr == ""){
                    alert(langDict["Can not view the info of this instance, because it is a empty instance."]);
                }else{
                    let instanceInfo = getInstanceById(instanceIdStr);
                    instanceInfoWindow_showInstanceInfo(instanceInfo);
                    instanceSelectWindow_updateOneInstance(instanceInfo);
                }
            });
            $("#" + labelDict["key"] + "Value Button.circleButton").click(function(e){
               if (this.prev().name == ""){
                   alert(langDict["Can not delete this value, because this value is already empty."]);
               }else{
                   // 准备数据
                   let curNodePosition = $("#pathValue").text();
                   let newValueDict = {
                       [labelDict["key"]]: ""
                   }
                   // 回传给后台
                   let nodeInfo = setNode(curNodePosition, newValueDict);
                   // 显示节点的最新信息
                   nodeInfoWindow_updateNodeInfo(nodeInfo);
                   nodeInfoWindow_showNodeInfo(nodeInfo);

               }
            });
            $("#" + labelDict["key"] + "Arrow").click(function(e){
                // 准备数据
                let curNodePosition = $("#pathValue").text();
                let newValueDict = {
                    [labelDict["key"]]: $("#idValue").text()
                }
                // 回传给后台
                let nodeInfo = setNode(curNodePosition, newValueDict);
                // 显示节点的最新信息
                nodeInfoWindow_updateNodeInfo(nodeInfo);
                nodeInfoWindow_showNodeInfo(nodeInfo);
                //
                // var slot = curTriggerInstanceSlot;
                // if (slot.parentElement.parentElement.getAttribute("id") === "nodeInfoWindow"){
                //     var slotType = "node";
                //     var position = $("#pathValue").text();
                // }
                // newInstanceId = curSelectedInstance.name;
                // // 向后台传数据
                // if (slotType === "node"){
                //     setNode(position,{"instance":newInstanceId});
                // } else if (slotType === "instance"){
                //     setInstance()
                // }
                // // 取消当前solt的待选特效
                // curTriggerInstanceSlot.classList.remove("curSlot");
                // document.body.style.cursor = "";
                // //
                // curTriggerInstanceSlot = undefined
                // // 更新instance info
                // if (curSelectedInstance != undefined){
                //     getInstanceById(curSelectedInstance.name);
                // }
            });
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
    "node": {
        "generateLabelObj_func": function(labelDict){
            reStr =     "<div id='nodeInfo-" + labelDict["key"] + "'>" +
                        "   <span id='" + labelDict["key"] + "Key'>" + labelDict["GUI_name"] + "</span>" +
                        "   <span id='" + labelDict["key"] + "Value'> " +
                        "       <button class='circleButton' name='addList'>x</button>" +
                        "   </span>" +
                        "   <button id='" + labelDict["key"] + "Arrow\' class='circleButton'>←</button>" +
                        "</div>";
            reObj = $(reStr);
            reObj.css("padding-left","10px");
            return reObj
        },
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
                                alert(langDict["set instance fail."]);
                            }
                            else if (typeof data == "object"){
                                instanceInfoWindow_showInstanceInfo();
                                instanceInfoWindow_updateInstanceInfo(data);
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
                            alert(langDict["set instance fail."]);
                        }
                        else if (typeof data == "object"){
                            instanceInfoWindow_showInstanceInfo(data);
                        }
                    }
                )
            }

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
                setNode(position, {[labelDict["key"]]: value});
            }else if($("#instancInfoWindow")[0].contains(this)){
                                                                   let id = $("#idValue").text();
                                                                   let value = $("#" + labelDict["key"] + "Value :checked").attr("value");
                                                                   setInstance(id, {[labelDict["key"]]: value});
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
                setNode(position, {[labelDict["key"]]: value});
            }else if($("#instancInfoWindow")[0].contains(this)){
                var id = $("#pidValue").text();
                var value = $("#" + labelDict["key"] + "Value :checked").attr("value");
                setInstance(id, {[labelDict["key"]]: value});
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
 let labelObj = generateListOneLabelObj(labelDict, labelValue);
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