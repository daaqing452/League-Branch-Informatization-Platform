$(document).ready(function(){
	

});


function add_b(){
	$(".modal-dialog").width(250);
	$("#myModal_body").empty();
	$("#myModalLabel").text("添加团支部");
	$("#myModal_body").append("<input class=\"form-control\" id=\"branchname\" type=\"text\"  placeholder=\"支部名\"/><br/>");
	$(".modal-footer").children("button").eq(1).attr("onclick","commit(6)");
}

function review_b(){
	$(".modal-dialog").width(250);
	$("#myModal_body").empty();
	$("#myModalLabel").text("审阅团支部工作手册");
	$("#myModal_body").append("<select id=\"review_year\" class=\"form-control\" onchange=\"review_year_onchange()\">"
		+"<option>2017</option>"
		+"<option>2018</option>"
		+"</select><br/>");
	$('#myModal_body').append("<div id=\"handbook_url\"></div>");
	$(".modal-footer").children("button").eq(1).attr("onclick","commit(7)");
	review_year_onchange();
}

function review_year_onchange() {
	var year = $("#review_year").val();
	var div = $("#handbook_url");
	div.empty();
	var url = window.location.href;
	var reg = url.match("department/\\d+/")[0];
	var did = parseInt(reg.substr(11, reg.length-12));
	$.ajax({
		url: "/handbook/b/0/",
		type: "POST",
		data: {"op": "get_handbook_list", "year": year, "did": did},
		success: function(data) {
			var data = JSON.parse(data);
			var handbooks = data['handbooks'];
			for (var i in handbooks) {
				var handbook = handbooks[i];
				div.append("<a href='/handbook/" + handbook['hid'] + "/'>" + handbook['title'] + "</a>");
			}
		}
	});
}