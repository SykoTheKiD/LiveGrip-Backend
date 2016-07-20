from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

class User(AbstractUser):
	class Meta:
		ordering = ['id']

	profile_image = models.CharField(max_length=300, null=True, default="unset")
	app_version = models.CharField(max_length=10, default="undefined", null=True)

	def __unicode__(self):
		return self.username

	def authenticate(self, username=None, password=None):
		try:
			user = User.objects.get(username__iexact=username)
			if user.check_password(password):
				return user
			else:
				return None
		except User.DoesNotExist:
			return None

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
	image = models.CharField(max_length=200, null=False)
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

	event = models.ForeignKey(Event, verbose_name="event", on_delete=models.CASCADE)
	user = models.ForeignKey(User, verbose_name="message user")
	body = models.TextField(verbose_name='message')
	created = models.DateTimeField(auto_now_add=True)


# This code is triggered whenever a new user has been created and saved to the database

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)