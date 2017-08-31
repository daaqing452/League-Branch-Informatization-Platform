from django.contrib import auth
from django.contrib.auth.models import User
from SUser.models import SUser, Department, Branch
from Message.models import Message
import json

def get_request_basis(request):
	rdata = {}
	op = request.POST.get('op', '')
	
	# 检查登录状态
	suser = None
	if request.user.is_authenticated():
		suser = SUser.objects.filter(username=request.user.username)[0]
		rdata['suser'] = suser
	rdata['login'] = suser is not None

	# 院系
	departments = Department.objects.all()
	d0 = []
	for department in departments:
		d1 = {}
		d1['department'] = department
		d1['branchs'] = Branch.objects.filter(did=department.id)
		d0.append(d1)
	rdata['departments'] = d0

	# 消息
	messages = []
	if suser is not None:
		messages = Message.objects.filter(recv_uid=suser.id).filter(read=False)
	rdata['unread_messages'] = messages
	rdata['unread_messages_length'] = len(messages)

	# 个人归属
	rdata['self_department'] = None
	rdata['self_admin_department'] = False
	rdata['self_branch'] = None
	rdata['self_admin_branch'] = False
	if suser is not None:
		for department in Department.objects.all():
			if suser.id in json.loads(department.admin):
				rdata['self_admin_department'] = True
				rdata['self_department'] = department
				break
		for branch in Branch.objects.all():
			if suser.id in json.loads(branch.admin):
				rdata['self_admin_branch'] = True
				rdata['self_branch'] = branch
				rdata['self_department'] = Department.objects.get(id=branch.did)
				break
			if suser.id in json.loads(branch.member):
				rdata['self_branch'] = branch
				rdata['self_department'] = Department.objects.get(id=branch.did)
		
	return rdata, op, suser