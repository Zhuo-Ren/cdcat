//label template
labelTemplate = {
    "radio": {
        "generateLabelObj_func":generateRadioLabelObj
    },
    "checkbox":{
        "generateLabelObj_func": function(labelDict){
            return  $("<span>没实现</span>");
        }
    },
    "menuone":{
        "generateLabelObj_func": generateMenuOneLabelObj
    },
    "menumulti":{
        "generateLabelObj_func": function(labelDict){
            return  $("<span>没实现</span>");
        }
    },
    "textreadonly":{
        "generateLabelObj_func": generateTextReadonlyLabelObj
    },
    "textinput":{
        "generateLabelObj_func": generateTextInputLabelObj
    },
    "objlist": {
        "generateLabelObj_func": generateObjListLabelObj,
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
    let labelObj = $(" <div name='labelInfo-" + labelDict["key"] + "'><div>");
    labelObj.css("padding-left","10px");
        // keyObj <span>
        let keyObj = $("<span id='" + labelDict["key"] + "Key'>" + labelDict["GUI_name"] + "</span>");
        labelObj.append(keyObj);
        // valueObj <span>
        let valueObj = $("<span id='" + labelDict["key"] + "Value'></span>");
            // optionObj <span><input type="radio" name="XXX" value="XXX">XXX</span>
            for (optionIndex = 0; optionIndex < labelDict["value_option"].length; optionIndex++)
            {
                let curOption = labelDict["value_option"][optionIndex];
                curOptionObj = $("<input type = 'radio' name = '" + labelDict["key"] + "' value = '" + curOption[1] + "' /><span>"+curOption[0]+" </span>");
                // if given a value, display the value
                if (labelValue != undefined){
                    if (labelValue == curOption[1]){
                        curOptionObj[0].checked = true;
                    }
                }
                // // if no value given, display the default value
                // else if (labelDict["value_default"] != undefined){
                //     if (labelDict["value_default"] == curOption[1]){
                //         curOptionObj[0].checked = true;
                //     }
                // }
                valueObj.append(curOptionObj);
            }
        valueObj.change(function() {
            if ($("#nodeInfoWindow")[0].contains(this)){
                let position = $("#positionValue").text();
                let value = $("#" + labelDict["key"] + "Value :checked").attr("value");
                let r = setNode(position, {[labelDict["key"]]: value});
                if (r[0] != "success"){
                    alert(langDict[r[1]]);
                    return;
                }else{
                    // refresh nodeInfoWindow
                    nodeInfoWindow_refresh();
                    // refresh instanceInfoWindow
                    instanceInfoWindow_refresh();
                }
            }else if($("#instanceInfoWindow")[0].contains(this)){
                let id = $("#idValue").text();
                let value = $("#" + labelDict["key"] + "Value :checked").attr("value");
                // ajax to background
                let r = setInstance(id, {[labelDict["key"]]: value});
                if (r[0] != "success"){
                    alert(langDict[r[1]]);
                    return;
                }else{
                    // refresh nodeInfoWindow
                    nodeInfoWindow_refresh();
                    // refresh instanceInfoWindow
                    instanceInfoWindow_refresh();
                }
            }
        });
        labelObj.append(valueObj);
    // return
    return labelObj
}

/**
 * This function generate a MenuOne type label obj.
 *
 * @example
 let labelDict = {
      "key": "type",
      "GUI_name": "type of the mention: ",
      "value_type": "MenuOne",
      "value_option": [["无", "none"],["人", "PEO"],["地", "LOC"],["行为", "ACT"],["组织", "ORG"],["物", "SUB"]],
      "value_default": "none"
    };
 let labelValue = "ORG";
 let labelObj = generateMenuOneLabelObj(labelDict, labelValue);
 *
 * @param {Array} labelDict **[Required]** Info of the label. Required items included "key", "GUI_name", "value_option".
 *   Optional items include "value_default".
 * @param {Array} labelValue **[Optional]** The value of this label. The generated obj will display the value if given, or
 *   display the default value in *labelDict* if not given.
 * @return {Jquery.HtmlElement}
 */
function generateMenuOneLabelObj(labelDict, labelValue){
    // labelObj <div>
    let labelObj = $(" <div name='labelInfo-" + labelDict["key"] + "'></div>");
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
                    // // if no value given, display the default value
                    // else if (labelDict["value_default"] != undefined){
                    //     if (curOption[1] == labelDict["value_default"]){
                    //         optionObj[0].selected = true;
                    //     }
                    // }
                    selectObj.append(optionObj);
                }
            valueObj.append(selectObj);
        valueObj.change(function() {
            if ($("#nodeInfoWindow")[0].contains(this)){
                var nodeId = $("#idValue").text();
                let value = $("#" + labelDict["key"] + "Value :checked").attr("value");
                let r = setNode(nodeId, {[labelDict["key"]]: value});
                if (r[0] != "success"){
                    alert(langDict[r[1]]);
                    return;
                }else{
                    // refresh nodeInfoWindow
                    nodeInfoWindow_refresh();
                    // refresh instanceInfoWindow
                    instanceInfoWindow_refresh();
                }
            }else if($("#instanceInfoWindow")[0].contains(this)){
                // prepare ajax data
                var id = $("#instanceInfo-selectedInstance div[name='labelInfo-id'] #idValue").text();
                console.log(id)
                let value = $("#instanceInfo-selectedInstance div[name='labelInfo-type'] #typeValue option:selected").attr("value")
                console.log(value)
                if (id == "XXXXX"){
                    return;
                }
                // ajax to background
                let r = setInstance(id, {[labelDict["key"]]: value});
                // GUI update
                console.log(r)
                if (r[0] != "success"){
                    alert(langDict[r[1]]);
                    return;
                }else{
                    // refresh nodeInfoWindow
                    nodeInfoWindow_refresh();
                    // refresh instanceInfoWindow
                    instanceInfoWindow_refresh();
                }
            }
        });
        labelObj.append(valueObj);
    // return
    return labelObj
}

/**
 * This function generate a textreadonly type label obj.
 *
 * @example
 let labelDict = {
        "key": "position",
        "GUI_name": "position: ",
        "value_type": "textreadonly",
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
    let labelObj = $(" <div name='labelInfo-" + labelDict["key"] + "'></div>");
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
 * This function generate a textinput type label obj.
 *
 * @example
 let labelDict = {
    "key": "desc",
    "GUI_name": "desc: ",
    "value_type": "textinput",
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
    let labelObj = undefined;
    // labelObj <div>
    {
        labelObj = $(" <div name='labelInfo-" + labelDict["key"] + "'></div>");
        labelObj.css("padding-left","10px");
        // keyObj <span>
        {
            let keyObj = $("<span id='" + labelDict["key"] + "Key'>" + labelDict["GUI_name"] + "</span>");
            labelObj.append(keyObj);
        }
        // valueObj <span>
        {
            let valueObj = $("<input id='" + labelDict["key"] + "Value' type='text'></input>");
            labelObj.append(valueObj);
            // display the label value
            {
                let inputText = undefined;
                // if given a value, display the value
                if (labelValue != undefined) {
                    inputText =  labelValue;
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
            valueObj.change(function() {
                // if the changed label belongs to a node
                if ($("#nodeInfoWindow")[0].contains(this)){
                    let position = $("#positionValue").text();
                    let value = $("#" + labelDict["key"] + "Value")[0].value;
                    let r = setNode(position, {[labelDict["key"]]: value});
                    if (r[0] != "success"){
                        alert(langDict[r[1]]);
                        return;
                    }else{
                        // refresh nodeInfoWindow
                        nodeInfoWindow_refresh();
                        // refresh instanceInfoWindow
                        instanceInfoWindow_refresh();
                    }
                }
                // if the changed label belongs to a instance
                else if($("#instanceInfoWindow")[0].contains(this)){
                    // prepare ajax data
//                    let td = $('instanceInfo-selectedInstance td')
//                    console.log(td)
//                    console.log($("#instanceInfo-selectedInstance div[name='labelInfo-id'] #idValue").text())
                    let id = $("#instanceInfo-selectedInstance div[name='labelInfo-id'] #idValue").text();
                    let value = $("#" + labelDict["key"] + "Value")[0].value;
                    console.log(id)
                    console.log(value)
                    // ajax to background
                    let r = setInstance(id, {[labelDict["key"]]: value});
                    if (r[0] != "success"){
                        alert(langDict[r[1]]);
                        return;
                    }else{
                        // refresh nodeInfoWindow
                        nodeInfoWindow_refresh();
                        // refresh instanceInfoWindow
                        instanceInfoWindow_refresh();
                        // update instance
                        instanceSelectWindow_updateOneInstance(r[1])
                    }
                }
            });
        }

    }
    // return
    return labelObj
}

function generateObjListLabelObj(labelDict, labelValue){
    /* 输入类似于：
    labelDict =  { GUI_name: "refer: ", key: "refer", value_type: "objlist" }
    labelValue = [ "i:2021060515413405139" ]
    或
    labelDict =  { GUI_name: "mention_list: ", key: "mentions", value_type: "objlist" }
    labelValue = [ "i:2021060515413405139" ]
     */
    let labelObj = $(" <div name='labelInfo-" + labelDict["key"] + "'></div>");
    labelObj.css("padding-left","10px");
    // <keyObj>
        let keyObj = $("<span id='" + labelDict["key"] + "Key'>" + labelDict["GUI_name"] + "</span>");
        labelObj.append(keyObj);
    // <valueObj>
        let valueObj = $("<span id='" + labelDict["key"] + "Value'></span>");
        labelObj.append(valueObj);
        // 如果nodeList标签的值是空，那么改成[]。这样才能显示操作按钮。
        // 不用担心这里改了以后和后台数据不一致，因为nodeListLabel的value_empty就是[]。
        if ((labelValue == undefined)||(labelValue == null)){
            labelValue = [];
        }
        //
        if (labelValue){
            // 左中括号
            valueObj.append($("<span>[</span>"));
            // 中间的东西
            {
                let insideObj = $("<div></div>");
                insideObj.css("padding-left","10px");
                for (let itemIndex = 0; itemIndex<labelValue.length; itemIndex++){
                    //
                    let curItemId = labelValue[itemIndex];
                    // curItemObj
                    {
                        // 如果要添加的item是node
                        if(curItemId.slice(0, 2) == "n:"){
                            // 获取Item信息
                            let curItem = undefined;
                            {
                                let r = getNodeById(curItemId);
                                if (r[0] == "success") {
                                    curItem = r[1];
                                }
                            }
                            // nodeButtonObj <button>
                            {
                                let curItemObj = $("<button class='node' name='' style='background-color: lightcyan;'>" + curItem["text"] + "</button>");
                                insideObj.append(curItemObj);
                                // display the label value

                                // add click event
                            }
                            // delNodeButtonObj <button>
                            {
                                let delNodeButtonObj = $("<button class='circleButton' style='background-color: lightcyan;'>x</button>");
                                insideObj.append(delNodeButtonObj);
                                // add click event
                                    delNodeButtonObj.click(function(){
                                        // 获取这个标签的owner是node还是instance
                                        let ownerType = undefined;
                                        if ($.contains( $("#nodeInfo-selectedNode")[0], $(this)[0])){
                                            ownerType = "node"
                                        }else if($.contains( $("#instanceInfo-selectedInstance")[0], $(this)[0])){
                                            ownerType = "instance"
                                        }else{
                                            // 报错
                                        }
                                        // prepare ajax data
                                        let curId = undefined;
                                        let newValueDict = undefined;
                                        if (delNodeButtonObj.prev().attr("name") == ""){
                                            alert(langDict["Can not delete this value, because this value is already empty."]);
                                        }else {
                                            // 准备数据
                                            if (ownerType == "node"){
                                                curId = $("#nodeInfo-selectedNode div[name='labelInfo-id'] #idValue").text()
                                            } else if (ownerType == "instance"){
                                                curId = $("#instanceInfo-selectedInstance div[name='labelInfo-id'] #idValue").text()
                                            }
                                            newValueDict = {
                                                [labelDict["key"]]: JSON.stringify({
                                                    "action": "del",
                                                    "targetObjId": delInstanceButtonObj.prev().attr("name"),
                                                })
                                            }
                                        }
                                        // ajax
                                        let r = undefined;
                                        if (ownerType == "node"){
                                            r = setNode(curId,newValueDict);
                                        }else if (ownerType == "instance"){
                                            r = setInstance(curId,newValueDict);
                                        }
                                        // GUI update
                                        if (r[0] != "success"){
                                            alert(langDict[r[1]]);
                                            return;
                                        }else{
                                            // refresh nodeInfoWindow
                                            nodeInfoWindow_refresh();
                                            // refresh instanceInfoWindow
                                            instanceInfoWindow_refresh();
                                        }
                                    });
                            }
                        }
                        // 如果要添加的item是instance
                        else if(curItemId.slice(0, 2) == "i:"){
                            // 获取Item信息
                            let curItem = undefined;
                            {
                                let r = getInstanceById(curItemId);
                                if (r[0] == "success"){
                                    curItem = r[1];
                                }
                            }
                            // instanceButtonObj <button>
                            {
                                let curItemObj = $("<button class='instance' name='' style='background-color: #c5c5c5;'></button>");
                                insideObj.append(curItemObj);
                                // display the label value
                                    let inputText = undefined;
                                    let instanceId = undefined;
                                    {
                                        // if given a value, display the value
                                        if (curItem != undefined) {
                                            if (curItem["desc"]==""){
                                                inputText = '　';
                                            }else{
                                                inputText =  curItem["desc"];
                                            }
                                            instanceId = curItem["id"];
                                        }
                                        // if no value given
                                        else{
                                            inputText = '　';
                                            instanceId = ""
                                        }
                                    }
                                    curItemObj.text(inputText);
                                    curItemObj.attr("name", instanceId);
                                // add click event
                                    curItemObj.click(function(e){
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
                            }
                            // delInstanceButtonObj <button>
                            {
                                let delInstanceButtonObj = $("<button class='circleButton'>x</button>");
                                insideObj.append(delInstanceButtonObj);
                                // add click event
                                    delInstanceButtonObj.click(function(){
                                        // 获取这个标签的owner是node还是instance
                                        let ownerType = undefined;
                                        if ($.contains( $("#nodeInfo-selectedNode")[0], $(this)[0])){
                                            ownerType = "node"
                                        }else if($.contains( $("#instanceInfo-selectedInstance")[0], $(this)[0])){
                                            ownerType = "instance"
                                        }else{
                                            // 报错
                                        }
                                        // prepare ajax data
                                        let curId = undefined;
                                        let newValueDict = undefined;
                                        if (delInstanceButtonObj.prev().attr("name") == ""){
                                            alert(langDict["Can not delete this value, because this value is already empty."]);
                                        }else {
                                            // 准备数据
                                            if (ownerType == "node"){
                                                curId = $("#nodeInfo-selectedNode div[name='labelInfo-id'] #idValue").text()
                                            } else if (ownerType == "instance"){
                                                curId = $("#instanceInfo-selectedInstance div[name='labelInfo-id'] #idValue").text()
                                            }
                                            newValueDict = {
                                                [labelDict["key"]]: JSON.stringify({
                                                    "action": "del",
                                                    "targetObjId": delInstanceButtonObj.prev().attr("name"),
                                                })
                                            }
                                        }
                                        // ajax
                                        let r = undefined;
                                        if (ownerType == "node"){
                                            r = setNode(curId,newValueDict);
                                        }else if (ownerType == "instance"){
                                            r = setInstance(curId,newValueDict);
                                        }
                                        // GUI update
                                        if (r[0] != "success"){
                                            alert(langDict[r[1]]);
                                            return;
                                        }else{
                                            // refresh nodeInfoWindow
                                            nodeInfoWindow_refresh();
                                            // refresh instanceInfoWindow
                                            instanceInfoWindow_refresh();
                                        }
                                    });
                            }
                        }
                    }
                }
                //
                valueObj.append(insideObj);
            }
            // 右中括号
            valueObj.append($("<span>]</span>"));
            // addInstanceByCurInstance按钮
            {
                let addInstanceByCurInstanceButtonObj = $("<button id='" + labelDict["key"] + "CI\' class='circleButton' style='background-color: #c5c5c5;'>c</button>");
                valueObj.append(addInstanceByCurInstanceButtonObj);
                // add click event
                addInstanceByCurInstanceButtonObj.click(function(){
                    // 获取这个标签的owner是node还是instance
                    let ownerType = undefined;
                    if ($.contains( $("#nodeInfo-selectedNode")[0], $(this)[0])){
                        ownerType = "node"
                    }else if($.contains( $("#instanceInfo-selectedInstance")[0], $(this)[0])){
                        ownerType = "instance"
                    }else{
                        // 报错
                    }
                    // prepare ajax data
                    let curId = undefined;
                    if (ownerType == "node"){
                        curId = $("#nodeInfo-selectedNode div[name='labelInfo-id'] #idValue").text()
                    } else if (ownerType == "instance"){
                        curId = $("#instanceInfo-selectedInstance div[name='labelInfo-id'] #idValue").text()
                    }
                    let curInstanceId = undefined;
                    if ($("#instanceInfo-selectedInstance").css("display") == "block") {
                        curInstanceId = $("#instanceInfo-selectedInstance #idValue").text();
                    }else{
                        alert(langDict["can not build a reference relation between cur node and cur instance, because no instance are selected."]);
                        return;
                    }
                    let newValueDict = {
                        [labelDict["key"]]: JSON.stringify({
                            "action": "add",
                            "targetObjId": curInstanceId,
                        })
                    };
                    // ajax
                    let r = undefined;
                    if (ownerType == "node"){
                        r = setNode(curId,newValueDict);
                    }else if (ownerType == "instance"){
                        r = setInstance(curId,newValueDict);
                    }
                    // GUI update
                    if (r[0] != "success"){
                        alert(langDict[r[1]]);
                        return;
                    }else{
                        // refresh nodeInfoWindow
                        nodeInfoWindow_refresh();
                        // refresh instanceInfoWindow
                        instanceInfoWindow_refresh();
                    }
                });
            }
            // addInstanceBySelect按钮
            /*
            {
                let setInstanceBySelectButtonObj = $("<button id='" + labelDict["key"] + "Finger\' class='circleButton'>☞</button>");
                valueObj.append(setInstanceBySelectButtonObj);
                // add click event
                setInstanceBySelectButtonObj.click(function(){
                    if ($(".slot").length == 0){
                        setInstanceBySelectButtonObj.addClass("slot");
                        // 上特效
                        document.body.style.cursor = "help";
                        setInstanceBySelectButtonObj.css("background", "red");
                    }
                });
                // add fill slot function
                setInstanceBySelectButtonObj[0].fillSlot = function(selectedInstanceId){  // html dom对象能存方法，jquery dom对象不行
                    // prepare ajax data
                    let curNodePosition = $("#positionValue").text();
                    let newValue = {[labelDict["key"]]: selectedInstanceId};
                    // ajax
                    let r = setNode(curNodePosition,newValue);
                    // GUI update
                    if (r[0] != "success"){
                        alert(langDict[r[1]]);
                        return;
                    }else{
                        setInstanceBySelectButtonObj.removeClass("slot");
                        // 去特效
                        document.body.style.cursor = "";
                        setInstanceBySelectButtonObj.css("background", "white");
                        // refresh nodeInfoWindow
                        nodeInfoWindow_refresh();
                        // refresh instanceInfoWindow
                        instanceInfoWindow_refresh();
                    }
                };

            }
             */
        }
    return labelObj

}
