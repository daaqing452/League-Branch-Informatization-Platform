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

def handbook(request, htype, hid):
	rdata, op, suser = get_request_basis(request)
	jdata = {}

	if htype == 'd':
		department = Department.objects.get(id=hid)
		branch = None
		admin_department = json.loads(department.admin)
		admin_branch = []
	elif htype == 'b':
		branch = Branch.objects.get(id=hid)
		department = Department.objects.get(id=branch.did)
		admin_department = json.loads(department.admin)
		admin_branch = json.loads(branch.admin)

	if op == 'submit':
		content = request.POST.get('content')
		if htype == 'd':
			Handbook.objects.create(htype=htype, review_id=0, submit_id=department.id, content=content)
		elif htype == 'b':
			Handbook.objects.create(htype=htype, review_id=department.id, submit_id=branch.id, content=content)
		return HttpResponse(json.dumps(jdata))

	# 权限检测
	if (suser is not None) and (suser.admin_super or suser.admin_school or (suser.id in admin_department) or (suser.id in admin_branch)):
		return render(request,'handbook.html', rdata)
