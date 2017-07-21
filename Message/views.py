# -*- coding: utf-8 -*-
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from SUser.models import SUser, Department, Branch
from SUser.utils import get_request_basis
from Message.models import Message, Handbook
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
			handbooks = Handbook.objects.filter(year=year, htype=htype, review_id=0)
			l = []
			for handbook in handbooks:
				department = Department.objects.get(id=handbook.submit_id)
				l.append({'hid': handbook.id, 'title': department.name})
		if htype == 'b':
			handbooks = Handbook.objects.filter(year=year, htype=htype, review_id=request.POST.get('did'))
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

	if op == 'submit':
		content = request.POST.get('content')
		year = datetime.datetime.now().year
		if htype == 'd':
			Handbook.objects.create(htype=htype, year=year, review_id=0, submit_id=department.id, content=content)
		elif htype == 'b':
			Handbook.objects.create(htype=htype, year=year, review_id=department.id, submit_id=branch.id, content=content)
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
	elif handbook.htype == 'b':
		hflag = False
		department = Department.objects.get(id=handbook.review_id)
		admin_department = json.loads(department.admin)

	if op == 'load_handbook':
		jdata['content'] = handbook.content
		return HttpResponse(json.dumps(jdata))

	rdata['readonly'] = True

	# 权限检测
	if (suser is not None) and (suser.admin_super or (hflag and suser.admin_school) or (not hflag and suser.id in admin_department)):
		return render(request,'handbook.html', rdata)

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