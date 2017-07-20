# -*- coding: utf-8 -*-
from django.contrib import auth
from django.contrib.auth.models import User
from django.db.models import Q 
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from SUser.models import SUser, Department, Branch
from SUser.utils import get_request_basis
from Handbook.models import Handbook
import json

def handbook(request, htype, id0):
	rdata, op, suser = get_request_basis(request)
	jdata = {}

	if op == 'get_handbook_list':
		if htype == 'd':
			handbooks = Handbook.objects.filter(htype=htype, review_id=0)
			l = []
			for handbook in handbooks:
				department = Department.objects.get(id=handbook.submit_id)
				l.append({'hid': handbook.id, 'title': department.name})
		if htype == 'b':
			handbooks = Handbook.objects.filter(htype=htype, review_id=request.POST.get('did'))
			l = []
			for handbook in handbooks:
				branch = Branch.objects.get(id=handbook.submit_id)
				l.append({'hid': handbook.id, 'title': branch.name})

		print('xx', len(l))
		jdata['handbooks'] = l
		return HttpResponse(json.dumps(jdata))

	if htype == 'd':
		department = Department.objects.get(id=id0)
		branch = None
		admin_department = json.loads(department.admin)
		admin_branch = []
	elif htype == 'b':
		branch = Branch.objects.get(id=id0)
		department = Department.objects.get(id=branch.did)
		admin_department = []
		admin_branch = json.loads(branch.admin)

	if op == 'submit':
		content = request.POST.get('content')
		if htype == 'd':
			Handbook.objects.create(htype=htype, review_id=0, submit_id=department.id, content=content)
		elif htype == 'b':
			Handbook.objects.create(htype=htype, review_id=department.id, submit_id=branch.id, content=content)
		return HttpResponse(json.dumps(jdata))

	if htype == 'd':
		rdata['title'] = '院系工作手册'
	elif htype == 'b':
		rdata['title'] = '团支部工作手册'

	# 权限检测
	if (suser is not None) and (suser.admin_super or (suser.id in admin_department) or (suser.id in admin_branch)):
		return render(request,'handbook.html', rdata)
