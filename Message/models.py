# -*- coding: utf-8 -*-
from django.db import models

class Message(models.Model):
	recv_uid = models.IntegerField(default=0)
	send_uid = models.IntegerField(default=0)
	group = models.IntegerField(default=0)
	read = models.BooleanField(default=False)
	mtype = models.IntegerField(default=0)
	send_time = models.DateTimeField(default='1970-01-01 00:00:00.000000')
	# read_time = models.DateTimeField(default='1970-01-01 00:00:00.000000')
	title = models.TextField(default='')
	text = models.TextField(default='')
	attachment = models.TextField(default='[]')
	meta = models.TextField(default='{}')

class Handbook(models.Model):
	htype = models.CharField(max_length=1, default='.')
	review_id = models.IntegerField(default=0)
	submit_id = models.IntegerField(default=0)
	year = models.IntegerField(default=0)
	content = models.TextField(default='')
	submitted = models.BooleanField(default=False)

class News(models.Model):
	display_type = models.CharField(max_length=1, default='.')
	display_id = models.IntegerField(default=0)
	year = models.IntegerField(default=0)
	title = models.TextField(default='')
	text = models.TextField(default='')

class JiatuanMaterial(models.Model):
	htype = models.CharField(max_length=1, default='.')
	review_id = models.IntegerField(default=0)
	submit_id = models.IntegerField(default=0)
	year = models.IntegerField(default=0)
	attachment = models.TextField(default='[]')