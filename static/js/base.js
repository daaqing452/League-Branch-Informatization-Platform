function login(){
	$(".modal-dialog").width(250);
	$("#myModal_body").empty();
	$("#myModalLabel").text("登录");
	$("#myModal_body").append("<input class=\"form-control\" id=\"username\" type=\"text\" name=\"username\" placeholder=\"学号\"><br/>")
	$("#myModal_body").append("<input class=\"form-control\" id=\"password\" type=\"password\" name=\"password\" placeholder=\"密码\">")
	$(".modal-footer").children("button").eq(1).attr("onclick","commit(1)");
}

function commit(flag){
	switch(flag){
		//登录
		case 1:{
			var username = $("#username").val();
			var password = $("#password").val();
			break;
		}
		//申请
		case 2:{

			break;
		}
		case 3:{

			break;
		}
	}
	$("#myModal").modal('hide');
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
    					+"</select><br>"
    $("#myModal_body").append(HTMLContent);
    var HTMLContent = "<select id=\"apply_authority_select_2\" class=\"form-control\">"
    					+"</select><br>"
    $("#myModal_body").append(HTMLContent);
    var HTMLContent = "<select id=\"apply_authority_select_3\" class=\"form-control\">"
    					+"</select>"
    $("#myModal_body").append(HTMLContent);
    $(".modal-footer").children("button").eq(1).attr("onclick","commit(2)");

}

function mail(){
	$(".modal-dialog").width(500);
	$("#myModal_body").empty();
	$("#myModalLabel").text("站内信");

	$(".modal-footer").children("button").eq(1).attr("onclick","commit(3)");

}