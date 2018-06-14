# -*- coding: utf-8 -*-
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from SUser.models import *
from SUser.utils import get_request_basis, permission
from Message.models import  *
import codecs
import datetime
import json
import os
import re
import time

from reportlab import platypus
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle

import reportlab.pdfbase.ttfonts
reportlab.pdfbase.pdfmetrics.registerFont(reportlab.pdfbase.ttfonts.TTFont('heilight', 'static/font/STHeiti Light.ttc'))
reportlab.pdfbase.pdfmetrics.registerFont(reportlab.pdfbase.ttfonts.TTFont('heimedium', 'static/font/STHeiti Medium.ttc'))



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
		return HttpResponse(json.dumps(jdata))

	if suser is None:
		return render(request, 'permission_denied.html', rdata)

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
				departments = Department.objects.filter(id=handbook.submit_id)
				if len(departments) > 0:
					l.append({'hid': handbook.id, 'title': departments[0].name})
		if htype == 'b':
			handbooks = Handbook.objects.filter(year=year, htype=htype, review_id=request.POST.get('did'), submitted=True)
			l = []
			for handbook in handbooks:
				branchs = Branch.objects.filter(id=handbook.submit_id)
				if len(branchs) > 0:
					l.append({'hid': handbook.id, 'title': branchs[0].name})
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
		jdata['htype'] = htype
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

	'''if op == 'export':
		year = int(request.POST.get('year'))
		if htype == 'd':
			handbooks = Handbook.objects.filter(htype=htype, year=year, submit_id=department.id)
			aff = department
		elif htype == 'b':
			handbooks = Handbook.objects.filter(htype=htype, year=year, submit_id=branch.id)
			aff = branch
		if len(handbooks) > 0:
			jdata['result'] = 'OK'
			jdata['export_path'] = export_handbook(handbooks[0], aff)
		else:
			jdata['result'] = '尚未提交或暂存'
		return HttpResponse(json.dumps(jdata))'''

	if htype == 'd':
		rdata['title'] = '院系工作手册'
	elif htype == 'b':
		rdata['title'] = '团支部工作手册'
	rdata['readonly'] = False

	# 权限检测
	if (suser is not None) and (suser.admin_super or (suser.id in admin_department) or (suser.id in admin_branch)):
		return render(request,'handbook.html', rdata)
	else:
		return render(request, 'permission_denied.html', rdata)

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
		jdata['htype'] = handbook.htype
		return HttpResponse(json.dumps(jdata))

	if op == 'export':
		jdata['result'] = 'OK'
		if handbook.htype == 'd':
			jdata['export_path'] = export_handbook(handbook, department)
		elif handbook.htype == 'b':
			jdata['export_path'] = export_handbook(handbook, branch)
		else:
			jdata['result'] = '错误'
		return HttpResponse(json.dumps(jdata))

	if op == 'export_item':
		title = request.POST.get('title')
		etype = int(request.POST.get('etype'))
		content = json.loads(handbook.content)
		jdata['result'] = 'OK'
		if handbook.htype == 'd':
			if etype == 100:
				jdata['export_path'] = export_txt(title+'-等级评估方案', content[6][0][0][0])
			elif etype == 101:
				jdata['export_path'] = export_txt(title+'-实施细则', content[7][0][0][0])
			elif etype == 102:
				jdata['export_path'] = export_txt(title+'-等级评估工作领导小组组成', content[8][0][0][0])
			elif etype == 103:
				jdata['export_path'] = export_txt(title+'-初评甲级团支部名单', content[9][0][0][0])
			else:
				jdata['result'] = '错误 d'
		elif handbook.htype == 'b':
			if etype == 0:
				jdata['export_path'] = export_handbook_fundamental_info(title, content[0][0])
			elif etype == 1:
				jdata['export_path'] = export_csv(title+'-奖惩情况', '奖惩对象,时间,内容', content[0][1])
			elif etype == 2:
				jdata['export_path'] = export_csv(title+'-团员花名册', '学号,姓名,性别,民族,政治面貌,籍贯,出生日期,入团时间,备注', content[0][2])
			elif etype == 3:
				jdata['export_path'] = export_csv(title+'-申请入团名单', '学号,姓名,性别,民族,籍贯,出生日期,申请入团时间,备注', content[0][3])
			elif etype == 4:
				jdata['export_path'] = export_csv(title+'-交纳团费情况', '月份,支部人数,应交人数,实交人数,应交金额,实交金额,备注', content[0][4])
			elif etype == 5:
				jdata['export_path'] = export_csv(title+'-推优入党名单', '学号,姓名,提交申请书时间,入党时间,转正时间', content[0][5])
			elif etype == 10:
				jdata['export_path'] = export_txt(title+'-全年计划', content[1][0][0][0])
			elif etype == 11:
				jdata['export_path'] = export_txt(title+'-春季学期计划', content[1][1][0][0])
			elif etype == 12:
				jdata['export_path'] = export_txt(title+'-秋季学期计划', content[1][2][0][0])
			elif etype == 20:
				jdata['export_path'] = export_txt(title+'-支部事业简介', content[2][0][0][0])
			elif etype == 21:
				jdata['export_path'] = export_txt(title+'-支部事业目标', content[2][1][0][0])
			elif etype == 22:
				jdata['export_path'] = export_txt(title+'-预期成果', content[2][2][0][0])
			elif etype == 30:
				jdata['export_path'] = export_handbook_theme_activity(title+'-主题团日', '活动主题,活动时间,地点,参与人数,主持人,记录人,活动内容,活动总结', content[3][0])
			elif etype == 31:
				jdata['export_path'] = export_handbook_theme_activity(title+'-组织生活', '活动类型,活动主题,活动时间,地点,参与人数,主持人,记录人,活动内容,活动总结', content[3][1])
			elif etype == 40:
				jdata['export_path'] = export_handbook_theme_activity(title+'-支部活动', '活动类型,活动主题,活动时间,地点,参与人数,主持人,记录人,活动内容,活动总结', content[4][0])
			elif etype == 50:
				jdata['export_path'] = export_txt(title+'-秋季学期工作总结', content[5][0][0][0])
			elif etype == 51:
				jdata['export_path'] = export_txt(title+'-春季学期工作总结', content[5][1][0][0])
			else:
				jdata['result'] = '错误 b'
		else:
			jdata['result'] = '错误 0'
		return HttpResponse(json.dumps(jdata))

	rdata['readonly'] = True
	if handbook.htype == 'd':
		rdata['htype'] = 0
	else:
		rdata['htype'] = 1

	# 权限检测
	if (suser is not None) and (suser.admin_super or (hflag and suser.admin_school) or (not hflag and suser.id in admin_department)):
		return render(request,'handbook.html', rdata)

def jiatuan_edit(request, bid):
	rdata, op, suser = get_request_basis(request)
	jdata = {}

	branch = Branch.objects.get(id=bid)

	if op == 'load_jiatuan':
		year = int(request.POST.get('year'))
		department = Department.objects.get(id=branch.did)
		assignments = JiatuanAssignment.objects.filter(year=year, did=department.id)
		if len(assignments) == 0:
			jdata['info'] = '院系尚未制定甲团'
			return HttpResponse(json.dumps(jdata))
		branchs = json.loads(assignments[0].branchs)
		if not str(branch.id) in branchs:
			jdata['info'] = '支部不是甲级团支部'
			return HttpResponse(json.dumps(jdata))
		jdata['info'] = 'yes'
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
		jdata['year'] = jiatuan.year
		return HttpResponse(json.dumps(jdata))

	if op == 'export':
		etype = int(request.POST.get('etype'))
		content = json.loads(jiatuan.content)
		title = request.POST.get('title')
		jdata['result'] = 'OK'
		if etype == 0:
			jdata["export_path"] = export_jiatuan_fundamental_info(title, content[0])
		elif etype == 1:
			jdata["export_path"] = export_txt(title + '-基本情况', content[0][2][0][0])
		elif etype == 2:
			jdata["export_path"] = export_txt(title + '-基本要求', content[0][3][0][0])
		elif etype == 3:
			jdata["export_path"] = export_txt(title + '-支部事业与文化', content[0][4][0][0])
		elif etype == 4:
			jdata["export_path"] = export_txt(title + '-支部工作案例', content[1][0])
		else:
			jdata['result'] = '错误'
		return HttpResponse(json.dumps(jdata))

	rdata['title'] = branch.name + ' 甲团材料'
	rdata['readonly'] = True

	# 权限检测
	if (suser is not None) and (suser.admin_school or (suser.id in json.loads(department.admin)) or (suser.id in json.loads(branch.admin))):
		return render(request, 'jiatuan.html', rdata)

def news(request, nid=-1):
	rdata, op, suser = get_request_basis(request)
	jdata = {}

	news = News.objects.get(id=nid)
	readable = False
	if news.display_type == 'i':
		readable = permission(suser, 'ir')
	elif news.display_type == 'd':
		readable = permission(suser, 'dr')
	elif news.display_type == 'b':
		readable = permission(suser, 'br')
	else:
		print('新闻访问错误')
	rdata['news'] = news

	if readable:
		return render(request, 'news.html', rdata)
	else:
		return render(request, 'permission_denied.html', rdata)

def news_list(request, dtype, idd=-1):
	rdata, op, suser = get_request_basis(request)
	jdata = {}

	readable = False
	if dtype == 'i':
		news_list = News.objects.filter(display_type='i')
		rdata['title'] = '学校新闻'
		readable = permission(suser, 'ir')
		rdata['is_admin'] = permission(suser, 'iw')
	elif dtype == 'd':
		news_list = News.objects.filter(display_type=dtype, display_id=idd)
		department = Department.objects.filter(id=idd)[0]
		rdata['title'] = department.name + '新闻'
		readable = permission(suser, 'dr', department)
		rdata['is_admin'] = permission(suser, 'dw', department)
	elif dtype == 'b':
		news_list = News.objects.filter(display_type=dtype, display_id=idd)
		branch = Branch.objects.get(id=idd)
		department = Department.objects.get(id=branch.did)
		rdata['title'] = branch.name + '新闻'
		readable = permission(suser, 'br', [rdata['self_department'], department])
		rdata['is_admin'] = permission(suser, 'bw', branch)
	else:
		print('新闻列表访问错误')
	rdata['news_list'] = news_list = list(reversed(news_list))

	if op == 'add_news':
		title = request.POST.get('title')
		text = request.POST.get('text')
		display_type = request.POST.get('display_type')
		display_id = request.POST.get('display_id')
		year = year = datetime.datetime.now().year
		news = News.objects.create(display_type=display_type, display_id=display_id, post_time=datetime.datetime.now(), title=title, text=text)
		return HttpResponse(json.dumps(jdata))

	if op == 'delete_news':
		News.objects.filter(id=int(request.POST.get('nid'))).delete()
		return HttpResponse(json.dumps(jdata))

	if readable:
		return render(request, 'news_list.html', rdata)
	else:
		return render(request, 'permission_denied.html', rdata)

def slide_list(request, dtype, idd=-1):
	rdata, op, suser = get_request_basis(request)
	jdata = {}

	if dtype == 'i':
		slide_list = Slide.objects.filter(display_type='i')
		rdata['title'] = '学校图文'
		rdata['is_admin'] = permission(suser, 'iw')
		rdata['slide_show_num'] = School.objects.all()[0].slide_show_num
	elif dtype == 'd':
		slide_list = Slide.objects.filter(display_type=dtype, display_id=idd)
		department = Department.objects.filter(id=idd)[0]
		rdata['title'] = department.name + '图文'
		rdata['is_admin'] = permission(suser, 'dw', department)
		rdata['slide_show_num'] = department.slide_show_num
	elif dtype == 'b':
		slide_list = Slide.objects.filter(display_type=dtype, display_id=idd)
		branch = Branch.objects.get(id=idd)
		department = Department.objects.get(id=branch.did)
		rdata['title'] = branch.name + '图文'
		rdata['is_admin'] = permission(suser, 'bw', branch)
		rdata['slide_show_num'] = branch.slide_show_num
	else:
		print('图文列表访问错误')

	if op == 'add_slide':
		Slide.objects.create(display_type=dtype, display_id=int(idd), title=request.POST.get('title'), text=request.POST.get('text'), img_path=request.POST.get('img_path'), post_time=datetime.datetime.now())
		return HttpResponse(json.dumps(jdata))

	if op == 'delete_slide':
		slide = Slide.objects.get(id=int(request.POST.get('sid')))
		if os.path.exists(slide.img_path[1:]):
			os.remove(slide.img_path[1:])
		slide.delete()
		return HttpResponse(json.dumps(jdata))

	if op == 'show':
		Slide.objects.filter(id=int(request.POST.get('sid'))).update(show=int(request.POST.get('show')))
		return HttpResponse(json.dumps(jdata))

	if op == 'change_slide_show_num':
		num = int(request.POST.get('num'))
		if dtype == 'i':
			School.objects.all().update(slide_show_num=num)
		elif dtype == 'd':
			department.slide_show_num = num
			department.save()
		elif dtype == 'b':
			branch.slide_show_num = num
			branch.save()
		return HttpResponse(json.dumps(jdata))

	rdata['slide_list'] = reversed(slide_list)

	if rdata['is_admin']:
		return render(request, 'slide_list.html', rdata)
	else:
		return render(request, 'permission_denied.html', rdata)

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

def filterhtml(txt):
	txt = re.compile(r'<[^>]+>', re.S).sub('', txt)
	txt = re.compile(r'\t', re.S).sub('', txt)
	txt = re.compile(r'&nbsp;', re.S).sub(' ', txt)
	return txt


def export_handbook(handbook, aff):
	styleSheet = getSampleStyleSheet()
	normalStyle = styleSheet['Normal']
	tableStyle = TableStyle([
		('FONTNAME',(0,0),(-1,-1),'heilight'),
		('FONTSIZE',(0,0),(-1,-1),8),
		('ALIGN',(0,0),(-1,-1),'CENTER'),
		('VALIGN',(0,0),(-1,-1),'MIDDLE'),
		('GRID',(0,0),(-1,-1),0.5,colors.black)
		])

	def makeTitle(s, fontSize=10, face="heilight"):
		return Paragraph('<para fontSize=' + str(fontSize) + ' align=center><br/><br/><font face="' + face + '">' + s + '</font><br/><br/></para>', normalStyle)

	def makeTable(t, colw, tStyle=tableStyle, largeText=False):
		for i in range(len(t)):
			for j in range(len(t[i])):
				if len(t[i][j]) > colw[j] / 8 or largeText:
					t[i][j] = Paragraph('<font face="heilight" fontSize=8>' + t[i][j] + '</font>', normalStyle)
		return Table(t, colWidths=colw, style=tStyle)

	def crossPage(txt, SPAN):
		txt = re.compile(r'<[^>]+>', re.S).sub('', txt)
		txt = re.compile(r'\t', re.S).sub('', txt)
		l = len(txt)
		arr = []
		i = 0
		while i < l:
			if i == 0:
				span = SPAN
			else:
				span = 3400
			arr.append( re.compile(r'<[^>]+>', re.S).sub('<br/>', txt[i:i+min(span, l-i)]) )
			i += span
		return arr

	def makeCrossPage(txt, SPAN=3100):
		arr = crossPage(txt, SPAN)
		return makeTable([[x] for x in arr], [500], largeText=True)

	h = json.loads(handbook.content)
	pdf = []
	if handbook.htype == 'd':
		pdfname = str(handbook.year-1) + '-' + str(handbook.year) + '学年' + aff.name + '院系工作手册'
		pdf.append(Paragraph('<para fontSize=20 align=center><font face="heimedium">' + pdfname + '</font><br/><br/></para>', normalStyle))
		pdf.append(makeTitle('等级评估方案', 15, 'heimedium'))
		pdf.append(makeCrossPage(h[8][0][0][0]))
		pdf.append(platypus.flowables.PageBreak())
		pdf.append(makeTitle('实施细则', 15, 'heimedium'))
		pdf.append(makeCrossPage(h[9][0][0][0]))
		pdf.append(platypus.flowables.PageBreak())
		pdf.append(makeTitle('等级评估工作领导小组组成', 15, 'heimedium'))
		pdf.append(makeCrossPage(h[10][0][0][0]))
		pdf.append(platypus.flowables.PageBreak())
		pdf.append(makeTitle('初级甲级团支部名单', 15, 'heimedium'))
		pdf.append(makeCrossPage(h[11][0][0][0]))
		pdf.append(platypus.flowables.PageBreak())
	elif handbook.htype == 'b':
		# 大标题
		pdfname = str(handbook.year) + '-' + str(handbook.year+1) + '学年' + aff.name + '团支部工作手册'
		pdf.append(Paragraph('<para fontSize=20 align=center><font face="heimedium">' + pdfname + '</font><br/><br/></para>', normalStyle))
		# 基本情况
		pdf.append(makeTitle('基本情况', 15, 'heimedium'))
		# 	基本信息
		pdf.append(makeTitle('基本信息'))
		table = [['团员人数', '团支部书记', '组织委员', '宣传委员', '备注'], h[0][0][0]]
		pdf.append(makeTable(table, [100, 100, 100, 100, 100]))
		if len(h[0][0]) > 1:
			pdf.append(makeTitle('其他委员'))
			table = [['委员职能', '委员姓名', '备注']]
			table.extend(h[0][0][1:])
			pdf.append(makeTable(table, [150, 150, 200]))
		# 	奖惩情况
		pdf.append(makeTitle('奖惩情况'))
		table = [['', '时间', '内容']]
		# ['团支部'], ['班级'], ['党课学习小组'], ['个人']
		h01 = h[0][1]
		i = 0
		n = len(h01)
		tbstyle = [
			('FONTNAME',(0,0),(-1,-1),'heilight'),
			('FONTSIZE',(0,0),(-1,-1),8),
			('ALIGN',(0,0),(-1,-1),'CENTER'),
			('VALIGN',(0,0),(-1,-1),'MIDDLE'),
			('GRID',(0,0),(-1,-1),0.5,colors.black)
			]
		while i < n:
			j = i + 1
			while j < n and h01[i][0] == h01[j][0]: j += 1
			table.extend(h01[i:j])
			tbstyle.append(('SPAN',(0,i+1),(0,j)))
			i = j
		pdf.append(makeTable(table, [100, 100, 300], TableStyle(tbstyle)))
		# 	团员花名册
		pdf.append(makeTitle('团员花名册'))
		table = [['学号', '姓名', '性别', '民族', '政治面貌', '籍贯', '出生日期', '入团时间', '备注']]
		table.extend(h[0][2])
		pdf.append(makeTable(table, [60, 50, 30, 30, 30, 70, 70, 70, 50]))
		# 	申请入团名单
		pdf.append(makeTitle('申请入团名单'))
		table = [['学号', '姓名', '性别', '民族', '籍贯', '出生日期', '申请入团时间', '备注']]
		table.extend(h[0][3])
		pdf.append(makeTable(table, [60, 50, 30, 30, 70, 70, 70, 50]))
		# 	交纳团费情况
		pdf.append(makeTitle('交纳团费情况'))
		table = [['月份', '支部人数', '应交人数', '实交人数', '应交金额', '实交金额', '备注']]
		table.extend(h[0][4])
		pdf.append(makeTable(table, [50, 50, 50, 50, 100, 100, 100]))
		# 	推优入党名单
		pdf.append(makeTitle('推优入党名单'))
		table = [['学号', '姓名', '提交申请书时间', '入党时间', '转正时间']]
		table.extend(h[0][5])
		pdf.append(makeTable(table, [100, 100, 100, 100, 100]))
		pdf.append(platypus.flowables.PageBreak())
		# 工作计划
		pdf.append(makeTitle('工作计划', 15, 'heimedium'))
		sarr = ['全年计划', '春季学期计划', '秋季学期计划']
		for i in range(3):
			pdf.append(makeTitle(sarr[i]))
			pdf.append(makeCrossPage(h[1][i][0][0], 2900))
			pdf.append(platypus.flowables.PageBreak())
		# 支部事业
		pdf.append(makeTitle('支部事业', 15, 'heimedium'))
		sarr = ['支部事业简介', '支部事业目标', '预期成果']
		for i in range(3):
			pdf.append(makeTitle(sarr[i]))
			pdf.append(makeCrossPage(h[2][i][0][0], 2900))
			pdf.append(platypus.flowables.PageBreak())
		# 思想引领
		sarr1 = ['主题团日', '组织生活']
		for i in range(len(sarr0)):
			titled = False
			for j in range(len(sarr1)):
				if i == 3 and j != 0: continue
				ii = i + 3
				sarr1j = sarr1[j]
				if i == 3: sarr1j = '特色活动'
				if len(h[ii][j]) > 2 or h[ii][j][1][0] != '':
					for k in range(0, len(h[ii][j]), 2):
						if not titled:
							pdf.append(makeTitle(sarr0[i], 15, 'heimedium'))
							titled = True
						meta = h[ii][j][k]
						cont = h[ii][j][k + 1][0]
						pdf.append(makeTitle(sarr1j + ' - ' + meta[0]))
						t = [['时间', meta[1], '地点', meta[2], '参与人数', meta[3]], ['主持人', meta[4], '', '记录人', meta[5], '']]
						# <crosspage>
						arr = crossPage(cont, 2700)
						print(arr)
						tStyle = [
							('FONTNAME',(0,0),(-1,-1),'heilight'),
							('FONTSIZE',(0,0),(-1,-1),8),
							('ALIGN',(0,0),(-1,-1),'CENTER'),
							('VALIGN',(0,0),(-1,-1),'MIDDLE'),
							('GRID',(0,0),(-1,-1),0.5,colors.black),
							('SPAN',(1,1),(2,1)),
							('SPAN',(4,1),(5,1))
							]
						for i in range(len(arr)):
							t.append([arr[i], '', '', '', '', ''])
							tStyle.append(('SPAN',(0,i+2),(-1,i+2)))
						print(t)
						print(tStyle)
						# </crosspage>
						tStyle = TableStyle(tStyle)
						pdf.append(makeTable(t, [90, 80, 80, 90, 80, 80], tStyle))
						pdf.append(platypus.flowables.PageBreak())
		# 工作总结
		pdf.append(makeTitle('全年工作总结', 15, 'heimedium'))
		pdf.append(makeCrossPage(h[7][0][0][0]))
	
	# 文件
	export_path = 'media/' + pdfname + '-' + time.strftime('%Y%m%d%H%M%S') + '.pdf'
	doc = SimpleDocTemplate(export_path)
	doc.build(pdf)
	return export_path

def export_txt(title, txt):
	filename = 'media/' + title + '-' + str(datetime.datetime.now()) + '.txt'
	f = codecs.open(filename, 'w', 'utf-8')
	f.write(filterhtml(txt))
	f.close()
	return filename

def export_csv(title, first_row, a):
	filename = 'media/' + title + '-' + str(datetime.datetime.now()) + '.csv'
	f = codecs.open(filename, 'w', 'gbk')
	f.write(first_row + '\n')
	for b in a:
		for i in range(len(b)):
			f.write('"' + b[i] + '"')
			if i == len(b)-1:
				f.write('\n')
			else:
				f.write(',')
	f.close()
	return filename

def export_jiatuan_fundamental_info(title, a):
	filename = 'media/' + title + '-基本信息-' + str(datetime.datetime.now()) + '.csv'
	f = codecs.open(filename, 'w', 'gbk')
	f.write('团支部名称,团支部书记姓名,男性团员人数,女性团员人数,团员总人数,男性党员人数,女性党员人数,党员总人数,男性申请入党人数,女性申请入党人数,申请入党总人数,班级男性人数,班级女性人数,班级总人数\n')
	f.write('"'+a[0][0][0]+'","'+a[0][0][1]+'"')
	for i in range(12): f.write(',"'+a[1][i//3][i%3]+'"')
	f.write('\n')
	f.close()
	return filename

def export_handbook_fundamental_info(title, a):
	filename = 'media/' + title + '-基本信息-' + str(datetime.datetime.now()) + '.csv'
	f = codecs.open(filename, 'w', 'gbk')
	f.write('团员人数,支部书记	,组织委员	,宣传委员	,备注')
	for b in a[1:]: f.write(',"' + b[0] + '"')
	f.write('\n')
	f.write('"'+a[0][0]+'","'+a[0][1]+'","'+a[0][2]+'","'+a[0][3]+'","' + a[0][4] + '"')
	for b in a[1:]: f.write(',"' + b[1] + '"')
	f.write('\n')
	f.close()
	return filename

def export_handbook_theme_activity(title, first_row, a):
	filename = 'media/' + title + '-主题团日-' + str(datetime.datetime.now()) + '.csv'
	f = codecs.open(filename, 'w', 'gbk')
	f.write(first_row+'\n')
	for i in range(0,len(a),3):
		for b in a[i]: f.write('"'+b+'",')
		f.write('"'+filterhtml(a[i+1][0])+'",')
		f.write('"'+filterhtml(a[i+2][0])+'"\n')
	f.close()
	return filename


def authority_files(request):
	rdata, op, suser = get_request_basis(request)

	if suser.admin_school:
		helps = reversed(Help.objects.all())
	else:
		helps = reversed(Help.objects.filter(released=True))

	rdata['helps'] = helps
	return render(request, 'authority_files.html', rdata)

