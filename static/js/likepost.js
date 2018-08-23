//改变显示样式
function change_like_style(data) {
    if (data == 'like') {
        $("#like").css("color","red")
        //console.log(data)
    }
    else {
        $("#like").css("color","black");}
        //console.log(data)
}

function weaker_like(post_id) {
    $.ajax({
        'url':'/like',
        'method':'get',
        "data":{
            'post_id':post_id
        },
        "success":function (resp) {
            change_like_style(resp);
            //console.log(resp)
        },
    })
}
//提交喜欢或不喜欢选择
function like(post_id,active) {
    $.ajax({
        "method":"post",
        "url":"/like",
        "data":{
            "post_id":post_id,
            "active":active,
        },
        "success":function (resp) {
            change_like_style(resp);
            //alert(resp)
        },
        'error':function () {
            console.log('error')
        }
    })

}

$(document).ready(function () {
    var post_id = location.pathname.split('/').pop() ; //返回当前图片ID

    weaker_like(post_id);   //确认用户是否已添加到喜欢，变改变心型的样式

    $("#like").click(function (){
        if ($("#like").css("color") == "rgb(0, 0, 0)")
        {
            like(post_id=post_id,active="like")
        }
        else{
            like(post_id=post_id,active="unlike")
        }
    })

})



