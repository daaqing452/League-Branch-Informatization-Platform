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
	$(".modal-dialog").width(800);
	$("#myModal_body").empty();
	$("#myModalLabel").text("确定校甲团支部");
	var s = "<select id=\"year\" class=\"form-control\" onchange=\"jiatuan_year_onchange()\">";
	for (var i = 0; i < years.length; i++) s += "<option>" + years[i] + "</option>";
	$("#myModal_body").append(s + "</select><br/>");
	$("#myModal_body").append("<h4>甲团名额：<span id='minge'></span><h4>");
	$("#myModal_body").append("<span id='submitted_branch'></span><br/><br/>");
	$("#myModal_body").append("<div id='minge_div'></div><br/>");
	$(".modal-footer").empty();
	$(".modal-footer").append("<button class='btn btn-default' onclick='commit(0)'>取消</button>");
	$(".modal-footer").append("<button class='btn btn-primary' id='inform' onclick='jiatuan_inform()'>通知甲团</button>");
	$(".modal-footer").append("<button class='btn btn-success' onclick='commit(11)'>向校级提交</button>");
	jiatuan_year_onchange();

	/*$("#myModal_body").append("<hr/>");
	$("#myModal_body").append("<input class=\"form-control\" id=\"news_title\" type=\"text\" placeholder=\"标题\"/><br/>");
	$("#myModal_body").append("<textarea  name=\"sg_text\" id=\"news_text\"></textarea><br/>");
	$("#myModelYes").text("提交");
	editor = KindEditor.create('textarea[name="sg_text"]', {
        resizeType : 1,
        allowPreviewEmoticons : false,
        allowImageRemote : false,
        useContextmenu : false,
        uploadJson : '/uploadFile/',
        width : '100%',
        items : [
            'insertfile']
    });*/
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
			$('span#submitted_branch').text("已提交支部：");
			var submitted_branch_num = 0;

			var branchs = data["branchs"];
			div.append("<table id='minge' length='" + branchs.length + "'><tr>");
			for (var i = 0; i < branchs.length; i++) {
				var branch = branchs[i];
				var s = "<td width='150'><input type='checkbox' id='minge-" + i + "' bid='" + branch['bid'] + "' onclick='branch_checkbox_onclick()' branch_name='" + branch["name"] + "' ";
				if (data['assigned']) {
					if (assigned_branchs.indexOf(''+branch["bid"]) != -1) s += "checked='checked' ";
				} else {
					s += "disabled=true ";
				}
				s += "/> ";
				if (branch.hasOwnProperty("material")) {
					s += "<a href='" + branch["material"] + "'>" + branch["name"] + "</a></td>";
					$('span#submitted_branch').append(branch["name"] + ", ");
					submitted_branch_num += 1;
				} else {
					s += branch["name"] + "</td>";
				}
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
			if (submitted_branch_num == 0) $('span#submitted_branch').empty();
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
			}
		});
	}
}

function submit_jiatuan_to_school() {
	var year = $("#year").val();
	if (confirm("确认向校级提交？")) {
		$.ajax({
			url: window.location.href,
			type: "POST",
			data: {"op": "submit_jiatuan_to_school", "year": year},
			success: function(data) {
				var data = JSON.parse(data);
				if (data["info"] = "yes") {
					alert("提交成功！");
				} else {
					alert(data["info"]);
				}
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