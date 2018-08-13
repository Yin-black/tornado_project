var mes = document.getElementById('messages');
        if("WebSocket" in window){

            var ws = new WebSocket("ws://"+location.host+"/websocket");
            ws.onopen = function ()   //连接websocketcd4ok
                {
                $(mes).append('<li>'+'聊天室已连接，可以聊天！'+'<li>')
                };
            ws.onmessage = function (re_msg) {
               //接受消息
                var received_msg = re_msg.data;
                var aLi = $("<li style='background-color: #80bdff'>"+received_msg+"</li>");
                $(mes).append($(aLi)) //  方法一

    //            $(aLi).appendTo(mes); //  方法二
            };
            ws.onclose = function () {
                mes.innerHTML = mes.innerHTML + "<br>连接已经关闭...";
            };
        }
        else
            {
            mes.innerHTML = "聊天室连接失败失败！"
            }
        function WebSocketSend() {
            ws.send($("#text").val());
            $('#text').val('')
        }
