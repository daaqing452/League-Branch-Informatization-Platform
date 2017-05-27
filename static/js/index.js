$(document).ready(function(){
	
	$("button#add_department").click(function(){
		var name = prompt("院系名", "");
		$.ajax({
			url: window.location.href,
			type: "POST",
			data: {"op": "add_department", "name": name},
			success: function(data) {
				data = JSON.parse(data);
				alert("添加成功！");
				window.location.reload();
			}
		});
	});
	
});