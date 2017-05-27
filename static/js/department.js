$(document).ready(function(){
	
	$("button#add_branch").click(function(){
		var name = prompt('团支部名', '');
		$.ajax({
			url: window.location.href,
			type: "POST",
			data: {"op": "add_branch", "name": name},
			success: function(data) {
				data = JSON.parse(data);
				alert("添加成功！");
				window.location.reload();
			}
		});
	});
	
});