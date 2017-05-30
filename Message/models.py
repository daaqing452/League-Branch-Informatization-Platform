# -*- coding: utf-8 -*-
from django.db import models

class Message(models.Model):
	send_uid = models.IntegerField(default=0)
	recv_uid = models.TextField(default='[]')
	mtype = models.IntegerField(default=0)
	title = models.TextField()
	text = models.TextField()
	attachment = models.TextField(default='[]')
	read = models.BooleanField(default=False)