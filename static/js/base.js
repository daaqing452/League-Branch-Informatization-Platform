var editor;
$(document).ready(function(){
	check_red_spot();
});

function check_red_spot() {
	var a = $("a[type=message]");
	if (a.length == 0) {
		$("span#red_spot").hide();
	} else {
		$("span#red_spot").show();
	}
}

function commit(flag){
	switch(flag){
		//登录
		case 1:{
			var username = $("#username").val();
			var password = $("#password").val();
			$.ajax({
				url: "/index/",
				type: "POST",
				data: {"op": "login", "username": username, "password": password},
				success: function(data) {
					var data = JSON.parse(data);
					var result = data['result'];
					if (result == "成功") {
						window.location.reload();
					} else {
						alert(result);
					}
				}
			});
			$("#myModal").modal('hide');
			break;
		}
		//申请
		case 2:{
			$("#myModal").modal('hide');
			break;
		}
		//发送站内信
		case 3:{
			var recver = $("#sg_recver").val().replace(/( )/g, "").split(";");
			var title = $("#sg_title").val();
			/*
				!!!
			*/
			var text = $("#sg_text").val();
			var attach_list = new Array();
			for(var i = 0; i < $("div.attachment").length; i ++ ){
				var attach = new Array();
				attach.push($("div.attachment").eq(i).attr("title"));
				attach.push($("div.attachment").eq(i).attr("url"));
				attach_list.push(attach);
			}
			//console.log(editor.html());
			//console.log(attach_list);
			$.ajax({
				url: "/message/",
				type: "POST",
				data: {"op": "send_message", "recver": JSON.stringify(recver), "title": title, "text": text, "attachment": JSON.stringify(attach_list)},
				success: function(data) {
					var data = JSON.parse(data);
					var result = data["result"];
					if (result != "yes") {
						alert(result);
					} else {
						alert("发送成功");
						$("#myModal").modal('hide');
					}
				}
			});
			break;
		}
		//阅读站内信
		case 4:{
			var mid = $("#message_div").attr("mid");
			$.ajax({
				url: "/message/",
				type: "POST",
				data: {"op": "close_message", "mid": mid},
				success: function(data) {
					var data = JSON.parse(data);
				}
			});
			var li = $("a[mid=" + mid + "]").parent();
			li.remove();
			check_red_spot();
			$("#myModal").modal('hide');
			break;
		}
		//添加院系
		case 5:{
			var name = $("#departmentname").val();
			$.ajax({
			url: window.location.href,
			type: "POST",
			data: {"op": "add_department", "name": name},
			success: function(data) {
				var data = JSON.parse(data);
				alert("添加成功！");
				window.location.reload();
				}
			});
			$("#myModal").modal('hide');
			break;
		}
		//添加支部
		case 6:{
			var name = $("#branchname").val();
			$.ajax({
				url: window.location.href,
				type: "POST",
				data: {"op": "add_branch", "name": name},
				success: function(data) {
					var data = JSON.parse(data);
					alert("添加成功！");
					window.location.reload();
				}
			});
			$("#myModal").modal('hide');
			break;
		}
	}
	
}

function cancel(){
	KindEditor.remove('textarea[name="sg_text"]');
}

function login(){
	$(".modal-dialog").width(250);
	$("#myModal_body").empty();
	$("#myModalLabel").text("登录");
	$("#myModal_body").append("<input class=\"form-control\" id=\"username\" type=\"text\" name=\"username\" placeholder=\"学号\"/><br/>");
	$("#myModal_body").append("<input class=\"form-control\" id=\"password\" type=\"password\" name=\"password\" placeholder=\"密码\"/>");
	$(".modal-footer").children("button").eq(1).attr("onclick","commit(1)");

}

function logout(){
	$.ajax({
		url: "/index/",
		type: "POST",
		data: {"op": "logout"},
		success: function(data) {
			var data = JSON.parse(data);
			window.location.reload();
		}
	});
}

function apply(){
	$(".modal-dialog").width(250);
	$("#myModal_body").empty();
	$("#myModalLabel").text("申请权限");
	var HTMLContent = "<select id=\"apply_select_1\" class=\"form-control\" onchange=\"apply_select_1_onchange()\">"
        				+"<option value=0>申请校管理员</option>"
       					+"<option value=1>申请院系级管理员</option>"
        				+"<option value=2>申请班团级管理员</option>"
        				+"<option value=3>申请团支部成员</option>"
    					+"</select>"
    					+"<br id=\"apply_select_1\" />";
    $("#myModal_body").append(HTMLContent);
    $(".modal-footer").children("button").eq(1).attr("onclick","commit(2)");

}

function apply_select_1_onchange() {
	var value = $("select#apply_select_1").val();
	$("select#apply_select_2").remove();
	$("br#apply_select_2").remove();
	$("select#apply_select_3").remove();
	$("br#apply_select_3").remove();
	if (value >= 1) {
		var HTMLContent = "<select id=\"apply_select_2\" class=\"form-control\" onchange=\"apply_select_2_onchange()\">"
    					+"<option>计算机系</option>"
    					+"<option>建筑学院</option>"
    					+"<option>自动化系</option>"
    					+"</select>"
    					+"<br id=\"apply_select_2\" />";
    	$("#myModal_body").append(HTMLContent);
	}
	if (value >= 2) {
		var HTMLContent = "<select id=\"apply_select_3\" class=\"form-control\">"
    					+"<option>计61班</option>"
    					+"<option>计62班</option>"
    					+"<option>计63班</option>"
    					+"</select>"
    					+"<br id=\"apply_select_3\" />";
    	$("#myModal_body").append(HTMLContent);
	}
}

function apply_select_2_onchange() {
	
}

//去掉包含该元素的div
function del_line(b){
	$b = $(b);
	$b.parents("div").eq(0).remove();
}

function send_message(){
	$(".modal-dialog").width(500);
	$("#myModal_body").empty();
	$("#myModalLabel").text("发送新消息");
	$("#myModelYes").text("发送");
	$("#myModal_body").append("<input class=\"form-control\" id=\"sg_recver\" type=\"text\" placeholder=\"收件人（用分号隔开）\"/><br/>");
	$("#myModal_body").append("<input class=\"form-control\" id=\"sg_title\" type=\"text\" placeholder=\"标题\"/><br/>");
	//$("#myModal_body").append("<textarea class=\"form-control\" id=\"sg_text\" style=\"height:300px\" placeholder=\"正文\"/><br/>");
	$("#myModal_body").append("<textarea   name=\"sg_text\" id=\"sg_text\"></textarea><br/>");
	$(".modal-footer").children("button").eq(1).attr("onclick","commit(3)");
	editor = KindEditor.create('textarea[name="sg_text"]', {
        resizeType : 1,
        allowPreviewEmoticons : false,
        allowImageRemote : false,
        useContextmenu : false,
        uploadJson : '/uploadFile/',
        width : '100%',
        items : [
            'fontname', 'fontsize', '|', 'forecolor', 'hilitecolor', 'bold', 'italic', 'underline',
            'removeformat', '|', 'justifyleft', 'justifycenter', 'justifyright', 'insertorderedlist',
            'insertunorderedlist', '|', 'emoticons', 'image','insertfile']
    });
}

function read_message(b){
	$b = $(b);
	var title = $b.text();
	var mid = $b.attr("mid");
	$("#myModal_body").empty();
	$("#myModalLabel").text(title);
	$.ajax({
		url: "/message/",
		type: "POST",
		data: {"op": "read_message", "mid": mid},
		success: function(data) {
			var data = JSON.parse(data);
			var HTMLContent = "<div id=\"message_div\" mid=" + mid + ">"
				+"<span>发送时间：" + data["send_time"] + "</span><br/><br/>"
				+"<span>" + data["text"] + "</span><br/><br/>";
			attachment = JSON.parse(data["attachment"]);
			for (var i = 0; i < attachment.length; i++) {
				var attach = attachment[i];
				HTMLContent += "<a href=\"" + attach[1] + "\">" + attach[0] + "</a><br/>";
			}
			HTMLContent += "</div>";
			$("#myModal_body").append(HTMLContent);
		}
	});
	$(".modal-footer").children("button").eq(1).attr("onclick","commit(4)");
}