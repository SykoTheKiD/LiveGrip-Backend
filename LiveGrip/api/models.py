from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	class Meta:
		ordering = ['id']

	profile_image = models.CharField(max_length=300, null=True, default="unset")
	gcm_id = models.CharField(max_length=500, default="not_set", null=True)
	app_version = models.CharField(max_length=10, default="undefined", null=True)

STATUS_CHOICES = (
    ('h', 'Holding'),
    ('p', 'Published')
)

class Event(models.Model):
	
	class Meta:
		db_table = 'events'
		ordering = ['start_time']
	
	name = models.CharField(max_length=30, null=False)
	info = models.TextField(default=None)
	image = models.CharField(max_length=70, null=False)
	location = models.CharField(max_length=30, null=False)
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	match_card = models.TextField(default="TBA")
	status = models.CharField(max_length=1, choices=STATUS_CHOICES)

	def __unicode__(self):
		return self.name

class Message(models.Model):

	class Meta:
		db_table = 'messages'

	event_id = models.ForeignKey(Event, verbose_name="event")
	user_id = models.ForeignKey(User, verbose_name="message user")
	body = models.TextField(verbose_name='message')