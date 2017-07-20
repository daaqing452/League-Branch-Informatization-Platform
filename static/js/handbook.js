var td_html = "<td><textarea style=\"width: 100%; height: 31px; overflow: auto; resize: none;\"></textarea></td>";
var add_del_html = "<td align=\"center\"><span class=\"glyphicon glyphicon-plus\" onclick=\"addOption(this)\"></span><span class=\"glyphicon glyphicon-minus\" onclick=\"delOption(this)\"></span></td>"


var chapter;
var grade;

$(document).ready(function(){
	grade = 0;
	chapter = 0;
	$("#grade_0").parent().eq(0).attr("class","active");
	$("#chapter_0").parent().eq(0).attr("class","active");
	for(var i = 0; i < 4; i++){
		for(var j = 0; j < 7; j++){
			var div = $("#table_"+j).clone();
			div.attr("id","table_"+i+"_"+j);
			div.attr("type","item");
			if(j == 0){
				div.find("[type=\"jibenxinxi_title\"]").text($("#grade_"+i).text());
			}
			div.hide();
			$("#content").append(div);
		}
	}
	$("#content").append("<button class=\"btn btn-primary\" style=\"float: right; width: 100px;\" onclick=\"submit()\">提交</button>");
	$("#table_0_0").show();
	fill_content();
});

function fill_content(){
	var HANDBOOK_content = JSON.parse('[[[[["1","2","3","4",""]],[["",""],["",""],["",""],["",""]],[["","","","","","","","",""]],[["","","","","","","","",""]],[["","","","","","",""]],[["","","",""]]],[[[""]],[[""]],[[""]]],[[["","","","","","",""]],[["","","","","","",""]],[["","","","","","",""]]],[[["","","","","","",""]],[["","","","","","",""]],[["","","","","","",""]]],[[["","","","","","",""]],[["","","","","","",""]],[["","","","","","",""]]],[[["","","","","","",""]]],[[[""]]]],[[[["","","","",""]],[["",""],["",""],["",""],["",""]],[["","","","","","","","",""]],[["","","","","","","","",""]],[["","","","","","",""]],[["","","",""]]],[[[""]],[[""]],[[""]]],[[["","","","","","",""]],[["","","","","","",""]],[["","","","","","",""]]],[[["","","","","","",""]],[["","","","","","",""]],[["","","","","","",""]]],[[["","","","","","",""]],[["","","","","","",""]],[["","","","","","",""]]],[[["","","","","","",""]]],[[[""]]]],[[[["4","5","6","7",""]],[["",""],["",""],["",""],["",""]],[["","","","","","","","",""]],[["","","","","","","","",""]],[["","","","","","",""]],[["","","",""]]],[[[""]],[[""]],[[""]]],[[["","","","","","",""]],[["","","","","","",""]],[["","","","","","",""]]],[[["","","","","","",""]],[["","","","","","",""]],[["","","","","","",""]]],[[["","","","","","",""]],[["","","","","","",""]],[["","","","","","",""]]],[[["","","","","","",""]]],[[[""]]]],[[[["","","","",""]],[["",""],["",""],["",""],["",""]],[["","","","","","","","",""]],[["","","","","","","","",""]],[["","","","","","",""]],[["","","",""]]],[[[""]],[[""]],[[""]]],[[["","","","","","",""]],[["","","","","","",""]],[["","","","","","",""]]],[[["","","","","","",""]],[["","","","","","",""]],[["","","","","","",""]]],[[["","","","","","",""]],[["","","","","","",""]],[["","","","","","",""]]],[[["","","","","","",""]]],[[[""]]]]]');
	for(var i = 0; i < 4; i++){
		var GRADE_content = HANDBOOK_content[i];
		for(var j = 0; j < 7; j++){
			var CHAPTER_content = GRADE_content[j];
			var div = $("#table_"+i+"_"+j);
			var table_num = div.find("table").length;
			for(var k = 0; k < table_num; k++){
				var TABLE_content = CHAPTER_content[k]
				var table = div.find("table").eq(k);
				var tr_num = table.find("tr").length;
				var real_num = tr_num;
				var start_num = 0;
				if(table.find("tr").eq(0).find("textarea").length == 0){
					start_num = 1;
					real_num -= 1;
				}
				if(i == 1 && j == 0){
					console.log(TABLE_content);
					console.log(start_num + " " + real_num + " " + TABLE_content.length);
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
					}
				}
			}
		}
	}
}

function all_hind(){
	for(var i = 0; i < 7; i++){
		for(var j = 0; j < 4; j++){
			$("#table_"+i+"_"+j).hide();
		}
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
	$("#table_"+grade+"_"+chapter).show();
}

function time_select(id){
	var length = $("#nav_0").children("li").length;
	grade = id;
	for(var i = 0; i < length; i++){
		$("#grade_"+i).parent().eq(0).attr("class","");
	}
	$("#grade_"+id).parent().eq(0).attr("class","active");
	all_hind();
	$("#table_"+grade+"_"+chapter).show();
}

function submit(){
	var HANDBOOK_content = new Array();
	for(var i = 0; i < 4; i++){
		var GRADE_content = new Array();
		for(var j = 0; j < 7; j++){
			var CHAPTER_content = new Array();
			var div = $("#table_"+i+"_"+j);
			var table_num = div.find("table").length;
			for(var k = 0; k < table_num; k++){
				var TABLE_content = new Array();
				var table = div.find("table").eq(k);
				var tr_num = table.find("tr").length;
				for(var m = 0; m < tr_num; m ++){
					var TR_content = new Array();
					var tr = table.find("tr").eq(m);
					var textarea_num = tr.find("textarea").length;
					if(textarea_num == 0){
						continue;
					}
					else{
						for(var n = 0; n < textarea_num; n++){
							TR_content.push(tr.find("textarea").eq(n).val());
						}
					}
					TABLE_content.push(TR_content);
				}
				CHAPTER_content.push(TABLE_content);
			}
			GRADE_content.push(CHAPTER_content);
		}
		HANDBOOK_content.push(GRADE_content);
	}

	$.ajax({
		url: window.location.href,
		type: "POST",
		data: {"op": "submit", "content": JSON.stringify(HANDBOOK_content)},
		success: function(data) {
			var data = JSON.parse(data);
			alert("提交成功");
			window.location.href = '/index/';
		}
	})
	//console.log(JSON.stringify(HANDBOOK_content));
}

function addOption(b){
	var $b = $(b);
	var current_row = b.parentNode.parentNode;
	var row_type = current_row.getAttribute("class");
	var current_index = current_row.rowIndex;
	var op_table = b.parentNode.parentNode.parentNode;
	var new_row = op_table.insertRow(current_index+1);

	var HTMLContent = "<tr class=\""+row_type+"\">";
	var num = $(b).parents("tr").eq(0).children("td").length-1;
	for(var i = 0; i < num; i ++){
		HTMLContent += td_html;
		
	}
	HTMLContent += add_del_html;
	HTMLContent += "</tr>";
	new_row.innerHTML = HTMLContent;
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