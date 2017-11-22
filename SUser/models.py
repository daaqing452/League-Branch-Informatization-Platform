# -*- coding: utf-8 -*-
from django.db import models

class SUser(models.Model):
	uid = models.IntegerField()
	username = models.CharField(max_length=32, default='')
	admin_super = models.BooleanField(default=False)
	admin_school = models.BooleanField(default=False)

class Department(models.Model):
	name = models.CharField(max_length=64, default='')
	admin = models.TextField(default='[]')

class Branch(models.Model):
	name = models.CharField(max_length=32, default='')
	did = models.IntegerField()
	admin = models.TextField(default='[]')
	member = models.TextField(default='[]')