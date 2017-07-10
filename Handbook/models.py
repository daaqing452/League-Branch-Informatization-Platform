from django.db import models

class Handbook(models.Model):
	htype = models.CharField(max_length=2, default='n')
	review_id = models.IntegerField(default=0)
	submit_id = models.IntegerField(default=0)
	content = models.TextField(default='')