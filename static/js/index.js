$(document).ready(function(){
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

function release_n(){
	$(".modal-dialog").width(500);
	$("#myModal_body").empty();
	$("#myModalLabel").text("发布新闻");
	$("#myModelYes").text("发布");
	$("#myModal_body").append("<input class=\"form-control\" id=\"news_title\" type=\"text\" placeholder=\"标题\"/><br/>");
	$("#myModal_body").append("<textarea  name=\"sg_text\" id=\"news_text\"></textarea><br/>");
	$(".modal-footer").children("button").eq(1).attr("onclick","commit(3)");
	editor = KindEditor.create('textarea[name="sg_text"]', {
        resizeType : 1,
        allowPreviewEmoticons : false,
        allowImageRemote : false,
        useContextmenu : false,
        uploadJson : '/uploadFile/',
        width : '100%',
        items : [
            'fontname', 'fontsize', '|', 'forecolor', 'hilitecolor', 'bold', 'italic', 'underline',
            'removeformat', '|', 'justifyleft', 'justifycenter', 'justifyright', 'insertorderedlist',
            'insertunorderedlist', '|', 'emoticons', 'image']
    });
    $(".modal-footer").children("button").eq(1).attr("onclick","commit(8)");
}