# -*- coding: utf-8 -*-
from django.contrib import auth
from django.contrib.auth.models import User
from django.db.models import Q 
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from SUser.models import SUser, Department, Branch
from SUser.auth_tsinghua import auth_tsinghua
from SUser.utils import get_request_basis
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt 
def index(request):
	rdata, op, suser = get_request_basis(request)
	jdata = {}

	if op == 'login':
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		users = User.objects.filter(username=username)
		if len(users) == 0:
			jdata['result'] = '用户名不存在'
		else:
			# 如果不是root进行清华验证
			# if username != 'root':
			#	yes = auth_tsinghua(request, username, password)
			#	if yes:
			#		password = xxxx
			#	else:
			#		password = ''
			# 验证
			user = auth.authenticate(username=username, password=password)
			if user is not None:
				auth.login(request, user)
				jdata['result'] = '成功'
			else:
				jdata['result'] = '密码错误'
		return HttpResponse(json.dumps(jdata))

	if op == 'logout':
		auth.logout(request)
		return HttpResponse(json.dumps(jdata))

	if op == 'add_department':
		department = Department.objects.create(name=request.POST.get('name', ''))
		return HttpResponse(json.dumps(jdata))

	return render(request, 'index.html', rdata)

def department(request, did):
	rdata, op, suser = get_request_basis(request)
	rdata['department'] = department = Department.objects.filter(id=did)[0]
	rdata['branchs'] = branchs = Branch.objects.filter(did=did)
	jdata = {}

	if op == 'add_branch':
		branch = Branch.objects.create(name=request.POST.get('name', ''), did=did)
		print("ye")
		return HttpResponse(json.dumps(jdata))

	return render(request, 'department.html', rdata)

def branch(request, bid):
	rdata, op, suser = get_request_basis(request)
	rdata['branch'] = branch = Branch.objects.filter(id=bid)[0]
	jdata = {}
	return render(request, 'branch.html', rdata)

def delete_user(request, username):
	users = User.objects.filter(username=username)
	if len(users) > 0: users[0].delete()
	susers = SUser.objects.filter(username=username)
	html = 'no such user ' + username
	if len(susers) > 0:
		susers[0].delete()
		html = 'delete ' + username + ' successful'
	return HttpResponse(html)

def add_user(request, username):
	password = username
	user = auth.authenticate(username=username, password=password)
	admin = False
	if username == 'root': admin = True
	if user is None:
		user = User.objects.create_user(username=username, password=password)
		suser = SUser.objects.create(username=username, uid=user.id, admin_super=admin, admin_school=admin)
		html = 'add ' + username + ' successful'
	else:
		html = username + ' already exists'
	return HttpResponse(html)