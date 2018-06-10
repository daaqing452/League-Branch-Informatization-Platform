$(document).ready(function(){

});

function add_year() {
	var new_year = prompt("新的年份", '');
	var num_pat = new RegExp("^[1-9][0-9]{3}$");
	if (num_pat.test(new_year) == false) {
		alert("年份必须是1000到9999之间的整数！")
		return;
	}
	new_year = Number(new_year);
	if (years.indexOf(new_year) >= 0) {
		alert("年份已存在！");
		return;
	}
	$.ajax({
		url: window.location.href,
		type: "POST",
		data: {"op": "add_year", "new_year": new_year},
		success: function(data) {
			var data = JSON.parse(data);
			alert("添加成功！");
			window.location.reload();
		}
	});
}

function delete_year() {
	var year = $("select#years").val();
	if (confirm("是否删除年份 " + year)) {
		$.ajax({
			url: window.location.href,
			type: "POST",
			data: {"op": "delete_year", "year": year},
			success: function(data) {
				var data = JSON.parse(data);
				alert("删除成功！");
				window.location.reload();
			}
		});
	}
}

function delete_admin_school(node) {
	var span = $(node);
	var sid = span.attr("sid");
	if (confirm("确认要取消该校级管理员权限？")) {
		$.ajax({
			url: window.location.href,
			type: "POST",
			data: {"op": "delete_admin_school", "sid": sid},
			success: function(data) {
				var data = JSON.parse(data);
				alert(data['info']);
				window.location.reload();
			}
		});
	}
}