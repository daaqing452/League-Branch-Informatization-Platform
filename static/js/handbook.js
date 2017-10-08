var td_html = "<td><textarea style=\"width: 100%; height: 31px; overflow: auto; resize: none;\"></textarea></td>";
var add_del_html = "<td align=\"center\"><span class=\"glyphicon glyphicon-plus\" onclick=\"addOption(this)\"></span><span class=\"glyphicon glyphicon-minus\" onclick=\"delOption(this)\"></span></td>"


var chapter;
var grade;

$(document).ready(function(){
	$("#chapter_0").parent().eq(0).attr("class","active");
	//$("#content").append("<button class=\"btn btn-primary\" style=\"float: right; width: 100px;\" onclick=\"submit()\">提交</button>");
	$("#table_0").show();
	for (var i = 0; i < years.length; i++) $("#year").append("<option>" + years[i] + "</option>");
	if (!readonly) year_onchange();
});

function load_handbook() {
	var hid = $("#main_div").attr("hid");
	$.ajax({
		url: window.location.href,
		type: "POST",
		data: {"op": "load_handbook", "hid": hid},
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
		data: {"op": "load_handbook", "year": year},
		success: function(data) {
			var data = JSON.parse(data);
			fill_content(data['content']);
			if (data['submitted']) {
				$("#button_save").attr({"disabled":"disabled"});
			} else {
				$("#button_save").removeAttr("disabled");
			}
		}
	})
}

function fill_content(content){
	//if (!content) content = '[[[["1","2","","",""]],[["",""],["",""],["",""],["",""]],[["","","","","","","","",""]],[["","","","","","","","",""]],[["","","","","","",""]],[["","","","",""]]],[[[""]],[[""]],[[""]]],[[["1","2","3","4","5","6"],["7"],["8","9","10","11","12","13"],["14"]],[["","","","","",""],[""]],[["","","","","",""],[""]]],[[["","","","","","",""]],[["","","","","","",""]],[["","","","","","",""]]],[[["","","","","","",""]],[["","","","","","",""]],[["","","","","","",""]]],[[["","","","","","",""]]],[[[""]]]]';
	var HANDBOOK_content = JSON.parse(content);
	for(var i = 0; i < 8; i++){
		var CHAPTER_content = HANDBOOK_content[i];
		var div = $("#table_"+i);
		var table_num = div.find("table").length;
		for(var k = 0; k < table_num; k++){
			var TABLE_content = CHAPTER_content[k]
			var table = div.find("table").eq(k);
			var tr_num = table.find("tr").length;
			var real_num = tr_num;
			var start_num = 0;
			if(i == 3 || i == 4 || i ==5 || i == 6){
				if(TABLE_content.length / 2 >1){
					var tr_pre = table.find("tr").eq(0).clone(); 
					var tr_cur = table.find("tr").eq(1).clone();
					var tr_next = table.find("tr").eq(2).clone();
					for(var clone_num = 0; clone_num < TABLE_content.length / 2 -1; clone_num++){
						tr_pre.appendTo(table); 
						tr_cur.appendTo(table); 
						tr_next.appendTo(table); 
					}
					
				}
				var content_cnt = 0;
				for(var m = 0; m < table.find("tr").length; m++){
					var tr = table.find("tr").eq(m);
					if(tr.find("textarea").length != 0){

						var TR_content = TABLE_content[content_cnt];
						var textarea_num = TR_content.length;
						content_cnt += 1;
						for(var n = 0; n < textarea_num; n++){
							tr.find("textarea").eq(n).val(TR_content[n]);
							tr.find("textarea").eq(n).css("background","");
						}
					}
				}
			}
			else{
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
		}
	}
}

function read_only(content){
	//var HANDBOOK_content = JSON.parse('[[[["wqe1aoidfjoaisdjfpaisdjfpaisdjfpasidfjapsdifjpasdifjapisdjfpaisdjfpaisdjfpasidjfpasidfj","qweqwe","123123","",""]],[["",""],["",""],["",""],["",""]],[["","","","","","","","",""]],[["","","","","","","","",""]],[["","","","","","",""]],[["","","",""]]],[[[""]],[[""]],[[""]]],[[["","","","","","",""]],[["","","","","","",""]],[["","","","","","",""]]],[[["","","","222","","",""]],[["","","","","","",""]],[["","","","","","",""]]],[[["","","","","","",""]],[["","","","","","",""]],[["","","","","","",""]]],[[["","","","","","",""]]],[[[""]]]]');
	//console.log(content);
	var HANDBOOK_content = JSON.parse(content);
	for(var i = 0; i < 8; i++){
		var CHAPTER_content = HANDBOOK_content[i];
		var div = $("#table_"+i);
		var table_num = div.find("table").length;
		for(var k = 0; k < table_num; k++){
			var TABLE_content = CHAPTER_content[k]
			var table = div.find("table").eq(k);
			var tr_num = table.find("tr").length;
			var real_num = tr_num;
			var start_num = 0;
			if(i == 3 || i == 4 || i ==5 || i == 6){
				if(TABLE_content.length / 2 >1){
					var tr_pre = table.find("tr").eq(0).clone(); 
					var tr_cur = table.find("tr").eq(1).clone();
					var tr_next = table.find("tr").eq(2).clone();
					for(var clone_num = 0; clone_num < TABLE_content.length / 2 -1; clone_num++){
						tr_pre.appendTo(table); 
						tr_cur.appendTo(table); 
						tr_next.appendTo(table); 
					}
					
				}
				var content_cnt = 0;
				for(var m = 0; m < table.find("tr").length; m++){
					var tr = table.find("tr").eq(m);
					if(tr.find("textarea").length != 0){

						var TR_content = TABLE_content[content_cnt];
						var textarea_num = TR_content.length;;
						content_cnt += 1;
						for(var n = 0; n < textarea_num; n++){
							tr.find("textarea").eq(n).val(TR_content[n]);
							tr.find("textarea").eq(n).attr("disabled", "disabled");
							tr.find("textarea").eq(n).attr("readonly", "readonly");
						}
					}
				}
			}
			else{
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
			
		}
	}
}

function all_hind(){
	for(var i = 0; i < 8; i++){
		$("#table_"+i).hide();
	}
}

function module_select(id){
	var length = $("#nav_1").children("li").length;
	chapter = id;
	for(var i = 0; i < length; i++){
		$("#chapter_"+i).parent().eq(0).attr("class","");
	}
	$("#chapter_"+id).parent().eq(0).attr("class","active");
	all_hind();
	$("#table_"+chapter).show();
}



function check_fill(tr,already_fill,tr_class,textarea_n,content){
	var num_pat = new RegExp("^[1-9][0-9]*$");
	var shishu_pat = new RegExp("^\\d+(\\.\\d+)?$");
	var xuehao_pat = new RegExp("^\\d{10}$");
	var data_pat = new RegExp("^([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8])))$");
	if(tr.find("td").eq(textarea_n).attr("class")=="canyurenshu"){
		if(content!="" && num_pat.test(content) == false){
			return "参与人数填写有误(非正整数)";
		}
	}
	if(tr.find("td").eq(textarea_n).attr("class")=="huodongshijian"){
		if(content!="" && data_pat.test(content) == false){
			return "活动时间填写有误(日期格式)";
		}
	}
	if(tr_class == "jibenxinxi"){
		if(textarea_n >= 0 && textarea_n <= 3){
			if(content == ""){
				return "基本信息填写有误(必填项)";
			}
		}
		if(textarea_n == 0 && content != ""){
			if(num_pat.test(content) == false){
				return "团员人数填写有误(非正整数)";
			}
		}
	}
	if(tr_class == "jiangchengqingkuang"){
		if(textarea_n == 0){
			var clist = content.split("\n");
			if(clist.length == 1 && clist[0] == ""){
				//no input
			}
			else{
				for(var i = 0; i < clist.length; i++){
					var each_c = clist[i];
					if(data_pat.test(each_c) == false){
						return "奖惩情况填写有误(日期格式)";
					}
				}
			}	
		}
	}
	if(tr_class == "huamingce" || tr_class == "shenqingrutuan"){
		if(textarea_n >= 0 && textarea_n <= 7 && tr_class == "huamingce"){
			if(content == ""){
				return "团员信息填写有误(必填项)";
			}
		}
		if(textarea_n >= 0 && textarea_n <= 7 && already_fill){
			if(content == ""){
				return "团员信息填写有误(必填项)";
			}
		}
		if(textarea_n == 0 && content != ""){
			if(xuehao_pat.test(content) == false){
				return "团员信息学号填写有误";
			}
		}
		if(textarea_n == 5 || textarea_n == 6){
			if(content != "" && data_pat.test(content) == false){
				return  "团员信息填写有误(日期格式)";
			}
		}
		if(textarea_n == 2){
			if(content != "" && content != "男" && content != "女"){
				return "团员信息填写有误(性别)";
			}
		}
	}
	if(tr_class == "jiaonatuanfei"){
		if(textarea_n >= 0 && textarea_n <= 5){
			if(content == ""){
				return "交纳团费填写有误(必填项)";
			}
		}
		if(textarea_n == 0 && content != ""){
			if(num_pat.test(content)){
				var num = parseFloat(content);
				if(num <= 0 || num > 12){
					return "交纳团费填写有误(月份)";
				}
			}
			else{
				return "交纳团费填写有误(月份)";
			}
		}
		if(textarea_n >= 1 && textarea_n <= 3 && content != ""){
			if(num_pat.test(content) == false){
				return "交纳团费填写有误(数字)";
			}
			if(textarea_n == 2 && (tr.find("textarea").eq(1).val() < tr.find("textarea").eq(2).val())){
				return "交纳团费填写有误(大于支部人数)";
			}
			if(textarea_n == 3 && (tr.find("textarea").eq(1).val() < tr.find("textarea").eq(3).val())){
				return "交纳团费填写有误(大于支部人数)";
			}
		}
		if(textarea_n >= 4 && textarea_n <= 5 && content != ""){
			if(shishu_pat.test(content) == false){
				return "交纳团费填写有误(数字)";
			}
		}


	}
	if(tr_class == "tuiyourudang"){
		if(textarea_n >= 0 && textarea_n <= 2 && already_fill){
			if(content == ""){
				return "推优入党填写有误(必填项)";
			}
		}
		if(textarea_n == 0 && content != ""){
			if(xuehao_pat.test(content) == false){
				return "推优入党学号填写有误";
			}
		}
		if(textarea_n >= 2 && textarea_n <= 4 && content != ""){
			if(data_pat.test(content) == false){
				return  "推优入党信息填写有误(日期格式)";
			}
			if(textarea_n == 3 && date_seq(tr.find("textarea").eq(2).val(),tr.find("textarea").eq(3).val()) == false){
				return "推优入党信息填写有误(时间顺序)";
			}
			if(textarea_n == 4 && date_seq(tr.find("textarea").eq(3).val(),tr.find("textarea").eq(4).val()) == false){
				return "推优入党信息填写有误(时间顺序)";
			}
		}

	}
	if(tr_class == "quannianjihua" || tr_class == "chunjijihua" || tr_class=="qiujijihua"){
		if(content == ""){
			return "计划填写有误(必填项)";
		}
	}
	if(tr_class == "zhibushiyejihua" || tr_class == "zhibushiyemubiao" || tr_class=="zhibushiyeyuqichengguo"){
		if(content == ""){
			return "计划填写有误(必填项)";
		}
	}
	return true;
}

function date_seq(date1, date2){
	if(date1 < date2){
		return true;
	}
	else{
		return false;
	}
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
	var HANDBOOK_content = new Array();
	wrong_messages = new Array();
	for(var i = 0; i < 8; i++){
		var CHAPTER_content = new Array();
		var div = $("#table_"+i);
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
						if(tr.find("textarea").eq(n).val() != ""){
							already_fill = true;
							break;
						}
					}
					for(var n = 0; n < textarea_num; n++){
						tr.find("textarea").eq(n).css("background","");
						var false_message = check_fill(tr,already_fill,tr.attr("class"),n,tr.find("textarea").eq(n).val());
						if (subtype == 0) false_message = true;
						if(false_message != true){
							if(is_in_array(wrong_messages,false_message) == false){
								wrong_messages.push(false_message);
							}
							tr.find("textarea").eq(n).css("background","#CCCCCC");
						}
						TR_content.push(tr.find("textarea").eq(n).val());
					}
				}
				TABLE_content.push(TR_content);
			}
			CHAPTER_content.push(TABLE_content);
		}
		HANDBOOK_content.push(CHAPTER_content);
	}
	
	
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
			data: {"op": "submit", "year": year, "subtype": subtype, "content": JSON.stringify(HANDBOOK_content)},
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

	//console.log(JSON.stringify(HANDBOOK_content));
}

function addOption(b){
	var $b = $(b);
	var current_row = b.parentNode.parentNode;
	var row_type = current_row.getAttribute("class");
	var current_index = current_row.rowIndex;
	var op_table = b.parentNode.parentNode.parentNode;
	var new_row = op_table.insertRow(current_index+1);
	
	var tr_html = $(b).parents("tr").eq(0).html();
	new_row.innerHTML = tr_html;
	$(new_row).attr("class",row_type);
}

function addOption_2(b){
	var $b = $(b);
	var $this_table = $b.parents("table").eq(0);	
	var current_index = b.parentNode.parentNode.rowIndex;
	var pre_html = $this_table.find("tr").eq(current_index-1).html();
	var current_html = $this_table.find("tr").eq(current_index).html();
	var next_html = $this_table.find("tr").eq(current_index+1).html();
	$this_table.append("<tr>"+pre_html+"</tr>");
	$this_table.append("<tr>"+current_html+"</tr>");
	$this_table.append("<tr>"+next_html+"</tr>");
}


function delOption(b){
	var current_row = b.parentNode.parentNode;
	var current_index = current_row.rowIndex;
	var op_table = b.parentNode.parentNode.parentNode;
	if(current_index == 1 && op_table.rows.length == 2)
	{
		alert("至少一条记录！");
		return;
	}
	op_table.deleteRow(current_index);
}

function delOption_2(b){
	var current_row = b.parentNode.parentNode;
	var current_index = current_row.rowIndex;
	var op_table = b.parentNode.parentNode.parentNode;
	if(current_index == 1 && op_table.rows.length == 3)
	{
		alert("至少一条记录！");
		return;
	}
	op_table.deleteRow(current_index+1);
	op_table.deleteRow(current_index);
	op_table.deleteRow(current_index-1);
}