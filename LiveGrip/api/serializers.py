from django.contrib.auth.models import User

from rest_framework import serializers

from models import *

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = '__all__'

	def create(self, validated_data):
		username=validated_data['username']
		user = User(username=username)
		user.set_password(validated_data['password'])
		user.save()
		return user

class EventSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event
		fields = ('name', 'info', 'image', 'location', 'start_time', 'end_time', 'match_card')


# class MessageSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = Message
# 		fields = ('body')