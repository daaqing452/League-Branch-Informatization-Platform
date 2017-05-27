# -*- coding: utf-8 -*-
from django.contrib import auth
from django.contrib.auth.models import User
from django.db.models import Q 
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from SUser.models import SUser
from SUser.auth_tsinghua import auth_tsinghua
import json

def index(request):
	rdata = {}
	op = request.POST.get('op', '')

	# 检查登录状态
	user = None
	if request.user.is_authenticated():
		user = request.user
		suser = SUser.objects.filter(username=user.username)[0]
		rdata['username'] = user.username
		print(suser.authority)
		authority = json.loads(suser.authority)
		rdata['admin'] = authority['school']
	rdata['login'] = user is not None

	if op == 'login':
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		users = User.objects.filter(username=username)
		if len(users) == 0:
			rdata['result'] = '用户名不存在'
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
				rdata['result'] = '成功'
			else:
				rdata['result'] = '密码错误'
		return HttpResponse(json.dumps(rdata))

	if op == 'logout':
		auth.logout(request)
		return HttpResponse(json.dumps(rdata))

	return render(request, 'index.html', rdata)

def setting(request):
	rdata = {}
	return render(request, 'setting.html', rdata)

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
	authority = {'super': False, 'school': False, 'department': [], 'branch': [], 'visit': []}
	if username == 'root': authority['super'] = authority['school'] = True
	if user is None:
		user = User.objects.create_user(username=username, password=password)
		suser = SUser.objects.create(username=username, uid=user.id, authority=json.dumps(authority))
		html = 'add ' + username + ' successful'
	else:
		html = username + ' already exists'
	return HttpResponse(html)