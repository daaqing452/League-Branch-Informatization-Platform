$(document).ready(function(){
	$('#op_list li a').click(function(){
        $('#op_list li').removeClass('active');
        $(this).parent().addClass('active');

   })
});

function jiatuan() {
	$(".modal-dialog").width(800);
	$("#myModal_body").empty();
	$("#myModalLabel").text("甲团");
	var s = "<select id=\"year\" class=\"form-control\" onchange=\"jiatuan_year_onchange()\">";
	for (var i = 0; i < years.length; i++) s += "<option>" + years[i] + "</option>";
	$("#myModal_body").append(s + "</select><br/>");
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
    });
	$(".modal-footer").children("button").eq(1).attr("onclick","commit(12)");
}

function jiatuan_year_onchange() {
}

function load_member() {
	$("#myModal_body").empty();
	$("#myModalLabel").text("导入班级成员名单");
	$('#myModal_body').append("\
		<form enctype='multipart/form-data' action='" + window.location.pathname + "' method='post' style=‘margin:0px;display:inline;’> \
			<input type='hidden' name='csrfmiddlewaretoken' value='" + $('#csrf_token').val() + "'> \
			<input type='file' class='btn btn-sm' name='upload' style='margin:0px;display:inline;'> \
			<input type='submit' value='上传名单' class='btn btn-info btn-sm' > \
		</form> \
		<br/> \
		<br/> \
		导入模板<a href='/static/file/branch_member.csv'>下载</a> \
	");
	$(".modal-footer").children("button").eq(1).attr("onclick","commit()");
}