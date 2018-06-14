var editor;
var tip;
$(document).ready(function(){
    var url_arr = window.location.href.split("/");
    var hid = url_arr[url_arr.length-2];
    $.ajax({
        url: window.location.href,
        type: 'POST',
        data: {'op': 'load','hid': hid},
        success: function(data) {
            var data = JSON.parse(data);
            var status = data['released'];
            tip = {title:data['title'],content:data['content'],attachment:data['attachment']}
            if(status == false){
                fill_content(0);
            }
            else{
                fill_content(1);
            }
        }
    });
	
});

function fill_content(flag){
    if(flag == 0){
        $("#save").show();
        $("#release").hide();
        editor = KindEditor.create('textarea[id="tip_text"]', {
        resizeType : 1,
        allowPreviewEmoticons : false,
        allowImageRemote : false,
        useContextmenu : false,
        uploadJson : '/uploadFile/',
        width : '100%',
        height : '400px',
        items : [
            'fontname', 'fontsize', '|', 'forecolor', 'hilitecolor', 'bold', 'italic', 'underline',
            'removeformat', '|', 'justifyleft', 'justifycenter', 'justifyright', 'insertorderedlist',
            'insertunorderedlist', '|', 'emoticons', 'image','insertfile']
        });
        $("#title").val(tip.title);
        editor.html(tip.content);
        if(tip.attachment == "[]"){
            return;
        }
        var attachment_list = tip.attachment.substring(1,tip.attachment.length-1).split(", ");
        len = attachment_list.length;
        for(var i = 0; i < len; i++){
            var real_url = attachment_list[i].substring(1,attachment_list[i].length-1);
            var title = real_url.substring(22);
            $('#attachment_list').append('<div class=\"attachment\"><a href=\"'+real_url + '\" title=\"'+title+'\">'+title+'</a>&nbsp<a onclick=\"del_line(this)\">取消</a></div>');
        }
    }
    else{
        $("#save").hide();
        $("#release").show();
        $("#tip_title").text(tip.title);
        $("#tip_content").html(tip.content);
        var attachment_list = tip.attachment.substring(1,tip.attachment.length-1).split(", ");
        len = attachment_list.length;
        if(tip.attachment == "[]"){
            return;
        }
        for(var i = 0; i < len; i++){
            var real_url = attachment_list[i].substring(1,attachment_list[i].length-1);
            var title = real_url.substring(22);
            $('#tip_attachment_list').append('<div class=\"attachment\"><a href=\"'+real_url + '\" title=\"'+title+'\">'+title+'</a></div>');
        }
    }
}

function del_line(b){
	$b = $(b);
	$b.parents("div").eq(0).remove();
}

function get_content(){
	var tip = {title:$("#title").val()};
	tip.html = editor.html();
	var length = $("#attachment_list").children("div").length;
	tip.attachments = []
	for(var i = 0; i < length; i++){
		tip.attachments.push($("#attachment_list").children("div").eq(i).children("a").eq(0).attr("href"));
	}
	return tip;
}

function save(){
	tip = get_content();
	tip_string = JSON.stringify(tip);
	$.ajax({
		url: window.location.href,
        type: 'POST',
        data: {'op': 'save', 'tip': tip_string},
        success: function(data) {
        	var data = JSON.parse(data);
        	alert('暂存成功');
        }
	});
	return;
}

function submit(){
	tip = get_content();
	tip_string = JSON.stringify(tip);
	$.ajax({
		url: window.location.href,
        type: 'POST',
        data: {'op': 'release', 'tip': tip_string},
        success: function(data) {
        	var data = JSON.parse(data);
        	alert('发布成功');
            window.location.href = '/case_study/';
        }
	});
	return;
}