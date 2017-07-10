# -*- coding: utf-8 -*-
from django.contrib import auth
from django.contrib.auth.models import User
from django.db.models import Q 
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from SUser.models import SUser, Department, Branch
from SUser.utils import get_request_basis
import json

def handbook(request, htype, hid):
	rdata, op, suser = get_request_basis(request)
	return render(request,'handbook.html', rdata)