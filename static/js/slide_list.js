$(document).ready(function(){

});


function release_a_n(){
	$(".modal-dialog").width(500);
	$("#myModal_body").empty();
	$("#myModalLabel").text("发布图文");
	$("#myModelYes").text("发布");
	$("#myModal_body").append("<input class=\"form-control\" id=\"slide_title\" type=\"text\" placeholder=\"标题\"/><br/>");
	$("#myModal_body").append("<input class=\"form-control\" id=\"slide_text\" type=\"text\" placeholder=\"内容\"/><br/>");
	$("#myModal_body").append("<textarea  name=\"sg_text\" id=\"news_text\"></textarea><br/>");
	$("#myModal_body").append("<div class=\"tupianchicun\"></div>")
	editor = KindEditor.create('textarea[name="sg_text"]', {
        resizeType : 1,
        allowPreviewEmoticons : false,
        allowImageRemote : false,
        useContextmenu : false,
        uploadJson : '/uploadFile/',
        width : '100%',
        items : [
            'image']
    });
    $(".modal-footer").children("button").eq(1).attr("onclick","commit(9)");
}

function show(node, status) {
	var sid = $(node).parents("#item").eq(0).attr("sid");
	$.ajax({
		url: window.location.href,
		type: "POST",
		data: {"op": "show", "sid": sid, "show": status},
		success: function(data) {
			var data = JSON.parse(data);
			window.location.reload();
		}
	});
}

function remove(node) {
	var sid = $(node).parents("#item").eq(0).attr("sid");
	if (confirm("确认删除？")) {
		$.ajax({
			url: window.location.href,
			type: "POST",
			data: {"op": "delete_slide", "sid": sid},
			success: function(data) {
				var data = JSON.parse(data);
				window.location.reload();
			}
		});
	}
}

function change_slide_show_num() {
	var num = $("#slide_show_num_input").val();
	var num_pat = new RegExp("^[1-9]$");
	if (num_pat.test(num) == false) {
		alert("请输入1到9之间的正整数！")
		return;
	}
	num = Number(num);
	$.ajax({
		url: window.location.href,
		type: "POST",
		data: {"op": "change_slide_show_num", "num": num},
		success: function(data) {
			var data = JSON.parse(data);
			alert("修改成功！");
			window.location.reload();
		}
	});
}