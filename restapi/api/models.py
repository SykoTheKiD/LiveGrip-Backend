from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
	username = models.CharField(max_length=30, null=False)
	password = models.CharField(max_length=200, null=False)
	email = models.CharField(max_length=50)
	profile_image = models.CharField(max_length=300)
	email_verified = models.BooleanField(default=False)


class Event(models.Model):
	name = models.CharField(max_length=30, null=False)
	info = models.CharField(max_length=500, null=False)
	image = models.CharField(max_length=70, null=False)
	location = models.CharField(max_length=30, null=False)
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	match_card = models.TextField(default="TBA")

class Message(models.Model):
	event_id = models.ForeignKey(Event, verbose_name="the related event")
	user_id = models.ForeignKey(User, verbose_name="message's user")
	body = models.TextField()


		
		