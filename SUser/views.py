# -*- coding: utf-8 -*-
from django.contrib import auth
from django.contrib.auth.models import User
from django.db.models import Q 
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from SUser.models import SUser, School, Department, Branch
from SUser.auth_tsinghua import auth_tsinghua
from SUser.utils import get_request_basis
from Message.models import Message, News
import datetime
import json
import random

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

	if op == 'apply':
		group = random.randint(1, 0x3fffffff) * (random.randint(0, 1) * 2 - 1)
		atype = int(request.POST.get('type'))
		if atype == 0:
			mtype = 2
			recv_uids = [ SUser.objects.get(admin_super=True).id ]
			text = suser.username + ' 申请校管理员'
			meta = {}
		elif atype == 1:
			mtype = 3
			department = Department.objects.get(id=request.POST.get('did'))
			recv_uids = [ recver.id for recver in SUser.objects.filter(admin_school=True) ]
			text = suser.username + ' 申请 ' + department.name + ' 的管理员'
			meta = {'did': department.id}
		elif atype == 2:
			mtype = 4
			department = Department.objects.get(id=request.POST.get('did'))
			branch = Branch.objects.get(id=request.POST.get('bid'))
			recv_uids = json.loads(department.admin)
			text = suser.username + ' 申请 ' + branch.name + ' 的管理员'
			meta = {'did': department.id, 'bid': branch.id}
		elif atype == 3:
			mtype = 5
			department = Department.objects.get(id=request.POST.get('did'))
			branch = Branch.objects.get(id=request.POST.get('bid'))
			recv_uids = json.loads(branch.admin)
			text = suser.username + ' 申请 ' + branch.name + ' 的成员'
			meta = {'did': department.id, 'bid': branch.id}
		for recv_uid in recv_uids:
			message = Message.objects.create(recv_uid=recv_uid, send_uid=suser.id, group=group, mtype=mtype, send_time=datetime.datetime.now(), title='权限申请', text=text, meta=json.dumps(meta))
		return HttpResponse(json.dumps(jdata))

	news_list = News.objects.filter(display_type='i')
	rdata['news_list'] = news_list
	rdata['slides'] = json.loads(School.objects.all()[0].slide)
	print(json.loads(School.objects.all()[0].slide)[1])
	return render(request, 'index.html', rdata)

def department(request, did):
	rdata, op, suser = get_request_basis(request)
	if did != '0':
		rdata['department'] = department = Department.objects.get(id=did)
		rdata['branchs'] = branchs = Branch.objects.filter(did=did)
		admin = json.loads(department.admin)
		rdata['is_admin'] = (suser is not None) and (suser.admin_super or (suser.id in admin))
	jdata = {}

	if op == 'add_branch':
		branch = Branch.objects.create(name=request.POST.get('name', ''), did=did)
		return HttpResponse(json.dumps(jdata))

	if op == 'get_departments':
		departments = []
		for department in Department.objects.all():
			d = {}
			d['did'] = department.id
			d['name'] = department.name
			departments.append(d)
		jdata['departments'] = departments
		return HttpResponse(json.dumps(jdata))

	news_list = News.objects.filter(display_type='d', display_id=did)
	rdata['news_list'] = news_list
	return render(request, 'department.html', rdata)

def branch(request, bid):
	rdata, op, suser = get_request_basis(request)
	if bid != '0':
		rdata['branch'] = branch = Branch.objects.get(id=bid)
		rdata['department'] = department = Department.objects.get(id=branch.did)
		admin = json.loads(branch.admin)
		rdata['is_admin'] = (suser is not None) and (suser.admin_super or (suser.id in admin))
	jdata = {}

	if op == 'get_branchs':
		did = int(request.POST.get("did", -1))
		branchs = []
		for branch in Branch.objects.filter(did=did):
			d = {}
			d['bid'] = branch.id
			d['name'] = branch.name
			branchs.append(d)
		jdata['branchs'] = branchs
		return HttpResponse(json.dumps(jdata))

	news_list = News.objects.filter(display_type='b', display_id=bid)
	rdata['news_list'] = news_list
	return render(request, 'branch.html', rdata)

def profile(request, sid):
	rdata, op, suser = get_request_basis(request)
	return render(request, 'profile.html', rdata)

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
