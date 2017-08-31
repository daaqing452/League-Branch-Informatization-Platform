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
from Message.models import Message, News, JiatuanMaterial
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

	if op == 'get_departments_jiatuan':
		year = request.POST.get('year')
		departments = []
		for department in Department.objects.all():
			d = {}
			d['did'] = department.id
			d['name'] = department.name
			materials = JiatuanMaterial.objects.filter(htype='d', review_id=0, submit_id=department.id, year=year)
			if len(materials) > 0:
				attachment = json.loads(materials[0].attachment)
				if len(attachment) > 0: d['material'] = attachment[0][1]
			departments.append(d)
		jdata['departments'] = departments
		return HttpResponse(json.dumps(jdata))

	if op == 'submit_minge':
		year = request.POST.get('year')
		minges = json.loads(request.POST.get('minges'))
		for minge in minges:
			department = Department.objects.get(id=minge['did'])
			department_admin = json.loads(department.admin)
			for everyone in department_admin:
				message = Message.objects.create(recv_uid=everyone, send_uid=suser.id, mtype=1, send_time=datetime.datetime.now(), title='甲团名额分配', text=str(year)+'年'+department.name+'院系甲团名额：'+str(minge['value']))
		return HttpResponse(json.dumps(jdata))

	news_list = News.objects.filter(display_type='i')
	rdata['news_list'] = news_list
	rdata['slide_list'] = json.loads(School.objects.all()[0].slide)
	return render(request, 'index.html', rdata)

def department(request, did):
	rdata, op, suser = get_request_basis(request)
	if did != '0':
		rdata['department'] = department = Department.objects.get(id=did)
		rdata['branchs'] = branchs = Branch.objects.filter(did=did)
		rdata['is_admin'] = is_admin = (suser is not None) and (suser.admin_super or (suser.id in json.loads(department.admin)))
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

	if op == 'get_branchs_jiatuan':
		year = request.POST.get('year')
		branchs = []
		for branch in Branch.objects.filter(did=did):
			d = {}
			d['bid'] = branch.id
			d['name'] = branch.name
			materials = JiatuanMaterial.objects.filter(htype='b', review_id=did, submit_id=branch.id, year=year)
			if len(materials) > 0:
				attachment = json.loads(materials[0].attachment)
				if len(attachment) > 0: d['material'] = attachment[0][1]
			branchs.append(d)
		jdata['branchs'] = branchs
		return HttpResponse(json.dumps(jdata))

	if op == 'jiatuan_inform':
		year = request.POST.get('year')
		jiatuans = json.loads(request.POST.get('jiatuans'))
		for jiatuan in jiatuans:
			branch = Branch.objects.get(id=jiatuan)
			branch_admin = json.loads(branch.admin)
			for everyone in branch_admin:
				message = Message.objects.create(recv_uid=everyone, send_uid=suser.id, mtype=1, send_time=datetime.datetime.now(), title='甲团评选结果', text='恭喜'+branch.name+'团支部获得'+str(year)+'年甲级团支部称号！请向院系提交甲团材料。')
		return HttpResponse(json.dumps(jdata))

	if op == 'submit_jiatuan_material':
		year = request.POST.get('year')
		title = request.POST.get('title')
		text = request.POST.get('text')
		attachment = request.POST.get('attachment')
		materials = JiatuanMaterial.objects.filter(htype='d', review_id=0, submit_id=department.id, year=year)
		if len(materials) > 0: materials[0].delete();
		material = JiatuanMaterial.objects.create(htype='d', review_id=0, submit_id=department.id, year=year, attachment=attachment)
		return HttpResponse(json.dumps(jdata))

	if (department is not None) and (suser is not None):
		news_list = News.objects.filter(display_type='d', display_id=did)
		rdata['news_list'] = news_list
		rdata['slide_list'] = json.loads(department.slide)
		return render(request, 'department.html', rdata)
	else:
		return HttpResponseRedirect('/index/')

def branch(request, bid):
	rdata, op, suser = get_request_basis(request)
	if bid != '0':
		rdata['branch'] = branch = Branch.objects.get(id=bid)
		rdata['department'] = department = Department.objects.get(id=branch.did)
		rdata['is_admin'] = is_admin = (suser is not None) and (suser.admin_super or (suser.id in json.loads(branch.admin)))
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

	if op == 'submit_jiatuan_material':
		year = request.POST.get('year')
		title = request.POST.get('title')
		text = request.POST.get('text')
		attachment = request.POST.get('attachment')
		materials = JiatuanMaterial.objects.filter(htype='b',review_id=department.id, submit_id=branch.id, year=year)
		if len(materials) > 0: materials[0].delete();
		material = JiatuanMaterial.objects.create(htype='b', review_id=department.id, submit_id=branch.id, year=year, attachment=attachment)
		return HttpResponse(json.dumps(jdata))

	if (branch is not None) and (suser is not None) and (suser.admin_school or ((rdata['self_department'] is not None) and (rdata['self_department'].id == department.id))):
		news_list = News.objects.filter(display_type='b', display_id=bid)
		rdata['news_list'] = news_list
		rdata['slide_list'] = json.loads(branch.slide)
		return render(request, 'branch.html', rdata)
	else:
		return HttpResponseRedirect('/index/')

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
