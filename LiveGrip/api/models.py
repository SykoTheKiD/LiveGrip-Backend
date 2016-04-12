from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	profile_image = models.CharField(max_length=300)
	gcm_id = models.CharField(max_length=500, default="not_set")
	app_version = models.CharField(max_length=10, default="undefined")

class Event(models.Model):
	
	class Meta:
		db_table = 'events'
	
	name = models.CharField(max_length=30, null=False)
	info = models.TextField(default=None)
	image = models.CharField(max_length=70, null=False)
	location = models.CharField(max_length=30, null=False)
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	match_card = models.TextField(default="TBA")

class Message(models.Model):

	class Meta:
		db_table = 'messages'

	event_id = models.ForeignKey(Event, verbose_name="the related event")
	user_id = models.ForeignKey(User, verbose_name="message's user")
	body = models.TextField()