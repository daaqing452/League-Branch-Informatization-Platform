from django.contrib import auth
from django.contrib.auth.models import User
from SUser.models import SUser

def get_request_basis(request):
	rdata = {}
	op = request.POST.get('op', '')
	# 检查登录状态
	suser = None
	if request.user.is_authenticated():
		suser = SUser.objects.filter(username=request.user.username)[0]
		rdata['suser'] = suser
	rdata['login'] = suser is not None
	return rdata, op, suser