# -*- coding: utf-8 -*-
from django.db import models

class Message(models.Model):
	send_uid = models.IntegerField()
	recv_uid = models.TextField()
	mtype = models.IntegerField()
	text = models.TextField()
