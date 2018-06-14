function add_one(){
	$.ajax({
		url: '/announcement_tip/00000/',
		type: 'POST',
		data: {'op': 'create'},
		success: function(data) {
			data = JSON.parse(data);
			window.location.href = '/announcement_tip/' + data['hid'] + '/'
		}
	});
}

function delete_help(obj) {
	if (confirm('确认删除？')) {
		var td = $(obj);
		var hid = td.attr('hid');
		$.ajax({
			url: '/announcement_tip/' + hid + '/',
			type: 'POST',
			data: {'op': 'delete'},
			success: function(data) {
				data = JSON.parse(data);
				td.parent().remove();
			}
		});
	}
}