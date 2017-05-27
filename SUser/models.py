# -*- coding: utf-8 -*-
from django.db import models

class SUser(models.Model):
	uid = models.IntegerField()
	username = models.CharField(max_length=32, default='')
	admin_super = models.BooleanField(default=False)
	admin_school = models.BooleanField(default=False)
	admin_department = models.TextField(default='[]')
	admin_branch = models.TextField(default='[]')

class Department(models.Model):
	name = models.CharField(max_length=64, default='')

class Branch(models.Model):
	name = models.CharField(max_length=32, default='')
	did = models.IntegerField()
