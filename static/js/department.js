$(document).ready(function(){
	$('#op_list li a').click(function(){
        $('#op_list li').removeClass('active');
        $(this).parent().addClass('active');

   })
});

function review_b(){
	$(".modal-dialog").width(250);
	$("#myModal_body").empty();
	$("#myModalLabel").text("审阅团支部工作手册");
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
				div.append("<a href='/handbook/" + handbook['hid'] + "/'>" + handbook['title'] + "</a><br/>");
			}
		}
	});
}

function jiatuan() {
	$(".modal-dialog").width(600);
	$("#myModal_body").empty();
	$("#myModalLabel").text("确定校甲团支部");
	var s = "<select id=\"year\" class=\"form-control\" onchange=\"jiatuan_year_onchange()\">";
	for (var i = 0; i < years.length; i++) s += "<option>" + years[i] + "</option>";
	$("#myModal_body").append(s + "</select><br/>");
	$("#myModal_body").append("<h4>甲团名额：<span id='minge'></span><h4>");
	$("#myModal_body").append("<span id='submitted_branch'></span><br/>");
	$("#myModal_body").append("<span id='delivered_branch'></span><br/>");
	$("#myModal_body").append("<span id='approved_branch'></span><br/><br/>");
	$("#myModal_body").append("<div id='minge_div'></div><br/>");
	$(".modal-footer").empty();
	$(".modal-footer").append("<button class='btn btn-default' onclick='commit(0)'>取消</button>");
	$(".modal-footer").append("<button class='btn btn-primary' id='inform' onclick='jiatuan_inform()'>通知甲团</button>");
	$(".modal-footer").append("<button class='btn btn-success' onclick='commit(11)'>向校级提交</button>");
	jiatuan_year_onchange();
}

var max_minge = 0;

function jiatuan_year_onchange() {
	var year = $("#year").val();
	var div = $("#minge_div");
	var urlInfo = getUrlInfo();
	div.empty();
	$.ajax({
		url: window.location.href,
		type: "POST",
		data: {"op" : "get_jiatuan_branchs", "year": year},
		success: function(data) {
			var data = JSON.parse(data);
			var status = data['status'];
			if (status == 0) {
				$('span#minge').text("");
				alert("甲团评选尚未开始！");
				return;
			}
			if (status == 2) {
				$('span#minge').text("");
				alert("甲团评选已经结束！");
				return;
			}
			var assigned_branchs;
			if (data['assigned']) {
				assigned_branchs = JSON.parse(data['assigned_branchs']);
			}
			$('span#minge').text(data["minge"]);
			max_minge = parseInt(data["minge"]);

			if (data['assigned']) {
				$('span#submitted_branch').text("已提交材料的支部：");
				$('span#delivered_branch').text("已送至校级的支部：");
				$('span#approved_branch').text('已批准通过的支部：');
			}

			var branchs = data["branchs"];
			div.append("<table id='minge' length='" + branchs.length + "'><tr>");
			for (var i = 0; i < branchs.length; i++) {
				var branch = branchs[i];
				var s = "<td width='120'>";
				// 已分配甲团，选择向校级提交材料
				if (data['assigned']) {
					// 甲团
					if (assigned_branchs.indexOf(''+branch["bid"]) != -1) {
						s += "<input type='checkbox' id='minge-" + i + "' bid='" + branch['bid'] + "' branch_name='" + branch["name"] + "' ";
						// 已提交材料
						// if (branch.hasOwnProperty("material")) {
						if (branch["submitted"]) {
							if (branch['delivered']) {
								$('span#delivered_branch').append(branch["name"] + ", ");
								s += "disabled='disabled' checked='checked'";
							}
							if (branch['approved']) {
								$('span#approved_branch').append(branch["name"] + ", ");
							}
							s += "/> <a href='" + branch["material"] + "'>" + branch["name"] + "</a>";
							$('span#submitted_branch').append(branch["name"] + ", ");
						// 未提交
						} else {
							s += "disabled='disabled' />" + branch["name"];
						}
					// 非甲团
					} else {
						s += "<span style='text-decoration:line-through'>" + branch["name"] + "</span>";
					}
				// 未分配甲团，选择甲团
				} else {
					s += "<input type='checkbox' id='minge-" + i + "' bid='" + branch['bid'] + "' onclick='branch_checkbox_onclick()' branch_name='" + branch["name"] + "' /> " + branch["name"];
				}
				s += "</td>"
				div.append(s);
				if ((i + 1) % 5 == 0) {
					div.append("</tr><tr>");
				}
			}
			if (data['assigned']) {
				$('button#inform').text("已通知");
				$('button#inform').attr("disabled", "disabled");
				/*if (data['submitted']) {
					$('#myModelYes').text("已向校级提交");
					$('#myModelYes').attr('disabled', 'disabled');
				}*/
			}
			div.append("</tr></table>");
		}
	});
}

function branch_checkbox_onclick() {
	var checked_num = $("input:checked").length;
	if (checked_num >= max_minge) {
		$("input:not(:checked)").attr('disabled', true);
	} else {
		$("input:not(:checked)").attr('disabled', false);
	}
}

function jiatuan_inform() {
	var year = $("#year").val();
	var jiatuans = new Array();
	var s = "甲团名单：\n";
	$("input:checked").each(function() {
		var input = $(this);
		jiatuans.push(input.attr("bid"));
		s += input.attr("branch_name") + "\n";
	});
	s += "确认通知？";
	if (jiatuans.length != max_minge) {
		alert("支部个数不符合！");
		return;
	}
	if (confirm(s)) {
		$.ajax({
			url: window.location.href,
			type: "POST",
			data: {"op" : "jiatuan_inform", "year": year, "jiatuans": JSON.stringify(jiatuans)},
			success: function(data) {
				var data = JSON.parse(data);
				if (data["info"] == "yes") {
					alert("通知甲团成功");
				} else {
					alert(data["info"]);
				}
				$("#myModal").modal('hide');
			}
		});
	}
}

function deliver_jiatuan() {
	var year = $("#year").val();
	var deliver_jiatuans = new Array();
	var info = "确认向校级提交\n";
	$("input:checked[disabled!='disabled']").each(function() {
		var input = $(this);
		deliver_jiatuans.push(input.attr("bid"));
		info += input.attr("branch_name") + "\n";
	});
	info += "支部的材料吗？";
	if (confirm(info)) {
		$.ajax({
			url: window.location.href,
			type: "POST",
			data: {"op": "deliver", "year": year, "jiatuans": JSON.stringify(deliver_jiatuans)},
			success: function(data) {
				var data = JSON.parse(data);
				if (data["info"] = "yes") {
					alert("提交成功！");
				} else {
					alert(data["info"]);
				}
				$("#myModal").modal('hide');
			}
		});
	}
}


// ???
function jiatuan_submit() {
	var year = $("#year").val();
	var title = $("#news_title").val();
	var text = editor.html();
	var attach_list = new Array();
	for(var i = 0; i < $("div.attachment").length; i ++ ){
		var attach = new Array();
		attach.push($("div.attachment").eq(i).attr("title"));
		attach.push($("div.attachment").eq(i).attr("url"));
		attach_list.push(attach);
	}
	$.ajax({
		url: window.location.href,
		type: "POST",
		data: {"op": "submit_jiatuan_material", "year": year, "title": title, "text": text, "attachment": JSON.stringify(attach_list)},
		success: function(data) {
			var data = JSON.parse(data);
			alert("提交成功");
		}
	});
}