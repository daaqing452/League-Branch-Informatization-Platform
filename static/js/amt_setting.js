$(document).ready(function(){

});

function add_d(){
	$(".modal-dialog").width(250);
	$("#myModal_body").empty();
	$("#myModalLabel").text("添加院系");
	$("#myModal_body").append("<input class=\"form-control\" id=\"departmentname\" type=\"text\"  placeholder=\"院系名\"/><br/>");
	$(".modal-footer").children("button").eq(1).attr("onclick","commit(5)");
}

function rename_d(node) {
	var did = $(node).parents("tr").eq(0).attr("did");
	var name = $(node).html();
	var new_name = prompt('重命名院系名', '');
	if (new_name == null) new_name = name;
	if (new_name == '') new_name = name;
	$.ajax({
		url: window.location.href,
		type: 'POST',
		data: {'op': 'rename_department', 'did': did, 'name': new_name},
		success: function(data) {
			var data = JSON.parse(data);
			window.location.reload();
		}
	});
}