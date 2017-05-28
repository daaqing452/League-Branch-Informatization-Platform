$(document).ready(function(){

});

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
					data = JSON.parse(data);
					var result = data['result'];
					if (result == "成功") {
						window.location.reload();
					} else {
						alert(result);
					}
				}
			});
			break;
		}
		//申请
		case 2:{
			break;
		}
		//发送站内信
		case 3:{
			var recver = $("#sg_recver").val().replace(/( )/g, "").split(";");
			var title = $("#sg_title").val();
			var text = $("#sg_text").val();
			var yes = true;
			$.ajax({
				url: "/message/",
				type: "POST",
				data: {"op": "check_recver", "recver": JSON.stringify(recver)},
				success: function(data) {
					data = JSON.parse(data);
					var result = data['result'];
					if (result != 'yes') {
						alert(result);
						yes = false;
					}
				}
			});
			if (!yes) break;
			$.ajax({
				url: "/message/",
				type: "POST",
				data: {"op": "send_message", "recver": JSON.stringify(recver), "title": title, "text": text},
				success: function(data) {
					data = JSON.parse(data);
					alert("发送成功！");
				}
			});
			break;
		}
		//阅读站内信
		case 4:{

			break;
		}
	}
	$("#myModal").modal('hide');
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
			data = JSON.parse(data);
			window.location.reload();
		}
	});
}

function apply(){
	$(".modal-dialog").width(250);
	$("#myModal_body").empty();
	$("#myModalLabel").text("申请权限");
	var HTMLContent = "<select id=\"apply_authority_select_1\" class=\"form-control\">"
        				+"<option>申请校管理员</option>"
       					+"<option>申请院系级管理员</option>"
        				+"<option>申请班团级管理员</option>"
        				+"<option>申请团支部成员</option>"
    					+"</select><br>";
    $("#myModal_body").append(HTMLContent);
    var HTMLContent = "<select id=\"apply_authority_select_2\" class=\"form-control\">"
    					+"<option>计算机系</option>"
    					+"<option>建筑学院</option>"
    					+"<option>自动化系</option>"
    					+"</select><br>";
    $("#myModal_body").append(HTMLContent);
    var HTMLContent = "<select id=\"apply_authority_select_3\" class=\"form-control\">"
    					+"<option>计61班</option>"
    					+"<option>计62班</option>"
    					+"<option>计63班</option>"
    					+"</select>";
    $("#myModal_body").append(HTMLContent);
    $(".modal-footer").children("button").eq(1).attr("onclick","commit(2)");

}

function send_message(){
	$(".modal-dialog").width(500);
	$("#myModal_body").empty();
	$("#myModalLabel").text("发送新消息");
	$("#myModelYes").text("发送");
	$("#myModal_body").append("<input class=\"form-control\" id=\"sg_recver\" type=\"text\" placeholder=\"收件人（用分号隔开）\"/><br/>");
	$("#myModal_body").append("<input class=\"form-control\" id=\"sg_title\" type=\"text\" placeholder=\"标题\"/><br/>");
	$("#myModal_body").append("<textarea class=\"form-control\" id=\"sg_text\" style=\"height:300px\" placeholder=\"正文\"/><br/>");
	$(".modal-footer").children("button").eq(1).attr("onclick","commit(3)");
}

function read_message(b){
	$b = $(b);
	var message_title = $b.text();
	$("#myModalLabel").text(message_title);
	$(".modal-footer").children("button").eq(1).attr("onclick","commit(4)");

}