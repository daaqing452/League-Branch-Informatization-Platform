$(document).ready(function(){
	$('#op_list li a').click(function(){
        $('#op_list li').removeClass('active');
        $(this).parent().addClass('active');

   })
});



function add_d(){
	
	$(".modal-dialog").width(250);
	$("#myModal_body").empty();
	$("#myModalLabel").text("添加院系");
	$("#myModal_body").append("<input class=\"form-control\" id=\"departmentname\" type=\"text\"  placeholder=\"院系名\"/><br/>");
	$(".modal-footer").children("button").eq(1).attr("onclick","commit(5)");
}

function review_d(){
	
	$(".modal-dialog").width(250);
	$("#myModal_body").empty();
	$("#myModalLabel").text("审阅院系工作手册");
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
	$.ajax({
		url: "/handbook/d/0/",
		type: "POST",
		data: {"op": "get_handbook_list", "year": year},
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

function jiatuan() {
	$(".modal-dialog").width(250);
	$("#myModal_body").empty();
	$("#myModalLabel").text("甲团");
	$('#myModal_body').append("");
	$(".modal-footer").children("button").eq(1).attr("onclick","commit(7)");
	review_year_onchange();
}