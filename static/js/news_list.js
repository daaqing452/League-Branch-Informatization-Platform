$(document).ready(function(){

});

function deletee(self) {
	var nid = $(self).attr('nid');
	$.ajax({
		url: window.location.pathname,
		type: 'POST',
		data: {'op': 'delete', 'nid': nid},
		success: function(data) {
			data = JSON.parse(data);
			alert('删除成功');
			window.location.reload();
		}
	});
}