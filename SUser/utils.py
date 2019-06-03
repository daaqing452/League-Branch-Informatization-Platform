# -*- coding: utf-8 -*-
from django.contrib import auth
from django.contrib.auth.models import User
from SUser.models import *
from Message.models import *
import json
import random
import time

MAX_ITEM_ON_HELP = 6

def get_request_basis_identity(rdata, suser, unserial=True):
	# 个人归属
	rdata['self_admin_school'] = False
	rdata['self_department'] = None
	rdata['self_admin_department'] = False
	rdata['self_branch'] = None
	rdata['self_admin_branch'] = False
	if suser is not None:
		if suser.admin_school: rdata['self_admin_school'] = True
		for department in Department.objects.all():
			if suser.id in json.loads(department.admin):
				rdata['self_admin_department'] = True
				if unserial:
					rdata['self_department'] = department
				else:
					rdata['self_department'] = '/department/' + str(department.id) + '/'
				break
		for branch in Branch.objects.all():
			branch_admin = False
			if suser.id in json.loads(branch.admin):
				rdata['self_admin_branch'] = True
				branch_admin = True
			if suser.id in json.loads(branch.member) or branch_admin:
				if unserial:
					rdata['self_branch'] = branch
					rdata['self_department'] = Department.objects.get(id=branch.did)
				else:
					rdata['self_branch'] = '/branch/' + str(branch.id) + '/'
				break

def get_request_basis(request):
	rdata = {}
	op = request.POST.get('op', '')
	
	# 检查登录状态
	suser = None
	if request.user.is_authenticated:
		suser = SUser.objects.filter(username=request.user.username)[0]
		rdata['suser'] = suser
	rdata['login'] = suser is not None
	get_request_basis_identity(rdata, suser)

	# 院系
	if suser is not None:
		if suser.admin_school:
			departments = Department.objects.order_by('amt_order')
		else:
			department = rdata['self_department']
			departments = [department] if (department is not None) else []
		d0 = []
		for department in departments:
			d1 = {}
			d1['department'] = department
			d1['branchs'] = [{'branch': branch} for branch in Branch.objects.filter(did=department.id).order_by('amt_order')]
			d0.append(d1)
		rdata['departments'] = d0

	# 消息
	messages = []
	if suser is not None:
		messages = Message.objects.filter(recv_uid=suser.id).filter(read=False)
	rdata['unread_messages'] = messages
	rdata['unread_messages_length'] = len(messages)

	rdata['years'] = json.loads(School.objects.all()[0].years)

	# 通知公告、优秀支部案例、规范文件
	helps = list(reversed(Help.objects.filter(released=True)))
	helps = helps[:min(len(helps), MAX_ITEM_ON_HELP)]
	rdata['helps'] = helps
	chelps = list(reversed(CHelp.objects.filter(released=True)))
	chelps = chelps[:min(len(chelps), MAX_ITEM_ON_HELP)]
	rdata['chelps'] = chelps
	ahelps = list(reversed(AHelp.objects.filter(released=True)))
	ahelps = ahelps[:min(len(ahelps), MAX_ITEM_ON_HELP)]
	rdata['ahelps'] = ahelps

	return rdata, op, suser

def upload_file(raw):
	f_path = 'media/' + time.strftime('%Y%m%d%H%M%S') + '-' + raw.name
	f = open(f_path, 'wb')
	for chunk in raw.chunks():
		f.write(chunk)
	f.close()
	return f_path

def permission(suser, opt, par=None):
	login = (suser is not None)
	if opt[0] == 'i':
		# permission(suser, 'ir')
		# permission(suser, 'iw')
		if opt[1] == 'r':
			return True
		elif opt[1] == 'w':
			return login and suser.admin_school
	elif opt[0] == 'd':
		# permission(suser, 'dr', department)
		# permission(suser, 'dw', department)
		if opt[1] == 'r':
			return login
		elif opt[1] == 'w':
			return login and (suser.admin_super or (suser.id in json.loads(par.admin)))
	elif opt[0] == 'b':
		# permission(suser, 'br', [my_department, visit_department])
		# permission(suser, 'bw', branch)
		if opt[1] == 'r':
			return login and (suser.admin_school or ((par[0] is not None) and (par[1] is not None) and (par[0].id == par[1].id)))
		if opt[1] == 'w':
			return login and (suser.admin_super or (suser.id in json.loads(par.admin)))

def get_random_group():
	group = random.randint(1, 0x3fffffff) * (random.randint(0, 1) * 2 - 1)
	return group