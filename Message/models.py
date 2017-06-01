# -*- coding: utf-8 -*-
from django.db import models

class Message(models.Model):
	recv_uid = models.IntegerField(default=0)
	send_uid = models.IntegerField(default=0)
	group_id = models.IntegerField(default=0)
	read = models.BooleanField(default=False)
	mtype = models.IntegerField(default=0)
	send_time = models.DateTimeField(default='1970-01-01 00:00:00.000000')
	read_time = models.DateTimeField(default='1970-01-01 00:00:00.000000')
	title = models.TextField(default='')
	text = models.TextField(default='')
	attachment = models.TextField(default='[]')