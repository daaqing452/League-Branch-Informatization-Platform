var td_html = "<td><textarea style=\"width: 100%; height: 31px; overflow: auto; resize: none;\"></textarea></td>";
var add_del_html = "<td align=\"center\"><span class=\"glyphicon glyphicon-plus\" onclick=\"addOption(this)\"></span><span class=\"glyphicon glyphicon-minus\" onclick=\"delOption(this)\"></span></td>"
var weiyuan_html = '<tr>'+
					'<td><textarea style="width: 100%; overflow: auto; resize: none;"  placeholder=\"委员职能\"></textarea></td>'+
					'<td><textarea style="width: 100%; overflow: auto; resize: none;" placeholder=\"委员姓名\"></textarea></td>'+
					'<td><textarea style="width: 100%; overflow: auto; resize: none;" placeholder=\"备注\"></textarea></td>'+
					'<td></td><td></td>'+
					'<td align=\"center\"><span class=\"glyphicon glyphicon-minus\" onclick=\"delOption(this)\"></td></tr>';

var weiyuan_html_without_edit = '<tr>'+
					'<td><textarea style="width: 100%; overflow: auto; resize: none;"  placeholder=\"委员职能\"></textarea></td>'+
					'<td><textarea style="width: 100%; overflow: auto; resize: none;" placeholder=\"委员姓名\"></textarea></td>'+
					'<td><textarea style="width: 100%; overflow: auto; resize: none;" placeholder=\"备注\"></textarea></td>'+
					'<td></td><td></td></tr>';


var huodongneirong_html = '<td align=\"center\" style=\"vertical-align: middle;\">活动内容</td> <td colspan=\"5\"><textarea  style=\"width: 100%; height: 100px; overflow: auto; resize: none;\"></textarea></td>';
var huodongneirong_html_without_edit = '<td align=\"center\" style=\"vertical-align: middle;\">活动内容</td> <td colspan=\"5\"><div  style=\"width: 100%; height: 100px; overflow: auto; resize: none; border:0.5px solid #ADADAD;\"></div></td>';
var youleixingdehuodongneirong_html = '<td align=\"center\" style=\"vertical-align: middle;\">活动内容</td> <td colspan=\"6\"><textarea  style=\"width: 100%; height: 100px; overflow: auto; resize: none;\"></textarea></td>';
var youleixingdehuodongneirong_html_without_edit = '<td align=\"center\" style=\"vertical-align: middle;\">活动内容</td> <td colspan=\"6\"><div  style=\"width: 100%; height: 100px; overflow: auto; resize: none; border:0.5px solid #ADADAD;\"></div></td>';
var huodongzongjie_html = '<td align=\"center\" style=\"vertical-align: middle;\">活动总结</td> <td colspan=\"5\"><textarea  style=\"width: 100%; height: 100px; overflow: auto; resize: none;\"></textarea></td>';
var huodongzongjie_html_without_edit = '<td align=\"center\" style=\"vertical-align: middle;\">活动总结</td> <td colspan=\"5\"><div  style=\"width: 100%; height: 100px; overflow: auto; resize: none; border:0.5px solid #ADADAD;\"></div></td>';
var youleixingdehuodongzongjie_html = '<td align=\"center\" style=\"vertical-align: middle;\">活动总结</td> <td colspan=\"6\"><textarea  style=\"width: 100%; height: 100px; overflow: auto; resize: none;\"></textarea></td>';
var youleixingdehuodongzongjie_html_without_edit = '<td align=\"center\" style=\"vertical-align: middle;\">活动总结</td> <td colspan=\"6\"><div  style=\"width: 100%; height: 100px; overflow: auto; resize: none; border:0.5px solid #ADADAD;\"></div></td>';
var huodongneirong_html_without_edit2 = '<td style=\"width:100%;\"><div  style=\"width: 100%; height: 100px; overflow: auto; resize: none; border:1px solid #ADADAD;\"></div></td>';

var chapter;
var grade;
var htype = "b";

$(document).ready(function(){
	for (var i = 0; i < years.length; i++) $("#year").append("<option>" + years[i] + "</option>");
	if (!readonly) year_onchange();
	
});

var options = {  
resizeType : 1,
filterMode : true,  
allowImageUpload : false,  
allowFlashUpload : false,  
allowMediaUpload : false,  
allowFileManager : false,  
afterBlur: function(){this.sync();},
items : ['fontname', 'fontsize', '|', 'forecolor', 'hilitecolor', 'bold', 'italic', 'underline',  
'removeformat', '|', 'justifyleft', 'justifycenter', 'justifyright', 'insertorderedlist',  
'insertunorderedlist'],  
};  



var bianji_list = new Array("quannianjihua_bianji","chunjixueqijihua_bianji","qiujixueqijihua_bianji","zhibushiyejianjie_bianji","zhibushiyemubiao_bianji",
					"zhibushiyeyuqichengguo_bianji","qiujixueqigongzuozongjie_bianji","chunjixueqigongzuozongjie_bianji",
					"huodongneirong_bianji_0","huodongneirong_bianji_1","huodongneirong_bianji_2","huodongneirong_bianji_3",
					"huodongneirong_bianji_4","huodongneirong_bianji_5","huodongneirong_bianji_6","huodongneirong_bianji_7",
					"huodongneirong_bianji_8","huodongneirong_bianji_9","dengjipinggufangan_bianji",
					"shishixize_bianji","dengjipinggulingdao_bianji","chujijiajituanzhibu_bianji");
var editor = new Array();  
KindEditor.ready(function(K) {  
	for(var i = 0; i < bianji_list.length; i++){
		editor[i] = K.create('textarea[name="'+bianji_list[i]+'"]',options);
	
	}
});  

function load_handbook() {
	var hid = $("#main_div").attr("hid");
	$.ajax({
		url: window.location.href,
		type: "POST",
		data: {"op": "load_handbook", "hid": hid},
		success: function(data) {
			var data = JSON.parse(data);
			htype = data["htype"];
			read_only(data["content"]);
			if(htype == "b"){
				$("#nav_1").show();
				$("#chapter_0").parent().eq(0).attr("class","active");
				$("#table_0").show();
			}
			else{
				$("#nav_2").show();
				$("#chapter_6").parent().eq(0).attr("class","active");
				$("#table_6").show();
			}
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
			//console.log(data["htype"]);
			htype = data["htype"];
			fill_content(data['content']);
			if (data['submitted']) {
				$("#button_save").attr({"disabled":"disabled"});
			} else {
				$("#button_save").removeAttr("disabled");
			}
			
			if(htype == "b"){
				$("#nav_1").show();
				$("#chapter_0").parent().eq(0).attr("class","active");
				$("#table_0").show();
			}
			else{
				$("#nav_2").show();
				$("#chapter_8").parent().eq(0).attr("class","active");
				$("#table_8").show();
			}
		}
	})
}

function fill_content(content){
	//console.log(content)
	//if (!content) content = '[[[["1","2","","",""]],[["",""],["",""],["",""],["",""]],[["","","","","","","","",""]],[["","","","","","","","",""]],[["","","","","","",""]],[["","","","",""]]],[[[""]],[[""]],[[""]]],[[["1","2","3","4","5","6"],["7"],["8","9","10","11","12","13"],["14"]],[["","","","","",""],[""]],[["","","","","",""],[""]]],[[["","","","","","",""]],[["","","","","","",""]],[["","","","","","",""]]],[[["","","","","","",""]],[["","","","","","",""]],[["","","","","","",""]]],[[["","","","","","",""]]],[[[""]]]]';
	//content = '[[[["1","2","3","4","5"],["11","22","33"],["44","55","66"]],[["",""],["",""],["",""],["",""]],[["1","2","","","","","","",""],["3","4","","","","","","",""],["5","6","","","","","","",""]],[["","","","","","","","",""]],[["","","","","","",""]],[["","","","",""]]],[[["","12<span style=\'color:#E53333;\'>31</span>2"]],[["",""]],[["",""]]],[[["","<ol>\\n\\t<li>\\n\\t\\t我爱<span style=\'background-color:#E56600;\'>中</span>国\\n\\t</li>\\n\\t<li>\\n\\t\\t2222\\n\\t</li>\\n</ol>"]],[["",""]],[["",""]]],[[["","","","","",""],[""]],[["","","","","",""],[""]],[["","","","","",""],[""]]],[[["","","","","",""],[""]],[["","","","","",""],[""]],[["","","","","",""],[""]]],[[["11","","","","",""],[""],["22","","","","",""],[""],["33","","","","",""],[""]],[["","","","","",""],[""]],[["","","","","",""],[""]]],[[["1","","","","",""],[""],["2","","","","",""],[""]]],[[["","我爱<em>我家啊啊啊</em>"]]]]';
	if(content == null){
		return;
	}
	//console.log(content);
	var HANDBOOK_content = JSON.parse(content);
	for(var i = 0; i < 10; i++){
		var CHAPTER_content = HANDBOOK_content[i];
		var div = $("#table_"+i);
		var table_num = div.find("table").length;
		for(var k = 0; k < table_num; k++){
			var TABLE_content = CHAPTER_content[k]
			var table = div.find("table").eq(k);
			var tr_num = table.find("tr").length;
			var real_num = tr_num;
			var start_num = 0;
			
			if(i >= 3 && i <= 4){
				//console.log(JSON.stringify(TABLE_content));
				if(TABLE_content.length / 3 >1){
					for(var clone_num = 0; clone_num < TABLE_content.length / 3 - 1; clone_num++){
						var tr_pre = table.find("tr").eq(0).clone(); 
						var tr_cur = table.find("tr").eq(1).clone();
						//var tr_next = table.find("tr").eq(2).clone();
						tr_pre.appendTo(table); 
						tr_cur.appendTo(table); 

						//tr_next.appendTo(table); 
						if(i == 3){
							if(k == 0){
								table.append("<tr>"+huodongneirong_html+"</tr>");
								table.append("<tr>"+huodongzongjie_html+"</tr>");
							}
							else{
								table.append("<tr>"+youleixingdehuodongneirong_html+"</tr>");
								table.append("<tr>"+youleixingdehuodongzongjie_html+"</tr>");
							}
						}
						else{
							table.append("<tr>"+youleixingdehuodongneirong_html+"</tr>");
							table.append("<tr>"+youleixingdehuodongzongjie_html+"</tr>");
						}
						var tr = table.find("tr").last().prev();
						tr.find('td').last().children("textarea").attr("name","huodongneirong_bianji_"+bianji_list.length);
						var bianji_length = bianji_list.length
						bianji_list.push("huodongneirong_bianji_"+bianji_list.length);

						KindEditor.ready(function(K) { 
							editor[bianji_length] = K.create('textarea[name="huodongneirong_bianji_'+bianji_length+'"]',options);
						});

						var tr = table.find("tr").last();
						tr.find('td').last().children("textarea").attr("name","huodongneirong_bianji_"+bianji_list.length);
						var bianji_length = bianji_list.length
						bianji_list.push("huodongneirong_bianji_"+bianji_list.length);

						KindEditor.ready(function(K) { 
							editor[bianji_length] = K.create('textarea[name="huodongneirong_bianji_'+bianji_length+'"]',options);
						});  
					}
					
				}

				var content_cnt = 0;
				//console.log(table.find("tr").length);
				//console.log(JSON.stringify(TABLE_content));
				
				for(var m = 0; m < table.find("tr").length; m++){
					var tr = table.find("tr").eq(m);
					if(tr.find("textarea").length != 0){
						var textarea_num = tr.find("textarea").length;
						if(textarea_num == 0){
							continue;
						}
						var keditor_flag = false;
						var textarea_name = tr.find("textarea").last().attr("name");
						for(var it = 0; it < bianji_list.length; it++){
							if(bianji_list[it].indexOf(textarea_name) >= 0){
								keditor_flag = true;
							}
						} 
						
						
						if(keditor_flag){
							var textarea_name = tr.find("textarea").last().attr("name");
							var editor_index = bianji_list.indexOf(textarea_name);
							editor[editor_index].edit.doc.body.style.backgroundColor = '';
							var TR_content = TABLE_content[content_cnt];
							editor[editor_index].html(TR_content[0]);
							//console.log(tr.attr("class")+" "+textarea_content);
						}
						else{
							var TR_content = TABLE_content[content_cnt];
							var textarea_num = TR_content.length;
							for(var n = 0; n < textarea_num; n++){
								tr.find("textarea").eq(n).val(TR_content[n]);
								
							}
						}
						content_cnt += 1;
						
					}
				}
			}
			else{
				if(table.find("tr").eq(0).find("textarea").length == 0){
					start_num = 1;
					real_num -= 1;
				}

				for(var clone_num = real_num; clone_num < TABLE_content.length; clone_num++){
					if(i == 0 && k == 0){
						var tr = weiyuan_html;
						table.append(tr);
					}
					else{
						var tr = table.find("tr").eq(start_num).clone();
						tr.appendTo(table);
					}
					
					
				}
				
				for(var m = 0; m < TABLE_content.length; m++){
					var TR_content = TABLE_content[m];
					var textarea_num = TR_content.length;
					var tr = table.find("tr").eq(start_num+m);
					var keditor_flag = false;
					var tr_class = tr.attr("class");
					if(tr_class != undefined &&tr_class.indexOf("jiangchengqingkuang") >= 0){
						if(TR_content[0] == "团支部"){
							tr.attr("class","jiangchengqingkuang_1");
						} 
						if(TR_content[0] == "班级"){
							tr.attr("class","jiangchengqingkuang_2");
						}
						if(TR_content[0] == "党课学习小组"){
							tr.attr("class","jiangchengqingkuang_3");
						}
						if(TR_content[0] == "个人"){
							tr.attr("class","jiangchengqingkuang_4");
						}
					}
					for(var it = 0; it < bianji_list.length; it++){
						if(bianji_list[it].indexOf(tr_class) >= 0){
							keditor_flag = true;
						}
					} 
					if(keditor_flag){
						var textarea_name = tr.find("textarea").eq(1).prop("name");
						KindEditor.html('textarea[name="'+textarea_name+'"]',TR_content[0]);
						var editor_index = bianji_list.indexOf(textarea_name);
						editor[editor_index].edit.doc.body.style.backgroundColor = '';
					}
					else{
						for(var n = 0; n < textarea_num; n++){
							tr.find("textarea").eq(n).val(TR_content[n]);
							tr.find("textarea").eq(n).css("background","");
						}
					}
					
				}
			}
		}	
	}
	//dosomething
	var placeholder_list = ["dengjipinggufangan_bianji","shishixize_bianji","dengjipinggulingdao_bianji","chujijiajituanzhibu_bianji"];
	var placeholder_words = ["填写院系本学年等级评估方案","填写院系本学年等级评估实施细则","填写院系本学年等级评估领导小组组成","填写院系本学年初评甲级团支部名单"]
	for(var i = 0; i < 4; i++){
		var editor_index = bianji_list.indexOf(placeholder_list[i]);
		if(editor[editor_index].html() == ""){
			editor[editor_index].html(placeholder_words[i]);
		}
	}

}

function read_only(content){
	//var HANDBOOK_content = JSON.parse('[[[["wqe1aoidfjoaisdjfpaisdjfpaisdjfpasidfjapsdifjpasdifjapisdjfpaisdjfpaisdjfpasidjfpasidfj","qweqwe","123123","",""]],[["",""],["",""],["",""],["",""]],[["","","","","","","","",""]],[["","","","","","","","",""]],[["","","","","","",""]],[["","","",""]]],[[[""]],[[""]],[[""]]],[[["","","","","","",""]],[["","","","","","",""]],[["","","","","","",""]]],[[["","","","222","","",""]],[["","","","","","",""]],[["","","","","","",""]]],[[["","","","","","",""]],[["","","","","","",""]],[["","","","","","",""]]],[[["","","","","","",""]]],[[[""]]]]');
	var HANDBOOK_content = JSON.parse(content);
	if(content == null){
		return;
	}
	
	for(var i = 0; i < 10; i++){
		var CHAPTER_content = HANDBOOK_content[i];
		var div = $("#table_"+i);
		var table_num = div.find("table").length;
		for(var k = 0; k < table_num; k++){
			var TABLE_content = CHAPTER_content[k]
			var table = div.find("table").eq(k);
			var tr_num = table.find("tr").length;
			var real_num = tr_num;
			var start_num = 0;
			if(i >= 3 && i <= 4){
				//console.log(table_num);
				
				table.find("tr").eq(0).children("td").last().remove();
				table.find("tr").eq(1).children("td").last().remove();
				if(TABLE_content.length / 3 >1){
					for(var clone_num = 0; clone_num < TABLE_content.length / 3 - 1; clone_num++){
						var tr_pre = table.find("tr").eq(0).clone(); 
						var tr_cur = table.find("tr").eq(1).clone();
						//console.log(tr_cur.children("td").last().attr("align"));
						//console.log(tr_cur.html());
						
						//var tr_next = table.find("tr").eq(2).clone();
						tr_pre.appendTo(table); 
						tr_cur.appendTo(table); 
						//tr_next.appendTo(table); 
						if(i == 3){
							if(k == 0){
								table.append("<tr>"+huodongneirong_html+"</tr>");
								table.append("<tr>"+huodongzongjie_html+"</tr>");
							}
							else{
								table.append("<tr>"+youleixingdehuodongneirong_html+"</tr>");
								table.append("<tr>"+youleixingdehuodongzongjie_html+"</tr>");
							}
						}
						else{
							table.append("<tr>"+youleixingdehuodongneirong_html+"</tr>");
							table.append("<tr>"+youleixingdehuodongzongjie_html+"</tr>");
						}
						var tr = table.find("tr").last().prev();
						tr.find('td').last().children("textarea").attr("name","huodongneirong_bianji_"+bianji_list.length);
						var bianji_length = bianji_list.length
						bianji_list.push("huodongneirong_bianji_"+bianji_list.length);

						KindEditor.ready(function(K) { 
							editor[bianji_length] = K.create('textarea[name="huodongneirong_bianji_'+bianji_length+'"]',options);
						});

						var tr = table.find("tr").last();
						tr.find('td').last().children("textarea").attr("name","huodongneirong_bianji_"+bianji_list.length);
						var bianji_length = bianji_list.length
						bianji_list.push("huodongneirong_bianji_"+bianji_list.length);

						KindEditor.ready(function(K) { 
							editor[bianji_length] = K.create('textarea[name="huodongneirong_bianji_'+bianji_length+'"]',options);
						}); 
					}
					
				}

				var content_cnt = 0;
				for(var m = 0; m < table.find("tr").length; m++){
					var tr = table.find("tr").eq(m);
					if(tr.find("textarea").length != 0){
						var textarea_num = tr.find("textarea").length;
						if(textarea_num == 0){
							continue;
						}
						var keditor_flag = false;
						var textarea_name = tr.find("textarea").last().attr("name");
						for(var it = 0; it < bianji_list.length; it++){
							if(bianji_list[it].indexOf(textarea_name) >= 0){
								keditor_flag = true;
							}
						} 
						
						
						if(keditor_flag){
							var textarea_name = tr.find("textarea").last().attr("name");
							var editor_index = bianji_list.indexOf(textarea_name);
							editor[editor_index].edit.doc.body.style.backgroundColor = '';
							var TR_content = TABLE_content[content_cnt];
							editor[editor_index].html(TR_content[0]);
							editor[editor_index].readonly(true);
							
							//tr.find("textarea").last().parents("tr").eq(0).append(huodongneirong_html_without_edit);
							tr.empty();
							if(content_cnt % 2 == 1){
								if(i == 3){
									if(k == 0){
										tr.append(huodongneirong_html_without_edit);
									}
									else{
										tr.append(youleixingdehuodongneirong_html_without_edit);
									}
								}
								else{
									tr.append(youleixingdehuodongneirong_html_without_edit);
									
								}
							}
							else{
								if(i == 3){
									if(k == 0){
										tr.append(huodongzongjie_html_without_edit);
									}
									else{
										tr.append(youleixingdehuodongzongjie_html_without_edit);
									}
								}
								else{
									tr.append(youleixingdehuodongzongjie_html_without_edit);
									
								}
							}
							
							tr.find("div").eq(0).append(TR_content[0]);
							//console.log(tr.attr("class")+" "+textarea_content);
						}
						else{
							var TR_content = TABLE_content[content_cnt];
							var textarea_num = TR_content.length;
							for(var n = 0; n < textarea_num; n++){
								tr.find("textarea").eq(n).val(TR_content[n]);
								tr.find("textarea").eq(n).attr("disabled", "disabled");
								tr.find("textarea").eq(n).attr("readonly", "readonly");
								
							}
						}
						content_cnt += 1;
						
					}
				}
			}
			else{
				if(table.find("tr").eq(0).find("textarea").length == 0){
					start_num = 1;
					real_num -= 1;
				}

				if(htype=="b" && i == 0){
					table.find("tr").eq(0).children("td").last().remove();
					table.find("tr").eq(start_num).children("td").last().remove();
					if(table.attr("name") == "jiangchengqingkuang"){
						table.find("tr").eq(2).children("td").last().remove();
						table.find("tr").eq(3).children("td").last().remove();
						table.find("tr").eq(4).children("td").last().remove();
					}
				}
				for(var clone_num = real_num; clone_num < TABLE_content.length; clone_num++){
					if(i == 0 && k == 0){
						var tr = weiyuan_html_without_edit;
						table.append(tr);
					}
					else{
						var tr = table.find("tr").eq(start_num).clone();
						tr.appendTo(table);
					}	
				}

				for(var m = 0; m < TABLE_content.length; m++){
					var TR_content = TABLE_content[m];
					var textarea_num = TR_content.length;
					var tr = table.find("tr").eq(start_num+m);
					var keditor_flag = false;
					var tr_class = tr.attr("class");
					for(var it = 0; it < bianji_list.length; it++){
						if(bianji_list[it].indexOf(tr_class) >= 0){
							keditor_flag = true;
						}
					} 
					if(keditor_flag){
						var textarea_name = tr.find("textarea").eq(1).prop("name");
						KindEditor.html('textarea[name="'+textarea_name+'"]',TR_content[0]);
						var editor_index = bianji_list.indexOf(textarea_name);
						editor[editor_index].readonly(true);
						editor[editor_index].remove();
						tr.empty();
						tr.append(huodongneirong_html_without_edit2);
						tr.find("div").eq(0).append(TR_content[0]);
						tr.find("div").eq(0).height(200);
					}
					else{
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
}

function all_hind(){
	var length = $("#nav_1").children("li").length + $("#nav_2").children("li").length;
	for(var i = 0; i < length; i++){
		$("#table_"+i).hide();
	}
}

function module_select(id){
	var length = $("#nav_1").children("li").length + $("#nav_2").children("li").length;
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
	var data_pat_jiangchengqingkuang = new RegExp("^([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-((0[13578]|1[02])|(0[469]|11)|(02))$"); 
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

	if(tr_class != undefined && tr_class.indexOf("jiangchengqingkuang")>=0){
		if(textarea_n == 1){
			var clist = content.split("\n");
			if(clist[0] == ""){
				//no input
			}
			else{
				for(var i = 0; i < clist.length; i++){
					var each_c = clist[i];
					if(data_pat_jiangchengqingkuang.test(each_c) == false){
						return "奖惩情况填写有误(日期格式)";
					}
				}
			}	
		}
	}
	if(tr_class == "huamingce"){
		if(textarea_n >= 0 && textarea_n <= 6 && tr_class == "huamingce"){
			if(content == ""){
				return "团员信息填写有误(必填项)";
			}
		}
		if(textarea_n >= 0 && textarea_n <= 6 && already_fill){
			if(content == ""){
				return "团员信息填写有误(必填项)";
			}
		}
		if(textarea_n == 0 && content != ""){
			if(xuehao_pat.test(content) == false){
				return "团员信息学号填写有误";
			}
		}
		if(textarea_n == 6 || textarea_n == 7){
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
	if(tr_class == "shenqingrutuan"){
		if(textarea_n >= 0 && textarea_n <= 6 && tr_class == "huamingce"){
			if(content == ""){
				return "团员信息填写有误(必填项)";
			}
		}
		if(textarea_n >= 0 && textarea_n <= 6 && already_fill){
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
	if(tr_class == "quannianjihua" || tr_class == "chunjixueqijihua" || tr_class=="qiujixueqijihua"){
		if(content == ""){
			//console.log(content);
			return "计划填写有误(必填项)";
		}
	}
	if(tr_class == "zhibushiyejianjie" || tr_class == "zhibushiyemubiao" || tr_class=="zhibushiyeyuqichengguo"){
		if(content == ""){
			//console.log(content);
			return "支部事业填写有误(必填项)";
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
	for(var i = 0; i < 10; i++){
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
				var keditor_flag = false;
				if(i >= 3 && i <= 4){
					var textarea_name = tr.find("textarea").last().attr("name");
					for(var it = 0; it < bianji_list.length; it++){
						if(bianji_list[it].indexOf(textarea_name) >= 0){
							keditor_flag = true;
						}
					} 
				}
				else{
					var tr_class = tr.attr("class");
					for(var it = 0; it < bianji_list.length; it++){
						if(bianji_list[it].indexOf(tr_class) >= 0){
							keditor_flag = true;
						}
					} 
				}

				if(keditor_flag){
					var textarea_name = tr.find("textarea").eq(1).prop("name");
					var editor_index = bianji_list.indexOf(textarea_name);
					editor[editor_index].edit.doc.body.style.backgroundColor = '';
					var textarea_content = editor[editor_index].html();
					//console.log(tr.attr("class")+" "+textarea_content);
					var false_message = check_fill(tr,already_fill,tr.attr("class"),n,textarea_content);
					if (subtype == 0) false_message = true;
					if(false_message != true){
						if(is_in_array(wrong_messages,false_message) == false){
							wrong_messages.push(false_message);
						}
						var textarea_name = tr.find("textarea").eq(1).prop("name");
						var editor_index = bianji_list.indexOf(textarea_name);
						editor[editor_index].edit.doc.body.style.backgroundColor = '#CCCCCC';	
					}
					TR_content.push(textarea_content);
					
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
						var textarea_content = tr.find("textarea").eq(n).val();
						var false_message = check_fill(tr,already_fill,tr.attr("class"),n,textarea_content);
						if (subtype == 0) false_message = true;
						if(false_message != true){
							if(is_in_array(wrong_messages,false_message) == false){
								wrong_messages.push(false_message);
							}
							tr.find("textarea").eq(n).css("background","#CCCCCC");
							
							
						}
						TR_content.push(textarea_content);
					}
				}
				TABLE_content.push(TR_content);
			}
			CHAPTER_content.push(TABLE_content);
		}
		HANDBOOK_content.push(CHAPTER_content);
	}
	
	console.log(JSON.stringify(HANDBOOK_content));
	
	if(htype == "b" && wrong_messages.length != 0){
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
	
	
}

function addOption(b){
	if(readonly){
		return;
	}
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
	if(readonly){
		return;
	}
	var $b = $(b);
	var $this_table = $b.parents("table").eq(0);	
	var current_index = b.parentNode.parentNode.rowIndex;
	var pre_html = $this_table.find("tr").eq(current_index-1).html();
	var current_html = $this_table.find("tr").eq(current_index).html();
	
	
	$this_table.append("<tr>"+pre_html+"</tr>");
	$this_table.append("<tr>"+current_html+"</tr>");
	$this_table.append("<tr>"+huodongneirong_html+"</tr>");
	$this_table.append("<tr>"+huodongzongjie_html+"</tr>");
	
	var tr = $this_table.find("tr").last().prev();
	tr.find('td').last().children("textarea").attr("name","huodongneirong_bianji_"+bianji_list.length);
	var bianji_length = bianji_list.length
	bianji_list.push("huodongneirong_bianji_"+bianji_list.length);

	KindEditor.ready(function(K) { 
		editor[bianji_length] = K.create('textarea[name="huodongneirong_bianji_'+bianji_length+'"]',options);
	});

	var tr = $this_table.find("tr").last();
	tr.find('td').last().children("textarea").attr("name","huodongneirong_bianji_"+bianji_list.length);
	var bianji_length = bianji_list.length
	bianji_list.push("huodongneirong_bianji_"+bianji_list.length);

	KindEditor.ready(function(K) { 
		editor[bianji_length] = K.create('textarea[name="huodongneirong_bianji_'+bianji_length+'"]',options);
	});  

}

function addOption_3(b){
	if(readonly){
		return;
	}
	var $b = $(b);
	var current_row = b.parentNode.parentNode;
	var row_type = current_row.getAttribute("class");
	var current_index = current_row.rowIndex;
	var op_table = b.parentNode.parentNode.parentNode;
	var new_row = op_table.insertRow(current_index+1);

	var tr_html = weiyuan_html;
	new_row.innerHTML = tr_html;
	$(new_row).attr("class","tianjiaweiyuan");
}

function addOption_leixing(b){
	if(readonly){
		return;
	}
	var $b = $(b);
	var $this_table = $b.parents("table").eq(0);	
	var current_index = b.parentNode.parentNode.rowIndex;
	var pre_html = $this_table.find("tr").eq(current_index-1).html();
	var current_html = $this_table.find("tr").eq(current_index).html();
	
	
	$this_table.append("<tr>"+pre_html+"</tr>");
	$this_table.append("<tr>"+current_html+"</tr>");
	$this_table.append("<tr>"+youleixingdehuodongneirong_html+"</tr>");
	$this_table.append("<tr>"+youleixingdehuodongzongjie_html+"</tr>");

	var tr = $this_table.find("tr").last().prev();
	tr.find('td').last().children("textarea").attr("name","huodongneirong_bianji_"+bianji_list.length);
	var bianji_length = bianji_list.length
	bianji_list.push("huodongneirong_bianji_"+bianji_list.length);

	KindEditor.ready(function(K) { 
		editor[bianji_length] = K.create('textarea[name="huodongneirong_bianji_'+bianji_length+'"]',options);
	});

	var tr = $this_table.find("tr").last();
	tr.find('td').last().children("textarea").attr("name","huodongneirong_bianji_"+bianji_list.length);
	var bianji_length = bianji_list.length
	bianji_list.push("huodongneirong_bianji_"+bianji_list.length);

	KindEditor.ready(function(K) { 
		editor[bianji_length] = K.create('textarea[name="huodongneirong_bianji_'+bianji_length+'"]',options);
	});  
}

function delOption(b){
	if(readonly){
		return;
	}
	var $b = $(b);
	
	if($b.parents("table").eq(0).attr("name") == "jiangchengqingkuang"){
		
		var duixiang_cnt = 0;
		var this_class = $b.parents("tr").eq(0).attr("class");
		
		var tr_object = $b.parents("table").eq(0).find("tr");
		var tr_length = tr_object.length;
		for(var i = 0; i < tr_length; i ++){
			if(tr_object.eq(i).attr("class") == this_class){
				duixiang_cnt += 1;
			}
		}
		
		if(duixiang_cnt <= 1){
			return;
		}
	}
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
	if(readonly){
		return;
	}
	var current_row = b.parentNode.parentNode;
	var current_index = current_row.rowIndex;
	var op_table = b.parentNode.parentNode.parentNode;
	if(current_index == 1 && op_table.rows.length == 4)
	{
		alert("至少一条记录！");
		return;
	}
	op_table.deleteRow(current_index+2);
	op_table.deleteRow(current_index+1);
	op_table.deleteRow(current_index);
	op_table.deleteRow(current_index-1);
}

function exportt() {
	$.ajax({
		url: window.location.href,
		type: 'POST',
		data: {'op': 'export', 'year': $("#year").val()},
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

function export_single() {
	var a = $("li.active").children('a');
	var tab_id = parseInt(a.attr('id').slice(8));
	var tab_text = a.text();
	var title = $("#title").text();
	$.ajax({
		url: window.location.href,
		type: 'POST',
		data: {'op': 'export_single', 'year': $("#year").val(), "title": title, "tab_id": tab_id, "tab_text": tab_text},
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

function export_item(etype) {
	$.ajax({
		url: window.location.href,
		type: 'POST',
		data: {'op': 'export_item', 'title': $('#title').text(), 'etype': etype},
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
