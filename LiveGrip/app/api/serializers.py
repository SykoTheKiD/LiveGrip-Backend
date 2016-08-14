from rest_framework import serializers

from api.models import *

import json

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id','username', 'profile_image')

	def create(self, validated_data):
		user = None
		try:
			username = validated_data['username']
			password = validated_data['password']
			app_version = validated_data['app_version']
			user = User(username=username, app_version=app_version)
			user.set_password(password)
			try:
				profile_image = validated_data['profile_image']
				user.profile_image = profile_image
			except KeyError:
				user.profile_image = "http://i.imgur.com/bVlVbb2.jpg"
			user.save()
			return user
		except KeyError:
			return user
			
class EventSerializer(serializers.ModelSerializer):
	start_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
	end_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
	class Meta:
		model = Event
		fields = ('id','name', 'info', 'image','location', 'event_video', 'start_time', 'end_time', 'match_card')

class MessageSerializer():
	def __init__(self, request):
		self.request = request
		self.key = None
		self.value = {}
		self.error = None

	def is_valid(self):
		try:
			self.value['user_id'] = self.request.data['user_id']
			self.value['event_id'] = self.request.data['event_id']
			self.value['username'] = self.request.data['username']
			self.value['profile_image'] = self.request.data['profile_image']
			self.value['body'] = self.request.data['body']
			self.key = self.request.data['event_id']
			return True
		except KeyError:
			self.error = "Missing Fields"
			return False

	def getKey(self):
		return str(self.key)

	def getValue(self):
		return json.dumps(self.value)


class DatabaseMessageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Message
		fields = ('user', 'event', 'body')

class AccessTokenSerializer(serializers.ModelSerializer):
	expiry_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
	class Meta:
		model = AccessToken
		fields = ('key', 'expiry_date')