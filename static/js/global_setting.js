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
	})
}