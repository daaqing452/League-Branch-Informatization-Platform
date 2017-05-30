# -*- coding: utf-8 -*-
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from SUser.models import SUser
from SUser.utils import get_request_basis
from django.views.decorators.csrf import csrf_exempt
import json
import time

def message(request, mid=-1):
	rdata, op, suser = get_request_basis(request)
	jdata = {}

	if op == 'send_message':
		recvers = json.loads(request.POST.get('recver', '[]'))
		# 检查收件人
		check_recvers = 'yes'
		for recver in recvers:
			if recver == '': continue
			susers = SUser.objects.filter(username=recver)
			if len(susers) == 0:
				check_recvers = '用户"' + recver + '"不存在'
				break
		if check_recvers != 'yes':
			jdata['result'] = check_recvers
			return HttpResponse(json.dumps(jdata))
		# 发送
		title = request.POST.get('title')
		text = request.POST.get('text')
		return HttpResponse(json.dumps(jdata))

	return render(request, 'message.html', rdata)

@csrf_exempt 
def uploadFile(request):
	if request.method == 'POST':
		buf = request.FILES.get('imgFile', None)
		file_name = buf.name
		file_buff = buf.read()
		save_file("media", file_name, file_buff)
		dict_tmp = {}
		dict_tmp["error"] = 0
		dict_tmp["url"] = "/media/"+file_name
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