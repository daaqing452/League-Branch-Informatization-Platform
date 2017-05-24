# -*- coding: utf-8 -*-
from django.db import models

class SUser(models.Model):
	uid = models.IntegerField()
	username = models.CharField(max_length=32, default='')
	authority = models.TextField()

class Department(models.Model):
	branch = models.TextField()

class Branch(models.Model):
	did = models.IntegerField()
	suser = models.TextField()
