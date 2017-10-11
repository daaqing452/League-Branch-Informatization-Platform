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
	var s = "<select id=\"year\" class=\"form-control\" onchange=\"review_year_onchange()\">";
	for (var i = 0; i < years.length; i++) s += "<option>" + years[i] + "</option>";
	$("#myModal_body").append(s + "</select><br/>");
	$('#myModal_body').append("<div id=\"handbook_url\"></div>");
	$(".modal-footer").children("button").eq(1).attr("onclick","commit(7)");
	review_year_onchange();
}

function review_year_onchange() {
	var year = $("#year").val();
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
				div.append("<a href='/handbook/" + handbook['hid'] + "/'>" + handbook['title'] + "</a><br/>");
			}
		}
	});
}

function jiatuan() {
	$(".modal-dialog").width(800);
	$("#myModal_body").empty();
	$("#myModalLabel").text("甲团");
	var s = "<select id=\"year\" class=\"form-control\" onchange=\"jiatuan_year_onchange()\">";
	for (var i = 0; i < years.length; i++) s += "<option>" + years[i] + "</option>";
	$("#myModal_body").append(s + "</select><br/>");
	$("#myModal_body").append("设置截止时间");
	$("#myModal_body").append("<hr/>")
	$("#myModal_body").append("<div id='minge_div'></div><br/>");
	//$("#myModal_body").append("<div align='left'><button class='btn btn-primary' onclick='submit_minge()'>分配名额</button></div>");
	jiatuan_year_onchange();
	$("#myModelYes").text("分配名额");
	$(".modal-footer").children("button").eq(1).attr("onclick","commit(10)");
}

function submit_minge() {
	var year = $("#year").val();
	var n = $("#minge").attr("length");
	var minges = new Array();
	var yes = true;
	for (var i = 0; i < n; i++) {
		var input = $("#minge-" + i);
		var did = input.attr("did");
		var value = input.val();
		if (value == "") value = "0";
		value = parseInt(value);
		if (isNaN(value)) yes = false;
		minges.push({"did": did, "value": value});
	}
	if (!yes) {
		alert("名额不合法");
		return;
	}
	$.ajax({
		url: "/index/",
		type: "POST",
		data: {"op" : "submit_minge", "year": year, "minges": JSON.stringify(minges)},
		success: function(data) {
			var data = JSON.parse(data);
			alert("分配成功");
			$("#myModal").modal('hide');
		}
	});
}

function jiatuan_year_onchange() {
	var year = $("#year").val();
	var div = $("#minge_div");
	div.empty();
	$.ajax({
		url: window.location.href,
		type: "POST",
		data: {"op" : "get_departments_jiatuan", "year": year},
		success: function(data) {
			var data = JSON.parse(data);
			var departments = data["departments"];
			div.append("<table id='minge' length='" + departments.length + "'><tr>");
			for (var i = 0; i < departments.length; i++) {
				var department = departments[i];
				var s = "<td width='180' style='padding-bottom:20px'>"
				s += "<input style='width:20px' type='text' id='minge-" + i + "' did='" + department['did'] + "'/>";
				s += department["name"] + "<br/>";
				if (department.hasOwnProperty("jiatuans")) {
					var jiatuans = department['jiatuans'];
					for (var j = 0; j < jiatuans.length; j++) {
						var jiatuan = jiatuans[j];
						s += "<div style=\"font-size:5px\">" + jiatuan["name"] + " ";
						s += "<a href=\"" + jiatuan['material'] + "\">材料</a> ";
						if (jiatuan.hasOwnProperty("handbook")) {
							s += "<a href=\"" + jiatuan['handbook'] + "\">手册</a>" 
						} else {
							s += "工作手册";
						}
						s += "</div>";
					}
				}
				div.append(s);
				if ((i + 1) % 5 == 0) {
					div.append("</tr><tr>");
				}
			}
			div.append("</tr></table>");
		}
	});
}

function load_admin() {
	$("#myModal_body").empty();
	$("#myModalLabel").text("导入校级管理员名单");
	$('#myModal_body').append("\
		<form enctype='multipart/form-data' action='/index/' method='post' style=‘margin:0px;display:inline;’> \
			<input type='file' class='btn btn-sm' name='upload' style='margin:0px;display:inline;'> \
			<input type='submit' value='上传名单' class='btn btn-info btn-sm' > \
		</form> \
	");
	$(".modal-footer").children("button").eq(1).attr("onclick","commit(13)");
}