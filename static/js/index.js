$(document).ready(function(){
	
	$("button#login").click(function(){
		var username = $("input#username").val();
		var password = $("input#password").val();
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
		})
	});

	$("#logout").click(function(){
		$.ajax({
			url: "/index/",
			type: "POST",
			data: {"op": "logout"},
			success: function(data) {
				data = JSON.parse(data);
				window.location.reload();
			}
		})
	})
});