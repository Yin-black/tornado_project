$(document).ready(function(){
    if (!window.console) window.console.log={};
    if(!window.console.log) window.console.log=function () {};

    //点击发送按钮时执行
    $("#messageform").on("submit",function () {
        newMessage($(this));
        //console.log("new connection");
        return false;
    });
    //按回车键发送
    $("#messageform").on("keypress",function (e) {
        if (e.keyCode ==13)
        {
            newMessage($(this));
            return false;
        }
    });
    $("#message").select();
    updater.start();
});

$.fn.formToDict = function () {   //把form表单里的name属性不为next的值，添加为字典
    var fields = this.serializeArray();
    var json = {};
    for (var i=0; i<fields.length; i++){
        json[fields[i].name] = fields[i].value;    //存取为json：fields{"body":"value"}
    }
    if (json.next)
    {
        delete json.next;
    }
   // console.log(json)
    return json;

};

//发送新消息到服务器
function newMessage(form) {
    var message = form.formToDict();
    updater.socket.send(JSON.stringify(message));   //把js数据转为json再发送
    form.find("input[type=text]").val("").select(); //查找input[type=text]置空，并选择
}

var updater = {
    socket: null,
    start: function () {
        var url = "ws://" + location.host + "/ws";
        updater.socket = new WebSocket(url);
        updater.socket.onmessage = function (event) {
            updater.showMessage(JSON.parse(event.data))  //把Json数据转换为js并显示
        };
    },

    showMessage: function (message) {
        var existing = $("#m" + message.id);
        //console.log(message.id);
        if (existing.length > 0) return;
        var node = $(message.html);
        console.log(message.html);
        $("#inbox").append(node);   //把message.html加到websocket.html中
    },
};


