//label template
labelTemplate = {
    "radio": {
        "generateLabelObj_func": function (labelDict) {
            reStr = " <div id='nodeInfo-" + labelDict["key"] + "'>" +
                    "   <span id='" + labelDict["key"] + "Key'>&nbsp &nbsp " + labelDict["GUI_name"] + ":</span>" +
                    "   <span id='" + labelDict["key"] + "Value'>";
            for (optionIndex = 0; optionIndex < labelDict["value_option"].length; optionIndex++) {
                curOption = labelDict["value_option"][optionIndex];
                reStr += "       <input type = 'radio' name = '" + labelDict["key"] + "' value = '" + curOption[1] + "' />" + curOption[0];
            }
            reStr += "   </span>" +
                "</div>";
            reObj = $(reStr);
            return reObj
        },
        "addUpdateValueFunc_func": function (labelDict) {
            return function (newValue) {
                if (newValue != undefined){
                    $("#" + labelDict["key"] + "Value input[value=" + newValue + "]")[0].checked = true;
                }else{
                    $("#" + labelDict["key"] + "Value input[value=" + labelDict["value_default"][1] + "]")[0].checked = true;
                }
            }
        },
        "addValueChangeEvent_func": function(labelDict){
            $("#" + labelDict["key"] + "Value input").change(function() {
                var position = $("#positionValue").text();
                var value = $("#" + labelDict["key"] + "Value :checked").attr("value");
                if (value === "false"){
                    value = false;
                }else if(tokenValue === "true"){
                    value = true;
                }
                setNode(position, {[labelDict["key"]]: value});
            });
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
        "generateLabelObj_func": function(labelDict){
            reStr =     " <div id='nodeInfo-" + labelDict["key"] + "'>" +
                        "   <span id='" + labelDict["key"] + "Key'>&nbsp &nbsp " + labelDict["GUI_name"] + ":</span>" +
                        "   <span id='" + labelDict["key"] + "Value'>" +
                        "   <select>";
            for (optionIndex = 0; optionIndex < labelDict["value_option"].length; optionIndex++){
                curOption = labelDict["value_option"][optionIndex];
                reStr +="       <option value = '" + curOption[1] + "'>" + curOption[0] + "</option>";
            }
            reStr +=    "   </select>"
                        "   </span>" +
                        "</div>";
            reObj = $(reStr);
            return reObj
        },
        "addUpdateValueFunc_func": function(labelDict) {
            return function(newValue){
                if (newValue != undefined) {
                    $("#" + labelDict["key"] + "Value option[value=" + newValue + "]")[0].selected = true;
                }else{
                    $("#" + labelDict["key"] + "Value option[value=" + labelDict["value_default"][1] + "]")[0].selected = true;
                }
            };
        },
        "addValueChangeEvent_func": function(labelDict){
            $("#" + labelDict["key"] + "Value select").change(function() {
                let position = $("#positionValue").text();
                let value = $("#" + labelDict["key"] + "Value :checked").attr("value");
                setNode(position, {[labelDict["key"]]: value});
            });
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
    "instance":{
        "generateLabelObj_func": function(labelDict){
            reStr =     " <div id='nodeInfo-" + labelDict["key"] + "'>" +
                        "   <span id='" + labelDict["key"] + "Key'>&nbsp &nbsp " + labelDict["GUI_name"] + ":</span>" +
                        "   <button id='" + labelDict["key"] + "Value'>none</button>" +
                        "   <span>(double click to edit)</span>"
                        "   </span>" +
                        "</div>"
            reObj = $(reStr);
            return reObj
        },
        "addUpdateValueFunc_func": function (labelDict) {
            return function(newValue){
                if(newValue != undefined){
                    let nodeInstance = $("#" + labelDict["key"] + "Value");
                    nodeInstance.text(newValue["desc"]);
                    nodeInstance.attr("name", newValue["id"]);
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
                    let nodeInstance = $("#" + labelDict["key"] + "Value");
                    nodeInstance.text("none");
                    nodeInstance.attr("name", "");
                    nodeInstance.removeClass("instance");
                    nodeInstance.click(function(){});
                }
            };
        },
        "addValueChangeEvent_func": function(labelDict){
            $("#" + labelDict["key"] + "Value").change(function() {
                alert("没实现")
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
    "text-readonly":{
        "generateLabelObj_func": function(labelDict){
            reStr = " <div id='nodeInfo-" + labelDict["key"] + "'>" +
                    "   <span id='" + labelDict["key"] + "Key'>&nbsp &nbsp " + labelDict["GUI_name"] + ":</span>" +
                    "   <span id='" + labelDict["key"] + "Value'>XXXX</span>" +
                    "</div>";
            reObj = $(reStr);
            return reObj
        },
        "addUpdateValueFunc_func": function (labelDict) {
            return function(newValue){
                if (newValue != undefined){
                    $("#" + labelDict["key"] + "Value")[0].textContent = newValue;
                }else{
                    $("#" + labelDict["key"] + "Value")[0].textContent = labelDict["value_default"];
                }
            };
        },
        "addValueChangeEvent_func": function(labelDict){
            $("#" + labelDict["key"] + "Value").change(function() {
            });
        }
    },
    "text":{
        "generateLabelObj_func": function(labelDict){
            reStr = " <div id='nodeInfo-" + labelDict["key"] + "'>" +
                    "   <span id='" + labelDict["key"] + "Key'>&nbsp &nbsp " + labelDict["GUI_name"] + ":</span>" +
                    "   <span id='" + labelDict["key"] + "Value'>XXXX</span>" +
                    "</div>";
            reObj = $(reStr);
            return reObj
        },
        "addUpdateValueFunc_func": function (labelDict) {
            return function(newValue){
                if (newValue != undefined){
                    $("#" + labelDict["key"] + "Value")[0].textContent = newValue;
                }else{
                    $("#" + labelDict["key"] + "Value")[0].textContent = labelDict["value_default"];
                }
            };
        },
        "addValueChangeEvent_func": function(labelDict){
            $("#" + labelDict["key"] + "Value").change(function() {
            });
        }
    },
    "text-input":{
        "generateLabelObj_func": function(labelDict){
            return  $("<span>没实现</span>");
        },
        "addUpdateValueFunc_func": function (labelDict) {
            return function(newValue){
                alert("没实现")
            };
        },
        "addValueChangeEvent_func": function(labelDict){
            $("#" + labelDict["key"] + "Value").change(function() {
                alert("没实现");
            });
        }
    },
}