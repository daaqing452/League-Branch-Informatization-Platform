from django.contrib import auth
from django.contrib.auth.models import User
from SUser.models import SUser, Department, Branch

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

	return rdata, op, suser