# -*- coding: utf-8 -*-
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from SUser.models import SUser
from SUser.utils import get_request_basis
from django.views.decorators.csrf import csrf_exempt
from Message.models import Message
import datetime
import json
import time

# m_type
#   0: 预留
#   1: 用户发送
def message(request, mid=-1):
	rdata, op, suser = get_request_basis(request)
	jdata = {}

	if op == 'send_message':
		recvers = json.loads(request.POST.get('recver', '[]'))
		# 检查收件人
		check_recvers = 'yes'
		recver_uids = []
		for recver in recvers:
			if recver == '': continue
			susers = SUser.objects.filter(username=recver)
			if len(susers) == 0:
				check_recvers = '用户"' + recver + '"不存在'
				break
			recver_uids.append(susers[0].id)
		jdata['result'] = check_recvers
		if check_recvers != 'yes':
			return HttpResponse(json.dumps(jdata))
		# 逐条发送
		for recver_uid in recver_uids:
			message = Message.objects.create(recv_uid=recver_uid, send_uid=suser.id, read=False, mtype=1, send_time=datetime.datetime.now(), title=request.POST.get('title'), text=request.POST.get('text'), attachment=request.POST.get('attachment'))
		return HttpResponse(json.dumps(jdata))

	if op == 'read_message':
		messages = Message.objects.filter(id=request.POST.get('mid'))
		if len(messages) > 0:
			message = messages[0]
			jdata['send_username'] = SUser.objects.get(id=message.send_uid).username
			jdata['mtype'] = message.mtype
			jdata['send_time'] = message.send_time.strftime("%Y-%m-%d %H:%M:%S")
			jdata['title'] = message.title
			if jdata['title'] == '': jdata['title'] = '（无标题）'
			jdata['text'] = message.text
			jdata['attachment'] = message.attachment
		return HttpResponse(json.dumps(jdata))

	if op == 'close_message':
		messages = Message.objects.filter(id=request.POST.get('mid'))
		if len(messages) > 0:
			message = messages[0]
			message.read = True
			message.save()
		return HttpResponse(json.dumps(jdata))

	if suser is None:
		return HttpResponseRedirect('/index/')

	if mid == -1:
		rdata['read_all'] = True
		messages = Message.objects.filter(recv_uid=suser.id)
		re_messages = []
		for message in messages:
			d = {}
			d['id'] = message.id
			d['read'] = message.read
			d['title'] = message.title
			if d['title'] == '': d['title'] = '（无标题）'
			d['send_username'] = SUser.objects.get(id=message.send_uid).username
			d['send_time'] = message.send_time.strftime("%Y-%m-%d %H:%M:%S")
			re_messages.append(d);
		rdata['messages'] = re_messages
	return render(request, 'message.html', rdata)

@csrf_exempt 
def uploadFile(request):
	if request.method == 'POST':
		buf = request.FILES.get('imgFile', None)
		file_name = buf.name
		file_buff = buf.read()
		time_stamp = time.strftime('%Y%m%d%H%M%S')
		real_file_name = str(time_stamp)+"-"+file_name
		save_file("media", real_file_name, file_buff)
		dict_tmp = {}
		dict_tmp["error"] = 0
		dict_tmp["url"] = "/media/"+file_name
		dict_tmp["real_url"] = "/media/"+ real_file_name
		return HttpResponse(json.dumps(dict_tmp))

def save_file(path, file_name, data):
    if data == None:
        return
    if(not path.endswith("/")):
        path=path+"/"
    file=open(path+file_name, "wb")
    file.write(data)
    file.flush()
    file.close()