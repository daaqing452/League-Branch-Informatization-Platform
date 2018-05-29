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
	$(".modal-footer").children("button").eq(1).attr("onclick","commit(7)");
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
	$("#myModalLabel").text("甲团");
	var s = "<select id=\"year\" class=\"form-control\" onchange=\"jiatuan_year_onchange()\">";
	for (var i = 0; i < years.length; i++) s += "<option>" + years[i] + "</option>";
	$("#myModal_body").append(s + "</select><br/>");
	$("#myModal_body").append("<div id='minge_div'></div><br/>");
	$("#myModal_body").append("<div align='left'><button class='btn btn-primary' onclick='jiatuan_inform()'>通知甲团</button></div>");
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
	$(".modal-footer").children("button").eq(1).attr("onclick","commit(11)");
}

function jiatuan_year_onchange() {
	var year = $("#year").val();
	var div = $("#minge_div");
	var urlInfo = getUrlInfo();
	div.empty();
	$.ajax({
		url: window.location.href,
		type: "POST",
		data: {"op" : "get_branchs_jiatuan", "year": year},
		success: function(data) {
			var data = JSON.parse(data);
			var branchs = data["branchs"];
			div.append("<table id='minge' length='" + branchs.length + "'><tr>");
			for (var i = 0; i < branchs.length; i++) {
				var branch = branchs[i];
				var s = "<td width='150'><input type='checkbox' id='minge-" + i + "' bid='" + branch['bid'] + "'/> ";
				if (branch.hasOwnProperty("material")) {
					s += "<a href='" + branch["material"] + "'>" + branch["name"] + "</a></td>";
				} else {
					s += branch["name"] + "</td>";
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

function jiatuan_inform() {
	var year = $("#year").val();
	var n = $("#minge").attr("length");
	var jiatuans = new Array();
	for (var i = 0; i < n; i++) {
		var input = $("#minge-" + i);
		var bid = input.attr("bid");
		if (input.prop("checked")) jiatuans.push(bid);
	}
	$.ajax({
		url: window.location.href,
		type: "POST",
		data: {"op" : "jiatuan_inform", "year": year, "jiatuans": JSON.stringify(jiatuans)},
		success: function(data) {
			var data = JSON.parse(data);
			alert("通知甲团成功");
		}
	});
}

function load_branch() {
	$("#myModal_body").empty();
	$("#myModalLabel").text("导入团支部列表");
	$('#myModal_body').append("\
		<form enctype='multipart/form-data' action='" + window.location.pathname + "' method='post' style=‘margin:0px;display:inline;’> \
			<input type='hidden' name='csrfmiddlewaretoken' value='" + $('#csrf_token').val() + "'> \
			<input type='file' class='btn btn-sm' name='upload' style='margin:0px;display:inline;'> \
			<input type='submit' value='上传列表' class='btn btn-info btn-sm' > \
		</form> \
		<br/> \
		<br/> \
		导入模板<a href='/static/file/branch_name.csv'>下载</a> \
	");
	$(".modal-footer").children("button").eq(1).attr("onclick","commit()");
}