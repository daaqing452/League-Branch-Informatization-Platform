# -*- coding: utf-8 -*-
from django.contrib import auth
from django.contrib.auth.models import User
from django.db.models import Q 
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from SUser.auth_tsinghua import auth_tsinghua
from SUser.models import *
from SUser.utils import *
from Message.models import *
import codecs
import datetime
import json
import random

NEWS_SHOW_NUM = 8
SLIDE_SHOW_NUM = 5


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
				suser = SUser.objects.filter(username=user.username)[0]
				get_request_basis_identity(jdata, suser, False)
				jdata['result'] = '成功'
			else:
				jdata['result'] = '密码错误'
		return HttpResponse(json.dumps(jdata))

	if op == 'logout':
		auth.logout(request)
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
		jiatuan_dict = {}
		for material in JiatuanMaterial.objects.filter(year=year):
			branch = Branch.objects.get(id=material.submit_id)
			department = Department.objects.get(id=branch.did)
			if not department.id in jiatuan_dict: jiatuan_dict[department.id] = []
			d = {}
			d['name'] = branch.name
			d['material'] = '/jiatuan/' + str(material.id) + '/'
			handbooks = Handbook.objects.filter(htype='b', year=year, submit_id=branch.id)
			if len(handbooks) > 0:
				d['handbook'] = '/handbook/' + str(handbooks[0].id) + '/'
			jiatuan_dict[department.id].append(d)
		departments = []
		for department in Department.objects.all():
			d = {}
			d['did'] = department.id
			d['name'] = department.name
			if department.id in jiatuan_dict:
				d['jiatuans'] = jiatuan_dict[department.id]
			departments.append(d)
		jdata['departments'] = departments
		print(jdata)
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

	# 导入院系管理员名单
	f = request.FILES.get('upload', None)
	if not f is None:
		f_path = upload_file(f)
		f = codecs.open(f_path, 'r', 'gbk')
		line_no = -1
		while True:
			line_no += 1
			try:
				line = f.readline()
			except:
				print('第' + str(line_no + 1) + '行读入失败')
				continue
			if len(line) == 0: break
			if line[-2:] == '\r\n': line = line[:-2]
			if line[-1:] == '\n': line = line[:-1]
			arr = line.split(',')
			username = arr[0]
			department_name = arr[1]
			susers = SUser.objects.filter(username=username)
			if len(susers) == 0:
				password = username
				user = User.objects.create_user(username=username, password=password)
				suser = SUser.objects.create(username=username, uid=user.id)
			else:
				suser = susers[0]
			departments = Department.objects.filter(name=department_name)
			if len(departments) == 0:
				print('第' + str(line_no + 1) + '行导入失败')
			else:
				department = departments[0]
				admin = json.loads(department.admin)
				if not suser.id in admin:
					admin.append(suser.id)
				else:
					print('第' + str(line_no + 1) + '行重复')
				department.admin = json.dumps(admin)
				department.save()
		f.close()

	rdata['is_admin'] = permission(suser, 'iw')
	if permission(suser, 'ir'):
		news_list = News.objects.filter(display_type='i')
		rdata['news_list'] = list(reversed(news_list))[0:min(len(news_list), NEWS_SHOW_NUM)]
		slide_list = Slide.objects.filter(display_type='i')
		rdata['slide_list'] = list(reversed(slide_list))[0:min(len(slide_list), SLIDE_SHOW_NUM)]
		return render(request, 'index.html', rdata)

def department(request, did):
	rdata, op, suser = get_request_basis(request)
	if did != '0':
		rdata['department'] = department = Department.objects.get(id=did)
		rdata['branchs'] = branchs = Branch.objects.filter(did=did)
		rdata['is_admin'] = is_admin = permission(suser, 'dw', department)
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
			materials = JiatuanMaterial.objects.filter(submit_id=branch.id, year=year)
			if len(materials) > 0:
				# attachment = json.loads(materials[0].attachment)
				# if len(attachment) > 0: d['material'] = attachment[0][1]
				d['material'] = '/jiatuan/' + str(materials[0].id) + '/'
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

	# 导入团支部列表
	f = request.FILES.get('upload', None)
	if not f is None:
		f_path = upload_file(f)
		f = codecs.open(f_path, 'r', 'gbk')
		line_no = -1
		while True:
			line_no += 1
			try:
				line = f.readline()
			except:
				print('第' + str(line_no + 1) + '行读入失败')
				continue
			if len(line) == 0: break
			if line[-2:] == '\r\n': line = line[:-2]
			if line[-1:] == '\n': line = line[:-1]
			branch_name = line
			branchs = Branch.objects.filter(name=branch_name)
			if len(branchs) == 0:
				branch = Branch.objects.create(name=branch_name, did=department.id)
			else:
				print('第' + str(line_no + 1) + '行重复')
		f.close()

	if (department is not None) and permission(suser, 'dr', department):
		news_list = News.objects.filter(display_type='d', display_id=did)
		rdata['news_list'] = list(reversed(news_list))[0:min(len(news_list), NEWS_SHOW_NUM)]
		slide_list = Slide.objects.filter(display_type='d', display_id=did)
		rdata['slide_list'] = list(reversed(slide_list))[0:min(len(slide_list), SLIDE_SHOW_NUM)]
		return render(request, 'department.html', rdata)
	else:
		return HttpResponseRedirect('/index/')

def branch(request, bid):
	rdata, op, suser = get_request_basis(request)
	if bid != '0':
		rdata['branch'] = branch = Branch.objects.get(id=bid)
		rdata['department'] = department = Department.objects.get(id=branch.did)
		rdata['is_admin'] = is_admin = permission(suser, 'bw', branch)
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

	# 导入班级成员名单
	f = request.FILES.get('upload', None)
	if not f is None:
		f_path = upload_file(f)
		f = codecs.open(f_path, 'r', 'gbk')
		line_no = -1
		member = json.loads(branch.member)
		while True:
			line_no += 1
			try:
				line = f.readline()
			except:
				print('第' + str(line_no + 1) + '行读入失败')
				continue
			if len(line) == 0: break
			if line[-2:] == '\r\n': line = line[:-2]
			if line[-1:] == '\n': line = line[:-1]
			username = line
			susers = SUser.objects.filter(username=username)
			if len(susers) == 0:
				password = username
				user = User.objects.create_user(username=username, password=password)
				suser = SUser.objects.create(username=username, uid=user.id)
			else:
				suser = susers[0]
			if not suser.id in member:
				member.append(suser.id)
			else:
				print('第' + str(line_no + 1) + '行重复')
		f.close()
		branch.member = json.dumps(member)
		branch.save()
		# 会丧失其他数据导致跳到index

	if (branch is not None) and permission(suser, 'br', [rdata['self_department'], department]):
		news_list = News.objects.filter(display_type='b', display_id=bid)
		rdata['news_list'] = list(reversed(news_list))[0:min(len(news_list), NEWS_SHOW_NUM)]
		slide_list = Slide.objects.filter(display_type='b', display_id=bid)
		rdata['slide_list'] = list(reversed(slide_list))[0:min(len(slide_list), SLIDE_SHOW_NUM)]
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

def amt_setting(request, amttype, did):
	rdata, op, suser = get_request_basis(request)
	
	if amttype == 'i':
		# 权限检测
		if permission(suser, 'iw'):
			rdata['amttype'] = 'i'
			rdata['departments'] = departments = Department.objects.order_by('amt_order')

			if op == 'add_department':
				department = Department.objects.create(name=request.POST.get('name', ''))
				department.amt_order=department.id
				department.save()
				return HttpResponse(json.dumps({}))

			if op == 'rename_department':
				Department.objects.filter(id=int(request.POST.get('did'))).update(name=request.POST.get('name'))
				return HttpResponse(json.dumps({}))

			return render(request, 'amt_setting.html', rdata)
		else:
			return HttpResponseRedirect('/index/')

	return HttpResponseRedirect('/index/')