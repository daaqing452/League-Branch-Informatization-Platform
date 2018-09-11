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


@csrf_exempt 
def index(request):
	rdata, op, suser = get_request_basis(request)
	jdata = {}

	if op == 'login':
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')

		if username is not None and password is not None:
			users = User.objects.filter(username=username)
			existed = (len(users) > 0)
			
			# 清华账号
			if username.isdigit() and len(username) == 10:
				yes = auth_tsinghua(request, username, password)
				if yes:
					# 不存在就新建
					if not existed:
						password = Utils.hash_md5(username)
						user = User.objects.create_user(username=username, password=password)
						suser = SUser.objects.create(uid=user.id, username=username)
					# 登录
					user = auth.authenticate(username=username, password=password)
					auth.login(request, user)
					jdata['result'] = '成功'
				else:
					jdata['result'] = '密码错误'
			
			# 非清华账号
			else:
				if existed:
					user = auth.authenticate(username=username, password=password)
					if user is not None:
						auth.login(request, user)
						jdata['result'] = '成功'
					else:
						jdata['result'] = '密码错误'
				else:
					jdata['result'] = '用户名不存在'

		return HttpResponse(json.dumps(jdata))

		'''users = User.objects.filter(username=username)
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
		return HttpResponse(json.dumps(jdata))'''

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

	if op == 'get_apportion':
		year = request.POST.get('year')
		apportions = JiatuanApportion.objects.filter(year=year)
		if len(apportions) > 0:
			apportion = apportions[0]
			jdata['deadline'] = apportion.deadline.strftime('%Y-%m-%d')
			minge = json.loads(apportion.minge)
		else:
			jdata['deadline'] = '2099-01-01'
			minge = {}

		jiatuan_dict = {}
		for material in JiatuanMaterial.objects.filter(year=year):
			branchs = Branch.objects.filter(id=material.submit_id)
			if len(branchs) == 0: continue
			branch = branchs[0]
			departments = Department.objects.filter(id=branch.did)
			if len(departments) == 0: continue
			department = departments[0]
			if not department.id in jiatuan_dict: jiatuan_dict[department.id] = []
			assignments = JiatuanAssignment.objects.filter(year=year, did=department.id)
			if len(assignments) == 0: continue
			jiatuan_branchs = json.loads(assignments[0].branchs)
			if not str(branch.id) in jiatuan_branchs: continue
			d = {}
			d['name'] = branch.name
			d['material'] = '/jiatuan/' + str(material.id) + '/'
			handbooks = Handbook.objects.filter(htype='b', year=year, submit_id=branch.id)
			if len(handbooks) > 0:
				d['handbook'] = '/handbook/' + str(handbooks[0].id) + '/'
			jiatuan_dict[department.id].append(d)
		departments = []
		for department in Department.objects.order_by('amt_order'):
			d = {}
			d['did'] = department.id
			d['name'] = department.name
			if department.id in jiatuan_dict:
				d['jiatuans'] = jiatuan_dict[department.id]
			if str(department.id) in minge.keys():
				d['minge'] = minge[str(department.id)]
			else:
				d['minge'] = 0
			assignments = JiatuanAssignment.objects.filter(year=year, did=department.id)
			d['submitted'] = (len(assignments) > 0 and assignments[0].submitted)
			departments.append(d)
		jdata['departments'] = departments
		return HttpResponse(json.dumps(jdata))

	if op == 'submit_apportion':
		year = request.POST.get('year')
		apportions = JiatuanApportion.objects.filter(year=year)
		if len(apportions) > 0:
			apportion = apportions[0]
		else:
			apportion = JiatuanApportion.objects.create(year=year)
		apportion.deadline = datetime.datetime.strptime(request.POST.get('deadline') + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
		minge_dict = {}
		minges = json.loads(request.POST.get('minges'))
		for minge in minges:
			department = Department.objects.get(id=minge['did'])
			department_admin = json.loads(department.admin)
			minge_dict[department.id] = int(minge['value'])
			for everyone in department_admin:
				message = Message.objects.create(recv_uid=everyone, send_uid=suser.id, mtype=1, send_time=datetime.datetime.now(), title='甲团名额分配', text=str(year)+'年'+department.name+'院系甲团名额：'+str(minge['value']))
		apportion.minge = json.dumps(minge_dict)
		apportion.save()
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
		slide_list = Slide.objects.filter(display_type='i', show=True)
		rdata['slide_list'] = list(reversed(slide_list))[0:min(len(slide_list), School.objects.all()[0].slide_show_num)]
		return render(request, 'index.html', rdata)

def department(request, did):
	rdata, op, suser = get_request_basis(request)
	if did != '0':
		rdata['department'] = department = Department.objects.get(id=did)
		rdata['branchs'] = branchs = Branch.objects.filter(did=did)
		rdata['is_admin'] = is_admin = permission(suser, 'dw', department)
	jdata = {}

	if op == 'get_departments':
		departments = []
		for department in Department.objects.order_by('amt_order'):
			d = {}
			d['did'] = department.id
			d['name'] = department.name
			departments.append(d)
		jdata['departments'] = departments
		return HttpResponse(json.dumps(jdata))

	if op == 'get_jiatuan_branchs':
		year = request.POST.get('year')
		apportions = JiatuanApportion.objects.filter(year=year)
		status = 0
		if len(apportions) > 0:
			apportion = apportions[0]
			if datetime.datetime.now() > apportion.deadline.replace(tzinfo=None):
				status = 2
			else:
				minge = json.loads(apportion.minge)
				if str(department.id) in minge:
					status = 1
					jdata['minge'] = minge[str(department.id)]
		jdata['status'] = status
		branchs = []
		for branch in Branch.objects.filter(did=did).order_by('amt_order'):
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
		assignments = JiatuanAssignment.objects.filter(year=year, did=department.id)
		if len(assignments) > 0:
			jdata['assigned'] = True
			jdata['assigned_branchs'] = assignments[0].branchs
			jdata['submitted'] = assignments[0].submitted
		else:
			jdata['assigned'] = False
		return HttpResponse(json.dumps(jdata))

	if op == 'jiatuan_inform':
		year = request.POST.get('year')
		jiatuans = json.loads(request.POST.get('jiatuans'))
		apportions = JiatuanApportion.objects.filter(year=year)
		if len(apportions) == 0:
			jdata['info'] = '未分配甲团名额'
			return HttpResponse(json.dumps(jdata))
		else:
			minge = json.loads(apportions[0].minge)
			if not str(department.id) in minge:
				jdata['info'] = '未被分配甲团名额'
				return HttpResponse(json.dumps(jdata))
			minge = int(minge[str(department.id)])
		assignments = JiatuanAssignment.objects.filter(year=year, did=department.id)
		if len(jiatuans) != minge:
			jdata['info'] = '支部数与名额不符'
			return HttpResponse(json.dumps(jdata))
		if len(assignments) > 0:
			jdata['info'] = '已通知'
			assignment = assignments[0]
		else:
			assignment = JiatuanAssignment.objects.create(year=year, did=department.id)
		assignment.branchs = json.dumps(jiatuans)
		assignment.save()
		jdata['info'] = 'yes'
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

	if op == 'submit_jiatuan_to_school':
		year = request.POST.get('year')
		assignments = JiatuanAssignment.objects.filter(year=year, did=department.id)
		if len(assignments) == 0:
			jdata["info"] = "尚未分配名额"
			return HttpResponse(json.dumps(jdata))
		assignment = assignments[0]
		assignment.submitted = True
		assignment.save()
		jdata["info"] = "yes"
		return HttpResponse(json.dumps(jdata))

	if (department is not None) and permission(suser, 'dr', department):
		news_list = News.objects.filter(display_type='d', display_id=did)
		rdata['news_list'] = list(reversed(news_list))[0:min(len(news_list), NEWS_SHOW_NUM)]
		slide_list = Slide.objects.filter(display_type='d', display_id=did, show=True)
		rdata['slide_list'] = list(reversed(slide_list))[0:min(len(slide_list), department.slide_show_num)]
		return render(request, 'department.html', rdata)
	else:
		return render(request, 'permission_denied.html', rdata)

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
		for branch in Branch.objects.filter(did=did).order_by('amt_order'):
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
			arr = line.split(',')
			username = arr[0]
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
		slide_list = Slide.objects.filter(display_type='b', display_id=bid, show=True)
		rdata['slide_list'] = list(reversed(slide_list))[0:min(len(slide_list), branch.slide_show_num)]
		return render(request, 'branch.html', rdata)
	else:
		return render(request, 'permission_denied.html', rdata)

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

def amt_setting(request, amttype, did=-1):
	rdata, op, suser = get_request_basis(request)
	rdata['amttype'] = amttype

	if amttype == 'i':
		if permission(suser, 'iw'):
			departments = Department.objects.order_by('amt_order')
			amt_objects = []
			for department in departments:
				d = {'object': department}
				admins = []
				admin_ids = json.loads(department.admin)
				for admin_id in admin_ids:
					susers = SUser.objects.filter(id=admin_id)
					if len(susers) > 0:
						admins.append(susers[0])
				d['admins'] = admins
				amt_objects.append(d)
			rdata['amt_objects'] = amt_objects

			if op == 'add_department':
				department = Department.objects.create(name=request.POST.get('name', ''))
				department.amt_order = department.id
				department.save()
				return HttpResponse(json.dumps({}))

			if op == 'rename':
				Department.objects.filter(id=int(request.POST.get('dbid'))).update(name=request.POST.get('name'))
				return HttpResponse(json.dumps({}))

			if op == 'updown':
				department = Department.objects.get(id=int(request.POST.get('dbid')))
				departments = list(Department.objects.order_by('amt_order'))
				index = departments.index(department)
				target = index + int(request.POST.get('direction'))
				if target >= 0 and target < len(departments):
					department_target = departments[target]
					temp = department.amt_order
					department.amt_order = department_target.amt_order
					department_target.amt_order = temp
					department.save()
					department_target.save()
				return HttpResponse(json.dumps({}))

			if op == 'remove':
				Department.objects.get(id=int(request.POST.get('dbid'))).delete()
				return HttpResponse(json.dumps({}))

			if op == 'delete_db_admin':
				dsuser = SUser.objects.get(id=int(request.POST.get('sid')))
				department = Department.objects.get(id=int(request.POST.get('dbid')))
				admins = json.loads(department.admin)
				if dsuser.id in admins:
					admins.remove(dsuser.id)
					department.admin = json.dumps(admins)
					department.save()
					message = Message.objects.create(recv_uid=dsuser.id, send_uid=suser.id, mtype=1, send_time=datetime.datetime.now(), title='管理员资格变更', text='你已被取消'+department.name+'院系管理员资格')
					return HttpResponse(json.dumps({'info': '取消成功！'}))
				else:
					return HttpResponse(json.dumps({'info': '取消失败！'}))

			return render(request, 'amt_setting.html', rdata)
		else:
			return render(request, 'permission_denied.html', rdata)

	if amttype == 'd':
		department = Department.objects.get(id=int(did))
		if permission(suser, 'dw', department):
			branchs = Branch.objects.filter(did=int(did)).order_by('amt_order')
			amt_objects = []
			for branch in branchs:
				d = {'object': branch}
				admins = []
				admin_ids = json.loads(branch.admin)
				for admin_id in admin_ids:
					susers = SUser.objects.filter(id=admin_id)
					if len(susers) > 0:
						admins.append(susers[0])
				d['admins'] = admins
				amt_objects.append(d)
			rdata['amt_objects'] = amt_objects

			if op == 'add_branch':
				branch = Branch.objects.create(name=request.POST.get('name', ''), did=did)
				branch.amt_order = branch.id
				branch.save()
				return HttpResponse(json.dumps({}))
		
			if op == 'rename':
				Branch.objects.filter(id=int(request.POST.get('dbid'))).update(name=request.POST.get('name'))
				return HttpResponse(json.dumps({}))

			if op == 'updown':
				branch = Branch.objects.get(id=int(request.POST.get('dbid')))
				branchs = list(Branch.objects.order_by('amt_order'))
				index = branchs.index(branch)
				target = index + int(request.POST.get('direction'))
				if target >= 0 and target < len(branchs):
					branch_target = branchs[target]
					temp = branch.amt_order
					branch.amt_order = branch_target.amt_order
					branch_target.amt_order = temp
					branch.save()
					branch_target.save()
				return HttpResponse(json.dumps({}))

			if op == 'remove':
				Branch.objects.get(id=int(request.POST.get('dbid'))).delete()
				return HttpResponse(json.dumps({}))

			if op == 'delete_db_admin':
				dsuser = SUser.objects.get(id=int(request.POST.get('sid')))
				branch = Branch.objects.get(id=int(request.POST.get('dbid')))
				admins = json.loads(branch.admin)
				if dsuser.id in admins:
					admins.remove(dsuser.id)
					branch.admin = json.dumps(admins)
					branch.save()
					message = Message.objects.create(recv_uid=dsuser.id, send_uid=suser.id, mtype=1, send_time=datetime.datetime.now(), title='管理员资格变更', text='你已被取消'+branch.name+'支部管理员资格')
					return HttpResponse(json.dumps({'info': '取消成功！'}))
				else:
					return HttpResponse(json.dumps({'info': '取消失败！'}))

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

			return render(request, 'amt_setting.html', rdata)
		else:
			return render(request, 'permission_denied.html', rdata)

	return render(request, 'permission_denied.html', rdata)

def global_setting(request):
	rdata, op, suser = get_request_basis(request)
	if suser is None:
		return render(request, 'permission_denied.html', rdata)

	if suser.admin_super:
		if op == 'delete_admin_school':
			sid = int(request.POST.get('sid'))
			susers = SUser.objects.filter(id=sid)
			print(sid, susers[0].username)
			if len(susers) > 0 and susers[0].username != 'root':
				susers[0].admin_school = False
				susers[0].save()
				message = Message.objects.create(recv_uid=susers[0].id, send_uid=suser.id, mtype=1, send_time=datetime.datetime.now(), title='管理员资格变更', text='你已被取消校级管理员资格')
				return HttpResponse(json.dumps({'info': '取消成功！'}))
			else:
				return HttpResponse(json.dumps({'info': '取消失败！'}))

	if suser.admin_school:
		if op == 'add_year':
			years = json.loads(School.objects.all()[0].years)
			years.insert(0, int(request.POST.get('new_year')))
			print(years)
			School.objects.all().update(years=json.dumps(years))
			return HttpResponse(json.dumps({}))

		if op == 'delete_year':
			years = json.loads(School.objects.all()[0].years)
			year = int(request.POST.get('year'))
			if year in years:
				years.remove(year)
				School.objects.update(years=json.dumps(years))
				return HttpResponse(json.dumps({'info': '删除成功'}))
			else:
				return HttpResponse(json.dumps({'info': '出错？'}))

		rdata['admins'] = SUser.objects.filter(admin_school=True)
		for d0 in rdata['departments']:
			department = d0['department']
			admins = []
			admin_ids = json.loads(department.admin)
			for admin_id in admin_ids:
				susers = SUser.objects.filter(id=admin_id)
				if len(susers) > 0:
					admins.append(susers[0])
			d0['admins'] = admins
			for d1 in d0['branchs']:
				branch = d1['branch']
				admins = []
				admin_ids = json.loads(branch.admin)
				for admin_id in admin_ids:
					susers = SUser.objects.filter(id=admin_id)
					if len(susers) > 0:
						admins.append(susers[0])
				d1['admins'] = admins
				d1['member_num'] = len(json.loads(branch.member))

		return render(request, 'global_setting.html', rdata)
	else:
		return render(request, 'permission_denied.html', rdata)
