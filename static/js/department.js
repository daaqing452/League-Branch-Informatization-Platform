$(document).ready(function(){
	

});


function add_b(){
	$(".modal-dialog").width(250);
	$("#myModal_body").empty();
	$("#myModalLabel").text("添加团支部");
	$("#myModal_body").append("<input class=\"form-control\" id=\"branchname\" type=\"text\"  placeholder=\"支部名\"/><br/>");
	$(".modal-footer").children("button").eq(1).attr("onclick","commit(6)");
}
