$(document).ready(function(){
	$('#op_list li a').click(function(){
        $('#op_list li').removeClass('active');
        $(this).parent().addClass('active');

   })
});



function review_d(){
	$(".modal-dialog").width(250);
	$("#myModal_body").empty();
	$("#myModalLabel").text("审阅院系工作手册");
	var s = "<select id=\"year\" class=\"form-control\" onchange=\"review_year_onchange()\">";
	for (var i = 0; i < years.length; i++) s += "<option>" + years[i] + "</option>";
	$("#myModal_body").append(s + "</select><br/>");
	$('#myModal_body').append("<div id=\"handbook_url\"></div>");
	$(".modal-footer").empty();
	$(".modal-footer").append("<button class='btn btn-default' onclick='commit(0)'>取消</button>");
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
	$("#myModalLabel").text("甲团名额分配");
	var s = "<select id=\"year\" class=\"form-control\" onchange=\"jiatuan_year_onchange()\">";
	for (var i = 0; i < years.length; i++) s += "<option>" + years[i] + "</option>";
	$("#myModal_body").append(s + "</select><br/>");
	$("#myModal_body").append("设置截止时间：<input id='deadline' type='text' style='width:85%' />");
	$("#myModal_body").append("<hr/>")
	$("#myModal_body").append("<div id='minge_div'></div><br/>");
	$(".modal-footer").empty();
	$(".modal-footer").append("<button class='btn btn-default' onclick='commit(0)'>取消</button>");
	$(".modal-footer").append("<button class='btn btn-primary' onclick='commit(10)'>分配名额</button>")
	$(".modal-footer").append("<button class='btn btn-success' onclick='jiatuan_approve()'>批准</button>");
	jiatuan_year_onchange();
}

function submit_apportion() {
	var year = $("#year").val();
	var n = $("#minge").attr("length");
	var minges = new Array();
	var yes = true;
	var info = "";
	for (var i = 0; i < n; i++) {
		var input = $("#minge-" + i);
		var did = input.attr("did");
		var value = input.val();
		if (value == "") value = "0";
		value = parseInt(value);
		if (isNaN(value)) yes = false;
		minges.push({"did": did, "value": value});
		if (value > 0) {
			info += input.attr("department_name") + "：" + value + "\n";
		}
	}
	var deadline = $("input#deadline").val();
	if (!yes) {
		alert("名额不合法");
		return;
	}
	if (confirm(info + "确定分配？")) {
		$.ajax({
			url: "/index/",
			type: "POST",
			data: {"op" : "submit_apportion", "year": year, "deadline": deadline, "minges": JSON.stringify(minges)},
			success: function(data) {
				var data = JSON.parse(data);
				alert("分配成功");
				$("#myModal").modal('hide');
			}
		});
	}
}

function jiatuan_year_onchange() {
	var year = $("#year").val();
	var div = $("#minge_div");
	div.empty();
	$.ajax({
		url: window.location.href,
		type: "POST",
		data: {"op" : "get_apportion", "year": year},
		success: function(data) {
			var data = JSON.parse(data);
			var departments = data["departments"];
			$('input#deadline').val(data['deadline']);
			div.append("<table id='minge' length='" + departments.length + "'><tr>");
			for (var i = 0; i < departments.length; i++) {
				var department = departments[i];
				var s = "<td width='180' style='padding-bottom:20px'>";
				var minge = "";
				if (department['minge'] > 0) minge = department['minge'];
				s += "<input style='width:20px' type='text' id='minge-" + i + "' did=" + department['did'] + " value='" + minge + "' department_name='" + department["name"] + "'/>";
				s += department["name"] + "<br/>";
				if (department.hasOwnProperty("jiatuans")) {
					var jiatuans = department['jiatuans'];
					for (var j = 0; j < jiatuans.length; j++) {
						var jiatuan = jiatuans[j];
						s += "<div style=\"font-size:10px\">";
						s += "<input type='checkbox' bid='" + jiatuan["bid"] + "' branch_name='" + jiatuan["name"] + "' ";
						if (jiatuan["approved"]) s += "checked='checked' disabled='disabled'";
						s += "/> ";
						s += jiatuan["name"] + " ";
						s += "<a href=\"" + jiatuan['material'] + "\">材料</a> ";
						if (jiatuan.hasOwnProperty("handbook")) {
							s += "<a href=\"" + jiatuan['handbook'] + "\">手册</a>" 
						} else {
							s += "手册";
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
	$("#myModalLabel").text("导入院系管理员名单");
	$('#myModal_body').append("\
		<form enctype='multipart/form-data' action='/index/' method='post' style=‘margin:0px;display:inline;’> \
			<input type='file' class='btn btn-sm' name='upload' style='margin:0px;display:inline;'> \
			<input type='submit' value='上传名单' class='btn btn-info btn-sm' > \
		</form> \
		<br/> \
		<br/> \
		导入模板<a href='/static/file/department_admin.csv'>下载</a> \
	");
	$(".modal-footer").empty();
	$(".modal-footer").append("<button class='btn btn-default' onclick='commit(0)'>取消</button>");
}

function jiatuan_approve() {
	var year = $("#year").val();
	var approve_jiatuans = new Array();
	var info = "确认批准支部\n";
	$("input:checked[disabled!='disabled']").each(function() {
		var input = $(this);
		approve_jiatuans.push(input.attr("bid"));
		info += input.attr("branch_name") + "\n";
	});
	info += "为甲级团支部吗？";
	if (confirm(info)) {
		$.ajax({
			url: window.location.href,
			type: "POST",
			data: {"op" : "approve", "year": year, "jiatuans": JSON.stringify(approve_jiatuans)},
			success: function(data) {
				alert("操作成功");
				$("#myModal").modal('hide');
			}
		});
	}
}
