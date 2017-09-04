# -*- coding: utf-8 -*-
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from SUser.models import SUser, School, Department, Branch
from SUser.utils import get_request_basis
from Message.models import Message, Handbook, News, JiatuanMaterial
import datetime
import json
import time

# m_type
#   0: 预留
#   1: 用户发送
def message(request, mid=-1):
	rdata, op, suser = get_request_basis(request)
	jdata = {}

	if op == 'send_message':
		recvers = json.loads(request.POST.get('recver', '[]'))
		# 检查收件人
		check_recvers = 'yes'
		recv_uids = []
		for recver in recvers:
			if recver == '': continue
			susers = SUser.objects.filter(username=recver)
			if len(susers) == 0:
				check_recvers = '用户"' + recver + '"不存在'
				break
			recv_uids.append(susers[0].id)
		jdata['result'] = check_recvers
		if check_recvers != 'yes':
			return HttpResponse(json.dumps(jdata))
		# 逐条发送
		for recv_uid in recv_uids:
			message = Message.objects.create(recv_uid=recv_uid, send_uid=suser.id, mtype=1, send_time=datetime.datetime.now(), title=request.POST.get('title'), text=request.POST.get('text'), attachment=request.POST.get('attachment'))
		return HttpResponse(json.dumps(jdata))

	if op == 'get_message':
		messages = Message.objects.filter(id=request.POST.get('mid'))
		if len(messages) > 0:
			message = messages[0]
			jdata['send_username'] = SUser.objects.get(id=message.send_uid).username
			jdata['mtype'] = message.mtype
			jdata['send_time'] = message.send_time.strftime("%Y-%m-%d %H:%M:%S")
			jdata['title'] = message.title
			if jdata['title'] == '': jdata['title'] = '（无标题）'
			jdata['text'] = message.text
			jdata['attachment'] = message.attachment
		return HttpResponse(json.dumps(jdata))

	if op == 'close_message':
		messages = Message.objects.filter(id=request.POST.get('mid'))
		if len(messages) > 0:
			message = messages[0]
			mtype = message.mtype
			# 申请
			if mtype in [2, 3, 4, 5]:
				yes = int(request.POST.get('yes'))
				if yes == 0:
					text = '您的申请未通过'
				else:
					sender = SUser.objects.get(id=message.send_uid)
					meta = json.loads(message.meta)
					if mtype == 2:
						sender.admin_school = True
						sender.save()
						text = '您的 校级管理员 申请已通过'
					elif mtype == 3:
						department = Department.objects.get(id=meta['did'])
						admin = json.loads(department.admin)
						admin.append(sender.id)
						department.admin = json.dumps(admin)
						department.save()
						text = '您的 ' + department.name + '管理员 申请已通过'
					elif mtype == 4:
						branch = Branch.objects.get(id=meta['bid'])
						admin = json.loads(branch.admin)
						admin.append(sender.id)
						branch.admin = json.dumps(admin)
						branch.save()
						text = '您的 ' + branch.name + '管理员 申请已通过'
					elif mtype == 5:
						branch = Branch.objects.get(id=meta['bid'])
						member = json.loads(branch.member)
						member.append(sender.id)
						branch.member = member
						branch.save()
						text = '您的 ' + branch.name + '成员 申请已通过'
				# 回复结果
				reply = Message.objects.create(recv_uid=message.send_uid, send_uid=message.recv_uid, mtype=1, send_time=datetime.datetime.now(), title='权限申请结果', text=text)
				# 消除同组其他邮件
				for peer_message in Message.objects.filter(group=message.group):
					peer_message.read = True
					peer_message.save()
			message.read = True
			message.save()
		return HttpResponse(json.dumps(jdata))

	if op == 'get_default_recver':
		recver_list = []
		departments = Department.objects.all()
		is_department_admin = False
		for department in departments:
			if suser.admin_school:
				recver_list.append({'type': 'd', 'id': department.id, 'name': department.name + '管理员'})
			if suser.id in json.loads(department.admin):
				is_department_admin = True
				admin_did = department.id
				recver_list.append({'type': 's', 'id': -1, 'name': '校级管理员'})
				break
		branchs = Branch.objects.all()
		for branch in branchs:
			if is_department_admin and admin_did == branch.did:
				recver_list.append({'type': 'b', 'id': branch.id, 'name': branch.name + '管理员'})
			if suser.id in json.loads(branch.admin):
				department = Department.objects.get(id=branch.did)
				recver_list.append({'type': 'd', 'id': department.id, 'name': department.name + '管理员'})
		jdata['recver_list'] = recver_list
		return HttpResponse(json.dumps(jdata))

	if op == 'get_default_recver_sub':
		recvers = []
		rtype = request.POST.get('rtype')
		rid = request.POST.get('rid')
		if rtype == 's':
			recvers = [rsuser.username for rsuser in SUser.objects.filter(admin_school=True)]
		elif rtype == 'd':
			department = Department.objects.get(id=rid)
			recvers = [SUser.objects.get(id=rsuser_id).username for rsuser_id in json.loads(department.admin)]
		elif rtype == 'b':
			branch = Branch.objects.get(id=rid)
			recvers = [SUser.objects.get(id=rsuser_id).username for rsuser_id in json.loads(branch.admin)]
		jdata['recvers'] = recvers
		print('sub', rtype, rid)
		print(recvers)
		return HttpResponse(json.dumps(jdata))

	if suser is None:
		return HttpResponseRedirect('/index/')

	# 显示收件箱
	if mid == -1:
		rdata['read_all'] = True
		messages = Message.objects.filter(recv_uid=suser.id)
		re_messages = []
		for message in messages:
			d = {}
			d['id'] = message.id
			d['read'] = message.read
			d['title'] = message.title
			if d['title'] == '': d['title'] = '（无标题）'
			d['send_username'] = SUser.objects.get(id=message.send_uid).username
			d['send_time'] = message.send_time.strftime("%Y-%m-%d %H:%M:%S")
			re_messages.append(d)
		rdata['messages'] = re_messages
	else:
		rdata['read_all'] = False
		message = Message.objects.get(id=mid)
		rdata['message'] = message
		rdata['send_username'] = SUser.objects.get(id=message.send_uid).username

	return render(request, 'message.html', rdata)

def handbook_edit(request, htype, idd):
	rdata, op, suser = get_request_basis(request)
	jdata = {}

	if op == 'get_handbook_list':
		year = int(request.POST.get('year'))
		if htype == 'd':
			handbooks = Handbook.objects.filter(year=year, htype=htype, review_id=0, submitted=True)
			l = []
			for handbook in handbooks:
				department = Department.objects.get(id=handbook.submit_id)
				l.append({'hid': handbook.id, 'title': department.name})
		if htype == 'b':
			handbooks = Handbook.objects.filter(year=year, htype=htype, review_id=request.POST.get('did'), submitted=True)
			l = []
			for handbook in handbooks:
				branch = Branch.objects.get(id=handbook.submit_id)
				l.append({'hid': handbook.id, 'title': branch.name})
		jdata['handbooks'] = l
		return HttpResponse(json.dumps(jdata))

	if htype == 'd':
		department = Department.objects.get(id=idd)
		branch = None
		admin_department = json.loads(department.admin)
		admin_branch = []
	elif htype == 'b':
		branch = Branch.objects.get(id=idd)
		department = Department.objects.get(id=branch.did)
		admin_department = []
		admin_branch = json.loads(branch.admin)

	if op == 'load_handbook':
		year = int(request.POST.get('year'))
		if htype == 'd':
			handbooks = Handbook.objects.filter(htype=htype, year=year, submit_id=department.id)
		elif htype == 'b':
			handbooks = Handbook.objects.filter(htype=htype, year=year, submit_id=branch.id)
		jdata['content'] = None
		jdata['submitted'] = False
		if len(handbooks) > 0:
			jdata['content'] = handbooks[0].content
			jdata['submitted'] = handbooks[0].submitted
		return HttpResponse(json.dumps(jdata))

	if op == 'submit':
		content = request.POST.get('content')
		subtype = int(request.POST.get('subtype'))
		# year = datetime.datetime.now().year
		year = int(request.POST.get('year'))
		if htype == 'd':
			handbooks = Handbook.objects.filter(htype=htype, year=year, submit_id=department.id)
			if len(handbooks) == 0:
				handbook = Handbook.objects.create(htype=htype, year=year, review_id=0, submit_id=department.id)
			else:
				handbook = handbooks[0]
			handbook.content = content
			handbook.submitted = subtype
			handbook.save()
		elif htype == 'b':
			handbooks = Handbook.objects.filter(htype=htype, year=year, submit_id=branch.id)
			if len(handbooks) == 0:
				handbook = Handbook.objects.create(htype=htype, year=year, review_id=department.id, submit_id=branch.id)
			else:
				handbook = handbooks[0]
			handbook.content = content
			handbook.submitted = subtype
			handbook.save()
		return HttpResponse(json.dumps(jdata))

	if htype == 'd':
		rdata['title'] = '院系工作手册'
	elif htype == 'b':
		rdata['title'] = '团支部工作手册'
	rdata['readonly'] = False

	# 权限检测
	if (suser is not None) and (suser.admin_super or (suser.id in admin_department) or (suser.id in admin_branch)):
		return render(request,'handbook.html', rdata)

def handbook_show(request, hid):
	rdata, op, suser = get_request_basis(request)
	jdata = {}

	handbook = Handbook.objects.get(id=hid)
	rdata['handbook'] = handbook
	if handbook.htype == 'd':
		hflag = True
		department = Department.objects.get(id=handbook.submit_id)
		rdata['title'] = department.name + " 院系工作手册"
	elif handbook.htype == 'b':
		hflag = False
		department = Department.objects.get(id=handbook.review_id)
		admin_department = json.loads(department.admin)
		branch = Branch.objects.get(id=handbook.submit_id)
		rdata['title'] = branch.name + " 团支部工作手册"

	if op == 'load_handbook':
		jdata['content'] = handbook.content
		return HttpResponse(json.dumps(jdata))

	rdata['readonly'] = True

	# 权限检测
	if (suser is not None) and (suser.admin_super or (hflag and suser.admin_school) or (not hflag and suser.id in admin_department)):
		return render(request,'handbook.html', rdata)

def jiatuan_edit(request, bid):
	rdata, op, suser = get_request_basis(request)
	jdata = {}

	branch = Branch.objects.get(id=bid)

	if op == 'load_jiatuan':
		year = int(request.POST.get('year'))
		jiatuans = JiatuanMaterial.objects.filter(year=year, submit_id=branch.id)
		jdata['content'] = None
		jdata['submitted'] = False
		if len(jiatuans) > 0:
			jdata['content'] = jiatuans[0].content
			jdata['submitted'] = jiatuans[0].submitted
		return HttpResponse(json.dumps(jdata))

	if op == 'submit':
		content = request.POST.get('content')
		subtype = int(request.POST.get('subtype'))
		year = int(request.POST.get('year'))
		jiatuans = JiatuanMaterial.objects.filter(year=year, submit_id=branch.id)
		if len(jiatuans) == 0:
			jiatuan = JiatuanMaterial.objects.create(year=year, submit_id=branch.id)
		else:
			jiatuan = jiatuans[0]
		jiatuan.content = content
		jiatuan.submitted = subtype
		jiatuan.save()
		return HttpResponse(json.dumps(jdata))

	rdata['title'] = '甲团材料'
	rdata['readonly'] = False

	# 权限检测
	if (suser is not None) and (suser.admin_super or (suser.id in json.loads(branch.admin))):
		return render(request,'jiatuan.html', rdata)

def jiatuan_show(request, jid):
	rdata, op, suser = get_request_basis(request)
	jdata = {}

	jiatuan = JiatuanMaterial.objects.get(id=jid)
	branch = Branch.objects.get(id=jiatuan.submit_id)
	department = Department.objects.get(id=branch.did)
	rdata['jiatuan'] = jiatuan

	if op == 'load_jiatuan':
		jdata['content'] = jiatuan.content
		return HttpResponse(json.dumps(jdata))

	rdata['readonly'] = True

	# 权限检测
	if (suser is not None) and (suser.admin_school or (suser.id in json.loads(department.admin)) or (suser.id in json.loads(branch.admin))):
		return render(request, 'jiatuan.html', rdata)

def news(request, nid=-1):
	rdata, op, suser = get_request_basis(request)
	jdata = {}

	if op == 'add_news':
		title = request.POST.get('title')
		text = request.POST.get('text')
		display_type = request.POST.get('display_type')
		display_id = request.POST.get('display_id')
		year = year = datetime.datetime.now().year
		news = News.objects.create(display_type=display_type, display_id=display_id, year=year, title=title, text=text)
		return HttpResponse(json.dumps(jdata))

	def slide_add(slide, title, text, img_path):
		slide = json.loads(slide)
		slide.append({'title': title, 'text': text, 'img_path': img_path})
		if len(slide) > 3:
			slide = slide[1:]
		return json.dumps(slide)

	if op == 'add_slide':
		title = request.POST.get('title')
		text = request.POST.get('text')
		img_path = request.POST.get('img_path')
		display_type = request.POST.get('display_type')
		display_id = int(request.POST.get('display_id'))
		print(display_type, display_id)
		if display_type == 'i':
			school = School.objects.all()[0]
			school.slide = slide_add(school.slide, title, text, img_path)
			school.save()
		elif display_type == 'd':
			department = Department.objects.get(id=display_id)
			department.slide = slide_add(department.slide, title, text, img_path)
			department.save()
		elif display_type == 'b':
			branch = Branch.objects.get(id=display_id)
			branch.slide = slide_add(branch.slide, title, text, img_path)
			branch.save()
		return HttpResponse(json.dumps(jdata))

	news = News.objects.get(id=nid)
	rdata['news'] = news
	return render(request, 'news.html', rdata)

@csrf_exempt 
def uploadFile(request):
	if request.method == 'POST':
		buf = request.FILES.get('imgFile', None)
		file_name = buf.name
		file_buff = buf.read()
		time_stamp = time.strftime('%Y%m%d%H%M%S')
		real_file_name = str(time_stamp)+"-"+file_name
		save_file("media", real_file_name, file_buff)
		dict_tmp = {}
		dict_tmp["error"] = 0
		dict_tmp["url"] = "/media/"+file_name
		dict_tmp["real_url"] = "/media/"+ real_file_name
		return HttpResponse(json.dumps(dict_tmp))

def save_file(path, file_name, data):
    if data == None:
        return
    if(not path.endswith("/")):
        path=path+"/"
    file=open(path+file_name, "wb")
    file.write(data)
    file.flush()
    file.close()