# -*- coding: utf-8 -*-
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from SUser.models import SUser
from SUser.utils import get_request_basis
import json

def message(request, mid=-1):
	rdata, op, suser = get_request_basis(request)
	jdata = {}

	if op == 'check_recver':
		recvers = json.loads(request.POST.get('recver', '[]'))
		jdata['result'] = 'yes'
		for recver in recvers:
			if recver == '': continue
			susers = SUser.objects.filter(username=recver)
			if len(susers) == 0:
				jdata['result'] = '用户"' + recver + '"不存在'
				break
		return HttpResponse(json.dumps(jdata))

	return render(request, 'message.html', rdata)