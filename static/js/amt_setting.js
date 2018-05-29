$(document).ready(function(){

});

function add_d(){
	$(".modal-dialog").width(250);
	$("#myModal_body").empty();
	$("#myModalLabel").text("添加院系");
	$("#myModal_body").append("<input class=\"form-control\" id=\"departmentname\" type=\"text\"  placeholder=\"院系名\"/><br/>");
	$(".modal-footer").children("button").eq(1).attr("onclick","commit(5)");
}

function add_b(){
	$(".modal-dialog").width(250);
	$("#myModal_body").empty();
	$("#myModalLabel").text("添加团支部");
	$("#myModal_body").append("<input class=\"form-control\" id=\"branchname\" type=\"text\"  placeholder=\"支部名\"/><br/>");
	$(".modal-footer").children("button").eq(1).attr("onclick","commit(6)");
}

function load_branch() {
	$("#myModal_body").empty();
	$("#myModalLabel").text("导入团支部列表");
	$('#myModal_body').append("\
		<form enctype='multipart/form-data' action='" + window.location.pathname + "' method='post' style=‘margin:0px;display:inline;’> \
			<input type='hidden' name='csrfmiddlewaretoken' value='" + $('#csrf_token').val() + "'> \
			<input type='file' class='btn btn-sm' name='upload' style='margin:0px;display:inline;'> \
			<input type='submit' value='上传列表' class='btn btn-info btn-sm' > \
		</form> \
		<br/> \
		<br/> \
		导入模板<a href='/static/file/branch_name.csv'>下载</a> \
	");
	$(".modal-footer").children("button").eq(1).attr("onclick","commit()");
}

function rename(node) {
	var dbid = $(node).parents("tr").eq(0).attr("dbid");
	var name = $(node).html();
	var new_name = prompt('重命名', '');
	if (new_name == null) new_name = name;
	if (new_name == '') new_name = name;
	$.ajax({
		url: window.location.href,
		type: 'POST',
		data: {'op': 'rename', 'dbid': dbid, 'name': new_name},
		success: function(data) {
			var data = JSON.parse(data);
			window.location.reload();
		}
	});
}

function updown(node, direction) {
	var dbid = $(node).parents("tr").eq(0).attr("dbid");
	$.ajax({
		url: window.location.href,
		type: 'POST',
		data: {'op': 'updown', 'direction': direction, 'dbid': dbid},
		success: function(data) {
			var data = JSON.parse(data);
			window.location.reload();
		}
	});
}

function remove(node) {
	var dbid = $(node).parents("tr").eq(0).attr("dbid");
	if (confirm('确认删除？')) {
		$.ajax({
			url: window.location.href,
			type: 'POST',
			data: {'op': 'remove', 'dbid': dbid},
			success: function(data) {
				var data = JSON.parse(data);
				window.location.reload();
			}
		});
	}
}