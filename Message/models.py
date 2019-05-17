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

class News(models.Model):
	display_type = models.CharField(max_length=1, default='.')
	display_id = models.IntegerField(default=0)
	post_time = models.DateTimeField(default='1970-01-01 00:00:00.000000')
	# year = models.IntegerField(default=0)
	title = models.TextField(default='')
	text = models.TextField(default='')

class Slide(models.Model):
	display_type = models.CharField(max_length=1, default='.')
	display_id = models.IntegerField(default=0)
	post_time = models.DateTimeField(default='1970-01-01 00:00:00.000000')
	title = models.TextField(default='')
	text = models.TextField(default='')
	img_path = models.TextField(default='')
	show = models.BooleanField(default=True)


class Handbook(models.Model):
	htype = models.CharField(max_length=1, default='.')
	review_id = models.IntegerField(default=0)
	submit_id = models.IntegerField(default=0)
	year = models.IntegerField(default=0)
	content = models.TextField(default='')
	submitted = models.BooleanField(default=False)


class JiatuanApportion(models.Model):
	year = models.IntegerField(default=0)
	deadline = models.DateTimeField(default='2099-12-31 23:59:59.999999')
	minge = models.TextField(default='{}')

class JiatuanAssignment(models.Model):
	year = models.IntegerField(default=0)
	did = models.IntegerField(default=0)
	branchs = models.TextField(default='[]')
	submitted = models.BooleanField(default=False)

class JiatuanMaterial(models.Model):
	submit_id = models.IntegerField(default=0)
	year = models.IntegerField(default=0)
	content = models.TextField(default='')
	submitted = models.BooleanField(default=False)
	attachment = models.TextField(default='[]')

class Help(models.Model):
	# authourity_files
	title = models.CharField(max_length=128, default='')
	content = models.TextField(default='')
	attachment = models.TextField(default='[]')
	founder = models.IntegerField(default=-1)
	released = models.BooleanField(default=0)
	create_time = models.DateTimeField(default='1970-01-01 00:00:00.000000')
	release_time = models.DateTimeField(default='1970-01-01 00:00:00.000000')

class AHelp(models.Model):
	# announcement
	title = models.CharField(max_length=128, default='')
	content = models.TextField(default='')
	attachment = models.TextField(default='[]')
	founder = models.IntegerField(default=-1)
	released = models.BooleanField(default=0)
	create_time = models.DateTimeField(default='1970-01-01 00:00:00.000000')
	release_time = models.DateTimeField(default='1970-01-01 00:00:00.000000')

class CHelp(models.Model):
	# case_study
	title = models.CharField(max_length=128, default='')
	content = models.TextField(default='')
	attachment = models.TextField(default='[]')
	founder = models.IntegerField(default=-1)
	released = models.BooleanField(default=0)
	create_time = models.DateTimeField(default='1970-01-01 00:00:00.000000')
	release_time = models.DateTimeField(default='1970-01-01 00:00:00.000000')