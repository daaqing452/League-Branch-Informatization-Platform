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
		if check_recvers != 'yes':
			jdata['result'] = check_recvers
			return HttpResponse(json.dumps(jdata))
		# 逐条发送
		for recver_uid in recver_uids:
			message = Message.objects.create(recv_uid=recver_uid, send_uid=suser.id, read=False, m_type=1, send_time=datetime.datetime.now(), title=request.POST.get('title'), text=request.POST.get('text'), attachment=json.dumps('[]'))
		return HttpResponse(json.dumps(jdata))

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