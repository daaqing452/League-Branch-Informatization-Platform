var td_html = "<td><textarea style=\"width: 100%; height: 31px; overflow: auto; resize: none;\"></textarea></td>";
var add_del_html = "<td align=\"center\"><span class=\"glyphicon glyphicon-plus\" onclick=\"addOption(this)\"></span><span class=\"glyphicon glyphicon-minus\" onclick=\"delOption(this)\"></span></td>"


var chapter;
var grade;

$(document).ready(function(){
	$("#chapter_0").parent().eq(0).attr("class","active");
	//$("#content").append("<button class=\"btn btn-primary\" style=\"float: right; width: 100px;\" onclick=\"submit()\">提交</button>");
	for (var i = 0; i < years.length; i++) $("#year").append("<option>" + years[i] + "</option>");
	$("#table_0").show();
	if (!readonly) year_onchange();
});

function load_jiatuan() {
	var jid = $("#main_div").attr("jid");
	$.ajax({
		url: window.location.href,
		type: "POST",
		data: {"op": "load_jiatuan", "jid": jid},
		success: function(data) {
			var data = JSON.parse(data);
			read_only(data["content"]);
		}
	});
}

function year_onchange() {
	var year = $("#year").val();
	$.ajax({
		url: window.location.href,
		type: "POST",
		data: {"op": "load_jiatuan", "year": year},
		success: function(data) {
			var data = JSON.parse(data);
			if (data['info'] == 'yes') {
				$("span#load_info").hide();
				$("div#main_content").show();
				fill_content(data['content']);
				if (data['delivered']) {
					//$("#button_save").hide();
					//$("#button_submit").hide();
					$("#button_save").attr({"disabled":"disabled"});
					$("#button_submit").attr({"disabled":"disabled"});
				} else {
					//$("#button_save").show();
					//$("#button_submit").show();
					$("#button_save").removeAttr("disabled");
					$("#button_submit").removeAttr("disabled");
				}
			} else {
				$("span#load_info").show();
				$("span#load_info").text(data['info']);
				$("div#main_content").hide();
			}
		}
	})
}

function fill_content(content){
	editor1 = KindEditor.create('textarea[name="sg_text"]', {
        resizeType : 1,
        allowPreviewEmoticons : false,
        allowImageRemote : false,
        useContextmenu : false,
        uploadJson : '/uploadFile/',
        width : '100%',
        items : [
            'fontname', 'fontsize', '|', 'forecolor', 'hilitecolor', 'bold', 'italic', 'underline',
            'removeformat', '|', 'justifyleft', 'justifycenter', 'justifyright', 'insertorderedlist',
            'insertunorderedlist']
    });
    editor2 = KindEditor.create('textarea[name="photo"]', {
        resizeType : 1,
        allowPreviewEmoticons : false,
        allowImageRemote : false,
        useContextmenu : false,
        uploadJson : '/uploadFile/',
        width : '100%',
        items : [
            'image']
    });
	if (!content) content = '[[[["1","2"]],[["3","4",""],["","",""],["","",""],["","",""]],[[""]],[[""]],[[""]]],["爱中国"],["/media/20170904122418-ctr_heat_map_page.png","/media/20170904122425-duration_heat_map_row.png"]]';
	var JIATUAN_content = JSON.parse(content);
	var SHENQING_content = JIATUAN_content[0];
	var div = $("#table_0");
	var table_num = div.find("table").length;
	for(var k = 0; k < table_num; k++){
		var TABLE_content = SHENQING_content[k]
		var table = div.find("table").eq(k);
		var tr_num = table.find("tr").length;
		var real_num = tr_num;
		var start_num = 0;
		if(table.find("tr").eq(0).find("textarea").length == 0){
			start_num = 1;
			real_num -= 1;
		}

		if(real_num < TABLE_content.length){
			var tr = table.find("tr").eq(start_num).clone();   
				tr.appendTo(table); 
		}
		for(var m = 0; m < TABLE_content.length; m++){
			var TR_content = TABLE_content[m];
			var textarea_num = TR_content.length;
			var tr = table.find("tr").eq(start_num+m);
			for(var n = 0; n < textarea_num; n++){
				tr.find("textarea").eq(n).val(TR_content[n]);
				tr.find("textarea").eq(n).css("background","");
			}
		}
	}
	var ANLI_content = JIATUAN_content[1];
	var PIC_content = JIATUAN_content[2];
	//editor1.html(ANLI_content[0]);
	//console.log(ANLI_content);
	if(ANLI_content[0] == ""){
		editor1.html("填写说明：<br />&nbsp; &nbsp; 一、 支部工作案例应重点描述该支部最优特色的几方面工作；<br />&nbsp; &nbsp; 二、 工作案例不少于1000字<br />&nbsp; &nbsp; 三、 优秀支部工作案例将用于后期宣传，形成《在集体中成长》中的支部案例素材；<br />&nbsp; &nbsp; 四、 校团委会根据优秀支部工作案例情况择优筛选出优秀支部进行重点支持。<span> </span><br />");
	}
	else{
		editor1.html(ANLI_content[0]);
	}
	var html_content = "照片命名需体现对照片的描述<br/>";
	for(var i = 0; i < PIC_content.length; i++){
		var url = PIC_content[i];
		html_content += '<img name="tuwen" src="' +url + '" data-ke-src="' + url + '" width="30%"/><br/>';
		$("#table_2").append('<div class=\"attachment\" url=\"'+url + '\" title=\"'+url.slice(22)+'\"><a href=\"'+url+'\">'+url.slice(22)+'</a>&nbsp<a onclick=\"del_line(this)\">取消</a><div>');
	}
	//console.log(html_content);
	editor2.html(html_content);
	
}

function read_only(content){
	if (!content) return
	var JIATUAN_content = JSON.parse(content);
	var SHENQING_content = JIATUAN_content[0];
	var div = $("#table_0");
	var table_num = div.find("table").length;

	for(var k = 0; k < table_num; k++){
		var TABLE_content = SHENQING_content[k]
		var table = div.find("table").eq(k);
		var tr_num = table.find("tr").length;
		var real_num = tr_num;
		var start_num = 0;
		if(table.find("tr").eq(0).find("textarea").length == 0){
			start_num = 1;
			real_num -= 1;
		}

		if(real_num < TABLE_content.length){
			var tr = table.find("tr").eq(start_num).clone();   
				tr.appendTo(table); 
		}
		for(var m = 0; m < TABLE_content.length; m++){
			var TR_content = TABLE_content[m];
			var textarea_num = TR_content.length;
			var tr = table.find("tr").eq(start_num+m);
			for(var n = 0; n < textarea_num; n++){
				tr.find("textarea").eq(n).val(TR_content[n]);
				tr.find("textarea").eq(n).attr("disabled", "disabled");
				tr.find("textarea").eq(n).attr("readonly", "readonly");
			}
		}
	}
	KindEditor.remove('textarea[name="sg_text"]');
	KindEditor.remove('textarea[name="photo"]');
	$("#photo_text").hide();
	$(".attachment").remove();
	$("#case_text").remove();
	$("#table_1").append('<div style=\"height: 300px; width: 100%; overflow: auto; resize: none; border:1px solid #ADADAD;\"></div>')
	$("#table_1").find("div").last().append(JIATUAN_content[1][0]);
	var PIC_content = JIATUAN_content[2];
	for(var i = 0; i < PIC_content.length; i++){
		var url = PIC_content[i];
		$("#table_2").append('<img src=\"'+url + '\" title=\"'+url.slice(22)+'\"></img>');
	}
	
}

function all_hind(){
	for(var i = 0; i < 3; i++){
		$("#table_"+i).hide();
	}
}

function module_select(id){
	var length = $("#nav_2").children("li").length;
	chapter = id;
	for(var i = 0; i < length; i++){
		$("#chapter_"+i).parent().eq(0).attr("class","");
	}
	$("#chapter_"+id).parent().eq(0).attr("class","active");
	all_hind();
	$("#table_"+chapter).show();
}



function check_fill(tr,tr_class,textarea_n,content){
	var num_pat = new RegExp("^[0-9][0-9]*$");
	var xuehao_pat = new RegExp("^\\d{10}$");
	var data_pat = new RegExp("^([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8])))$");
	if(tr_class == "jibenxinxi"){
		if(content == ""){
			return "基本信息填写有误(必填项)";
		}
	}

	if(tr_class == "jibenqingkuang"){
		if(content == ""){
			return "基本情况填写有误(必填项)";
		}
	}

	if(tr_class == "jibenyaoqiu"){
		if(content == ""){
			return "基本要求填写有误(必填项)";
		}
	}

	if(tr_class == "zhibushiyeyuwenhua"){
		if(content == ""){
			return "支部事业与文化填写有误(必填项)";
		}
	}

	if(tr_class == "renshu"){
		if(content == ""){
			return "人数填写有误(必填项，无填0)";
		}
		else{
			if(num_pat.test(content) == false){
				return "人数填写有误(非正整数)";
			}
		}
		if(textarea_n == 2){
			tr.find("textarea").eq(2).val(Number(tr.find("textarea").eq(0).val())+Number(tr.find("textarea").eq(1).val()));
		}

	}

	return true;
}

function is_in_array(arr,value){
    for(var i = 0; i < arr.length; i++){
        if(value === arr[i]){
            return true;
        }
    }
    return false;
}

function submit(subtype){
	var JIATUAN_content = new Array();
	var SHENQING_content = new Array();
	wrong_messages = new Array();
	var div = $("#table_"+0);
	var table_num = div.find("table").length;
	for(var k = 0; k < table_num; k++){
		var TABLE_content = new Array();
		var table = div.find("table").eq(k);
		var tr_num = table.find("tr").length;
		for(var m = 0; m < tr_num; m ++){
			var TR_content = new Array();
			var tr = table.find("tr").eq(m);
			var textarea_num = tr.find("textarea").length;
			var already_fill = false;
			if(textarea_num == 0){
				continue;
			}
			else{
				for(var n = 0; n < textarea_num; n++){
					tr.find("textarea").eq(n).css("background","");
					var false_message = check_fill(tr,tr.attr("class"),n,tr.find("textarea").eq(n).val());
					if (subtype == 0) false_message = true;
					if(false_message != true){
						if(is_in_array(wrong_messages,false_message) == false){
							wrong_messages.push(false_message);
						}
						tr.find("textarea").eq(n).css("background","#CCCC99");

					}
					TR_content.push(tr.find("textarea").eq(n).val());
				}
			}
			TABLE_content.push(TR_content);
		}
		SHENQING_content.push(TABLE_content);
	}

	var ANLI_content = new Array();
	ANLI_content.push(editor1.html());
	
	var PIC_content = new Array();

	for(var i = 0; i < $("div.attachment").length; i ++ ){
		PIC_content.push($("div.attachment").eq(i).attr("url"));
	}

	JIATUAN_content.push(SHENQING_content);
	JIATUAN_content.push(ANLI_content);
	JIATUAN_content.push(PIC_content);

	//console.log(JSON.stringify(JIATUAN_content));
	
	if(wrong_messages.length != 0){
		wrong_messages_br = "";
		for(var i = 0; i < wrong_messages.length; i++){
			wrong_messages_br += wrong_messages[i]+"\n";
		}
		alert(wrong_messages_br);
	}
	else{
		
		var year = $("#year").val();
		$.ajax({
			url: window.location.href,
			type: "POST",
			data: {"op": "submit", "year": year, "subtype": subtype, "content": JSON.stringify(JIATUAN_content)},
			success: function(data) {
				var data = JSON.parse(data);
				if (subtype == 0) {
					alert("暂存成功");
				} else if (subtype == 1) {
					alert("提交成功");
					window.location.href = '/index/';
				}
			}
		});
	}
}

function exportt(etype) {
	$.ajax({
		url: window.location.href,
		type: 'POST',
		data: {'op': 'export', 'title': $('#title').text(), 'etype': etype},
		success: function(data) {
			var data = JSON.parse(data);
			if (data['result'] == 'OK') {
				export_path = '/' + data['export_path'];
				$('a#download').attr('href', export_path);
				$('a#download').attr('download', export_path.slice(7));
				document.getElementById("download").click();
			} else {
				alert(data['result']);
			}
		}
	});
}
