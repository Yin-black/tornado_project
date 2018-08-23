var url =document.getElementById('imgurl');

$(function () {
    $("#down_imgurl").click(function()
    {
        if ($(url).val())
        {
            $.ajax({
                'method': "post",
                'url': "/save",
                'timeout':10000,
                'data': {"imgurl": $(url).val()},
                "success":function (data) {
                    alert('下载图片成功！')
                }
            })
        }
        else{
            alert("网址不能为空！")
        }
    }
)
})


